#!/usr/bin/env python3
"""brain_lint.py: hard-rule scan of brain repo content before a PR.

Scans a directory tree, a single file, or a unified git diff (only added "+" lines).
Prints only offending  file:line  rule  [REDACTED ...]  lines.
NEVER prints the matched secret or PII value. A short hash tag lets you tell
repeat hits apart without seeing the value.

Usage:
  python3 brain_lint.py DIR_OR_FILE [...]
  python3 brain_lint.py --diff changes.diff
  git diff --cached | python3 brain_lint.py --diff -
  options: --json, --rules secrets,pii,emdash, --allow-email ADDR, --allow-phone DIGITS,
           --max-per-file N (default 50, 0 = no cap), --summary
Exit code: 0 clean, 1 any hit, 2 script error.
"""
import argparse, hashlib, json, os, re, sys

EM = "\u2014"

# Ryne's own business addresses (allowed). Compared lowercase.
ALLOWED_EMAILS = {
    "ryne@achievesportsperformance.com",
    "ryne@ironblueprint.app",
    "ryne@iron-blueprint.com",
    "contact@achievesportsperformance.com",
    "contact@achieve-personaltraining.com",
}
ALLOWED_EMAIL_DOMAINS = {"group.calendar.google.com", "example.com", "example.org", "users.noreply.github.com"}
# Public business numbers (digits only, 10 digits).
ALLOWED_PHONES = {"6303404114"}

SECRET_RULES = [
    ("private-key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("stripe-live-key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{10,}")),
    ("stripe-test-key", re.compile(r"\b(?:sk|rk)_test_[0-9A-Za-z]{10,}")),
    ("stripe-webhook-secret", re.compile(r"\bwhsec_[0-9A-Za-z]{16,}")),
    ("mongodb-uri-with-password", re.compile(r"mongodb(?:\+srv)?://[^\s:/@]+:[^\s@/]+@")),
    ("db-uri-with-password", re.compile(r"\b(?:postgres(?:ql)?|mysql|redis|amqp)://[^\s:/@]+:[^\s@/]+@")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})")),
    ("slack-token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("slack-webhook", re.compile(r"hooks\.slack\.com/services/[A-Za-z0-9/]{20,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("openai-style-key", re.compile(r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}")),
    ("xai-key", re.compile(r"\bxai-[A-Za-z0-9]{20,}")),
    ("bearer-token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}", re.I)),
    ("url-basic-auth", re.compile(r"\bhttps?://[^\s:/@]+:[^\s@/]{3,}@")),
    ("password-assignment", re.compile(
        r"(?i)\b(?:password|passwd|pwd|pass|secret|client_secret|api[_-]?key|apikey|access[_-]?token|auth[_-]?token|token)\b"
        r"\s*[:=]\s*[\"']?(?!\s*(?:<|\$\{|\{\{|null|none|true|false|redacted|\*{3}|xxx|\[))[^\s\"',;]{8,}")),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<![\w.-])(?:\+?1[\s.-]?)?\(?([2-9]\d{2})\)?[\s.-]?(\d{3})[\s.-](\d{4})(?![\w-])")

TEXT_EXT_SKIP = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".gz", ".mp3", ".mp4", ".mov",
                 ".docx", ".xlsx", ".pptx", ".db", ".sqlite", ".ico", ".woff", ".woff2", ".ttf", ".bin"}


def tag(value):
    return hashlib.sha256(value.encode("utf-8", "ignore")).hexdigest()[:8]


def scan_line(text, rules, allow_emails, allow_phones):
    hits = []
    if "secrets" in rules:
        for name, rx in SECRET_RULES:
            for m in rx.finditer(text):
                hits.append((name, f"[REDACTED secret #{tag(m.group(0))}]"))
    if "pii" in rules:
        for m in EMAIL_RE.finditer(text):
            if m.start() > 0 and text[m.start() - 1] in ":/":
                continue  # credential part of a URI, already covered by the URI rules
            addr = m.group(0).lower()
            dom = addr.split("@", 1)[1]
            if addr in allow_emails or dom in ALLOWED_EMAIL_DOMAINS:
                continue
            hits.append(("pii-email", f"[REDACTED email @{dom.split('.')[-2] if '.' in dom else dom}.. #{tag(addr)}]"))
        for m in PHONE_RE.finditer(text):
            digits = "".join(m.groups())
            if digits in allow_phones:
                continue
            hits.append(("pii-phone", f"[REDACTED phone #{tag(digits)}]"))
    if "emdash" in rules and EM in text:
        hits.append(("em-dash", f"{text.count(EM)} em dash(es)"))
    return hits


def iter_files(path):
    if os.path.isfile(path):
        yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", "secrets")]
        for f in sorted(files):
            yield os.path.join(root, f)


def read_text(path):
    if os.path.splitext(path)[1].lower() in TEXT_EXT_SKIP:
        return None
    try:
        with open(path, "rb") as fh:
            data = fh.read(5_000_000)
    except OSError:
        return None
    if b"\x00" in data[:4096]:
        return None
    return data.decode("utf-8", "replace")


def iter_diff(fh):
    """Yield (file, new_line_no, text) for added lines in a unified diff."""
    cur, ln = None, 0
    for raw in fh:
        line = raw.rstrip("\n")
        if line.startswith("+++ "):
            p = line[4:].strip()
            cur = None if p == "/dev/null" else re.sub(r"^b/", "", p)
            continue
        if line.startswith("--- "):
            continue
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if m:
            ln = int(m.group(1))
            continue
        if cur is None:
            continue
        if line.startswith("+"):
            yield cur, ln, line[1:]
            ln += 1
        elif line.startswith("-") or line.startswith("\\"):
            continue
        else:
            ln += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--diff", help="unified diff file, or - for stdin")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rules", default="secrets,pii,emdash")
    ap.add_argument("--allow-email", action="append", default=[])
    ap.add_argument("--allow-phone", action="append", default=[])
    ap.add_argument("--max-per-file", type=int, default=50)
    ap.add_argument("--summary", action="store_true", help="print hit counts per rule and per file instead of every line")
    a = ap.parse_args()
    if not a.paths and not a.diff:
        ap.error("give a directory/file or --diff")
    rules = set(a.rules.split(","))
    allow_e = ALLOWED_EMAILS | {x.lower() for x in a.allow_email}
    allow_p = ALLOWED_PHONES | {re.sub(r"\D", "", x)[-10:] for x in a.allow_phone}

    hits, files_scanned, suppressed = [], 0, {}

    def record(fname, ln, text):
        for rule, marker in scan_line(text, rules, allow_e, allow_p):
            n = sum(1 for h in hits if h["file"] == fname)
            if a.max_per_file and n >= a.max_per_file:
                suppressed[fname] = suppressed.get(fname, 0) + 1
                continue
            hits.append({"file": fname, "line": ln, "rule": rule, "detail": marker})

    if a.diff:
        fh = sys.stdin if a.diff == "-" else open(a.diff, encoding="utf-8", errors="replace")
        seen = set()
        for fname, ln, text in iter_diff(fh):
            seen.add(fname)
            record(fname, ln, text)
        files_scanned += len(seen)
    for p in a.paths:
        for f in iter_files(p):
            t = read_text(f)
            if t is None:
                continue
            files_scanned += 1
            for i, line in enumerate(t.splitlines(), 1):
                record(f, i, line)

    total = len(hits) + sum(suppressed.values())
    if a.json:
        by_rule = {}
        for h in hits:
            by_rule[h["rule"]] = by_rule.get(h["rule"], 0) + 1
        print(json.dumps({"files_scanned": files_scanned, "hit_count": total, "by_rule": by_rule,
                          "hits": hits, "suppressed_per_file": suppressed}, indent=2))
    elif a.summary:
        from collections import Counter
        br, bf = Counter(), Counter()
        for h in hits:
            br[h["rule"]] += 1
            bf[(h["file"], h["rule"])] += 1
        for f, n in suppressed.items():
            bf[(f, "more (capped)")] += n
        for r, n in sorted(br.items()):
            print(f"rule {r}: {n}")
        for (f, r), n in sorted(bf.items()):
            print(f"{f}  {r}  x{n}")
        print(f"{total} hits in {files_scanned} files scanned" if total else f"0 hits ({files_scanned} files scanned)")
    else:
        for h in hits:
            print(f"{h['file']}:{h['line']}  {h['rule']}  {h['detail']}")
        for f, n in suppressed.items():
            print(f"{f}: +{n} more hits not shown (--max-per-file)")
        print(f"{total} hits in {files_scanned} files scanned" if total else f"0 hits ({files_scanned} files scanned)")
    return 1 if total else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"brain_lint error: {type(e).__name__}", file=sys.stderr)
        sys.exit(2)
