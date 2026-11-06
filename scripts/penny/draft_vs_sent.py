#!/usr/bin/env python3
"""draft_vs_sent.py: compare the Gmail drafts Penny saved with what Ryne actually sent.

Read-only. Python 3 standard library only. Calls no API: it never reads Gmail itself and never
sends, edits or deletes a draft or an email. Penny saves her drafts (draft-log.jsonl) and pulls Sent
mail (and, optionally, the current Drafts list) read-only with her Gmail connectors, saves the JSON,
runs this, then reads the summary.

Matching (each sent message is used at most once, drafts are taken oldest first):
  1. threadId: a sent message in the draft's thread, dated from the save time (minus --slack-minutes)
     up to --window-days after it. If several qualify, the most similar one wins.
  2. fallback: a sent message that shares at least one recipient (To/Cc) with the draft and has the
     same normalized subject (Re:/Fwd:/[EXTERNAL] prefixes, curly quotes, case and spacing ignored),
     in the same time window.
Before comparing, both bodies get: CRLF -> LF, quoted reply text cut ("On ... wrote:", "> " lines,
"-----Original Message-----", Outlook "From:/Sent:" headers), the signature block cut (from the
"Ryne Gioviano, MSEd" line or a "-- " line down, so a typed signature and a Gmail-added one are equal),
curly quotes made straight, and whitespace collapsed. The sign-off ("Thanks," etc.) is split off and
compared separately.

Classification (word-level similarity = difflib ratio 2*M/T on the core word lists):
  sent_as_is   core words identical and same sign-off (whitespace/signature/quote differences ignored)
  light_edit   similarity >= --light-threshold (default 0.85), or only the sign-off changed
  heavy_edit   similarity <  --light-threshold
  never_sent   no match. never_sent_reason: deleted (not in --open-drafts), still_in_drafts (open and
               the window has passed), pending (window not over yet; not counted as a change), or
               unknown (no --open-drafts given and the window has passed).
A matched pair with similarity < --rewrite-threshold (default 0.40) is flagged doubtful_match: Ryne
may have written a fresh reply in the same thread instead of editing the draft. Check those by hand.

Usage:
  python3 draft_vs_sent.py --drafts draft-log.jsonl --sent sent.json [--open-drafts list_drafts.json]
                           [--now "2026-10-23 10:30 CT"] [--format text|json] [--out result.json]
Exit code: 0 no changes (every matched draft sent as is, nothing final never_sent), 1 changes found,
2 error (bad input: report it, do not guess).
"""
import argparse, collections, datetime as dt, difflib, html, json, os, re, sys

try:
    from zoneinfo import ZoneInfo
    CT = ZoneInfo("America/Chicago")
except Exception:  # pragma: no cover - no tz database
    CT = dt.timezone(dt.timedelta(hours=-5), "CT")

DEFAULT_LOG = "/home/box/agent-data/penny/draft-log.jsonl"
LIGHT_THRESHOLD = 0.85
REWRITE_THRESHOLD = 0.40
WINDOW_DAYS = 3.0
SLACK_MINUTES = 10

ADDR_RX = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+")
SUBJ_PREFIX_RX = re.compile(r"^\s*((re|aw|fw|fwd)\s*:\s*|\[external\]\s*)+", re.I)
# Where quoted reply text starts (everything from here down is dropped).
QUOTE_START_RX = [
    re.compile(r"^\s*On .{3,300}wrote:\s*$", re.I | re.S),
    re.compile(r"^\s*-{2,}\s*Original Message\s*-{2,}", re.I),
    re.compile(r"^\s*-{2,}\s*Forwarded message\s*-{2,}", re.I),
    re.compile(r"^\s*From:\s.+$", re.I),          # Outlook header block (only if followed by Sent:/Date:)
    re.compile(r"^\s*_{8,}\s*$"),
]
# Signature: first line of Ryne's block, or the RFC "-- " delimiter.
SIG_START_RX = [
    re.compile(r"^\s*Ryne Gioviano\s*,?\s*MSEd", re.I),
    re.compile(r"^--\s?$"),
]
SIGNOFF_RX = re.compile(
    r"^(thanks|thank you|thanks so much|thanks again|many thanks|best|best regards|regards|cheers|talk soon|"
    r"see you( soon| then| at \S+| there| both( at \S+)?)?|looking forward to it|take care|sincerely)\b.{0,60}$", re.I)
GREETING_RX = re.compile(r"^(hi|hello|hey|dear|good (morning|afternoon|evening))\b[^\n.?]{0,40}[,!:]?$|^[A-Z][\w'-]+( and [A-Z][\w'-]+)?,$", re.I)
SENT_SPLIT_RX = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
CURLY = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-",
                       "\u00a0": " ", "\u2022": "*"})
STOP = set("a an the and or but to of in on at for with is are be it its it's this that we you i he she they "
           "his her their our your my me us so if as by from him them can will we'll we're i'll i'd you'd you're "
           "there there's what when then than once just let know about up out into over do does did done have has "
           "had get got would could should also all any some more most very much one".split())


class InputError(Exception):
    pass


# ---------------------------------------------------------------- loading
def _parse_json_text(text, where):
    text = text.strip()
    if not text:
        return []
    try:
        return json.loads(text)
    except ValueError:
        pass
    lines = [l for l in text.splitlines() if l.strip()]
    try:
        return [json.loads(l) for l in lines]
    except ValueError:
        pass
    # connector output saved with write_to_file: wrapper text around the JSON
    starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
    if starts:
        s = min(starts)
        e = max(text.rfind("}"), text.rfind("]"))
        try:
            return json.loads(text[s:e + 1])
        except ValueError:
            pass
    raise InputError("%s: not JSON, JSONL or connector output" % where)


def load_records(paths, keys):
    out = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as fh:
                data = _parse_json_text(fh.read(), p)
        except OSError as e:
            raise InputError("%s: %s" % (p, e))
        acct = None
        if isinstance(data, dict):
            acct = data.get("account")
            for k in keys:
                if isinstance(data.get(k), list):
                    data = data[k]
                    break
            else:
                data = [data] if data.get("body") is not None or data.get("id") else []
        if not isinstance(data, list):
            raise InputError("%s: expected a list of records" % p)
        for r in data:
            if not isinstance(r, dict):
                raise InputError("%s: record is not an object: %r" % (p, r))
            r = dict(r)
            if acct and not r.get("account"):
                r["account"] = acct
            out.append(r)
    return out


def parse_time(value, where=""):
    """ISO with Z/offset (UTC-aware), or 'YYYY-MM-DD HH:MM[ CT]' (box-local Chicago)."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(value / (1000 if value > 1e11 else 1), dt.timezone.utc)
    s = str(value).strip()
    local = bool(re.search(r"\s(CT|CST|CDT)$", s))
    s = re.sub(r"\s(CT|CST|CDT)$", "", s)
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    for fmt in (None, "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            t = dt.datetime.fromisoformat(s) if fmt is None else dt.datetime.strptime(s, fmt)
            break
        except ValueError:
            t = None
    if t is None:
        raise InputError("bad date %r %s" % (value, where))
    if t.tzinfo is None or local:
        t = t.replace(tzinfo=CT)
    return t


def fmt_ct(t):
    return t.astimezone(CT).strftime("%Y-%m-%d %H:%M CT") if t else None


def addresses(*fields):
    out = []
    for f in fields:
        if isinstance(f, list):
            f = ", ".join(str(x) for x in f)
        for a in ADDR_RX.findall(f or ""):
            a = a.lower()
            if a not in out:
                out.append(a)
    return out


def norm_subject(s):
    s = (s or "").translate(CURLY)
    prev = None
    while prev != s:
        prev = s
        s = SUBJ_PREFIX_RX.sub("", s)
    return re.sub(r"\s+", " ", s).strip().lower()


# ---------------------------------------------------------------- text cleaning
def html_to_text(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(div|p|li|tr|h\d)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s)


def strip_quoted(text):
    lines = text.split("\n")
    keep = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith(">"):
            break
        # "On ... wrote:" may wrap over 2-3 lines
        joined = " ".join(l.strip() for l in lines[i:i + 3])
        if re.match(r"^\s*On\s", line) and re.search(r"wrote:\s*$", joined.split("wrote:")[0] + "wrote:") \
                and "wrote:" in joined:
            break
        if any(rx.match(line) for rx in QUOTE_START_RX[1:3] + QUOTE_START_RX[4:]):
            break
        if QUOTE_START_RX[3].match(line):
            nxt = " ".join(lines[i + 1:i + 4])
            if re.search(r"(?im)^\s*(sent|date):", "\n".join(lines[i + 1:i + 4])) or "Sent:" in nxt:
                break
        keep.append(line)
        i += 1
    return "\n".join(keep)


def split_signature(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if any(rx.match(line) for rx in SIG_START_RX):
            return "\n".join(lines[:i]), True
    return text, False


def clean(body, is_html=False):
    """Return dict: paragraphs (core, no sign-off), signoff, has_signature, words."""
    t = body or ""
    if is_html or (re.search(r"(?i)<(div|br|p)\b", t) and "\n\n" not in t):
        t = html_to_text(t)
    t = t.replace("\r\n", "\n").replace("\r", "\n").translate(CURLY)
    t = strip_quoted(t)
    t, has_sig = split_signature(t)
    paras = [re.sub(r"[ \t]+", " ", " ".join(p.split("\n"))).strip() for p in re.split(r"\n\s*\n", t)]
    paras = [p for p in paras if p]
    # a paragraph may still hold "Thanks,\nRyne" style lines; split the last para's lines for sign-off
    signoff = ""
    if paras:
        last_lines = [l.strip() for l in re.split(r"\n\s*\n", t.strip())[-1].split("\n") if l.strip()]
        if last_lines and SIGNOFF_RX.match(last_lines[0]) and len(" ".join(last_lines).split()) <= 12:
            signoff = " ".join(last_lines)
            paras = paras[:-1]
        else:
            # sign-off glued to the end of the last paragraph line ("... See you at 5!")
            last = paras[-1]
            sents = SENT_SPLIT_RX.split(last)
            if len(sents) == 1 and SIGNOFF_RX.match(last) and len(last.split()) <= 8:
                signoff = last
                paras = paras[:-1]
    greeting = ""
    if paras and GREETING_RX.match(paras[0]) and len(paras[0].split()) <= 8:
        greeting = paras[0]
    elif paras:
        m = re.match(r"^((?:hi|hello|hey|dear)\b[^,\n]{0,40},)\s+(.*)$", paras[0], re.I)
        if m:
            greeting = m.group(1)
            paras = [greeting, m.group(2)] + paras[1:]
    words = " ".join(paras).split()
    return {"paragraphs": paras, "greeting": greeting, "signoff": signoff, "has_signature": has_sig,
            "words": words}


def body_of(rec):
    if rec.get("body"):
        return rec["body"], False
    if rec.get("htmlBody"):
        return rec["htmlBody"], True
    return rec.get("snippet", "") or "", False


# ---------------------------------------------------------------- comparison
def similarity(a, b):
    if not a and not b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def word_diff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops, inline = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            inline.append(" ".join(a[i1:i2]))
            continue
        old, new = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        ops.append({"op": tag, "removed": old, "added": new})
        if old:
            inline.append("[-%s-]" % old)
        if new:
            inline.append("{+%s+}" % new)
    return ops, " ".join(x for x in inline if x)


def sentences(paras, skip_greeting):
    out = []
    for i, p in enumerate(paras):
        if i == 0 and skip_greeting:
            continue
        out.extend(s.strip() for s in SENT_SPLIT_RX.split(p) if s.strip())
    return out


def _key(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def opening_report(d, s):
    ds, ss = sentences(d["paragraphs"], bool(d["greeting"])), sentences(s["paragraphs"], bool(s["greeting"]))
    dkeys, skeys = {_key(x) for x in ds}, {_key(x) for x in ss}
    rep = {"greeting_draft": d["greeting"], "greeting_sent": s["greeting"],
           "greeting_changed": _key(d["greeting"]) != _key(s["greeting"]),
           "opening_draft": ds[0] if ds else "", "opening_sent": ss[0] if ss else "",
           "opening_changed": bool(ds or ss) and (_key(ds[0]) if ds else "") != (_key(ss[0]) if ss else ""),
           "opening_removed": [], "opening_added": []}
    # leading sentences that disappeared / appeared (up to the first shared sentence)
    for x in ds:
        if _key(x) in skeys:
            break
        rep["opening_removed"].append(x)
    for x in ss:
        if _key(x) in dkeys:
            break
        rep["opening_added"].append(x)
    rep["sentences_removed"] = [x for x in ds if _key(x) not in skeys and not _near(x, ss)]
    rep["sentences_added"] = [x for x in ss if _key(x) not in dkeys and not _near(x, ds)]
    return rep


def _near(x, pool, cut=0.75):
    xw = x.lower().split()
    return any(similarity(xw, y.lower().split()) >= cut for y in pool)


def norm_phrase(s):
    s = s.lower().translate(CURLY)
    s = re.sub(r"^[^\w$]+|[^\w%]+$", "", s)
    return re.sub(r"\s+", " ", s)


def classify(sim, d, s, light):
    same_signoff = _key(d["signoff"]) == _key(s["signoff"]) and d["signoff"].strip()[-1:] == s["signoff"].strip()[-1:]
    if d["words"] == s["words"]:
        return "sent_as_is" if same_signoff else "light_edit"
    return "light_edit" if sim >= light else "heavy_edit"


def compare(draft, sent, light):
    db, dh = body_of(draft)
    sb, sh = body_of(sent)
    d, s = clean(db, dh), clean(sb, sh)
    sim = similarity(d["words"], s["words"])
    ops, inline = word_diff(d["words"], s["words"])
    cls = classify(sim, d, s, light)
    dto, sto = addresses(draft.get("to"), draft.get("cc")), addresses(sent.get("to"), sent.get("cc"))
    rep = {
        "classification": cls,
        "similarity": round(sim, 3),
        "word_count": {"draft": len(d["words"]), "sent": len(s["words"]),
                       "change": len(s["words"]) - len(d["words"]),
                       "change_pct": round(100.0 * (len(s["words"]) - len(d["words"])) / max(1, len(d["words"])), 1)},
        "word_diff": ops,
        "word_diff_inline": inline,
        "opening": opening_report(d, s),
        "signoff": {"draft": d["signoff"], "sent": s["signoff"],
                    "changed": d["signoff"].strip() != s["signoff"].strip(),
                    "signature_draft": d["has_signature"], "signature_sent": s["has_signature"],
                    "note": "signature block ignored in the comparison (typed or Gmail-added count as equal)"},
        "recipients": {"draft": dto, "sent": sto, "removed": [a for a in dto if a not in sto],
                       "added": [a for a in sto if a not in dto]},
        "subject_change": {"draft": draft.get("subject", ""), "sent": sent.get("subject", ""),
                    "changed": norm_subject(draft.get("subject")) != norm_subject(sent.get("subject"))},
    }
    if sent.get("body_source") == "snippet" or (not sent.get("body") and sent.get("snippet")):
        rep["warning"] = "sent body is only the snippet; diff is partial"
    return rep


# ---------------------------------------------------------------- matching
def dedupe_drafts(drafts):
    """Same draftId logged more than once: keep the latest save."""
    by_id, out = {}, []
    for d in drafts:
        did = d.get("draftId")
        if did:
            prev = by_id.get(did)
            if prev is None or (d["_saved"] or dt.datetime.min.replace(tzinfo=dt.timezone.utc)) >= (prev["_saved"] or dt.datetime.min.replace(tzinfo=dt.timezone.utc)):
                if prev is not None:
                    out.remove(prev)
                by_id[did] = d
                out.append(d)
        else:
            out.append(d)
    return out


def in_window(sent_t, saved_t, window_days, slack_min):
    if saved_t is None or sent_t is None:
        return False
    return saved_t - dt.timedelta(minutes=slack_min) <= sent_t <= saved_t + dt.timedelta(days=window_days)


def match_all(drafts, sent, window_days=WINDOW_DAYS, slack_min=SLACK_MINUTES):
    used = set()
    pairs = []
    order = sorted(range(len(drafts)), key=lambda i: drafts[i]["_saved"] or dt.datetime.max.replace(tzinfo=dt.timezone.utc))
    for i in order:
        d = drafts[i]
        dwords = clean(*body_of(d))["words"]
        best, how = None, None
        if d.get("threadId"):
            cands = [m for m in sent if m["_key"] not in used and m.get("threadId") == d["threadId"]
                     and in_window(m["_date"], d["_saved"], window_days, slack_min)]
            if cands:
                best = max(cands, key=lambda m: (similarity(dwords, clean(*body_of(m))["words"]),
                                                 -m["_date"].timestamp()))
                how = "threadId"
        if best is None:
            dto = set(addresses(d.get("to"), d.get("cc")))
            dsub = norm_subject(d.get("subject"))
            cands = [m for m in sent if m["_key"] not in used and dto & set(addresses(m.get("to"), m.get("cc")))
                     and norm_subject(m.get("subject")) == dsub and in_window(m["_date"], d["_saved"], window_days, slack_min)]
            if cands:
                best = max(cands, key=lambda m: (similarity(dwords, clean(*body_of(m))["words"]),
                                                 -m["_date"].timestamp()))
                how = "recipient+subject"
        if best is not None:
            used.add(best["_key"])
        pairs.append((d, best, how))
    return pairs


def open_draft_index(open_drafts):
    ids, threads, keys = set(), set(), set()
    for o in open_drafts:
        if o.get("draftId"):
            ids.add(o["draftId"])
        if o.get("threadId"):
            threads.add(o["threadId"])
        for a in addresses(o.get("to"), o.get("cc")):
            keys.add((a, norm_subject(o.get("subject"))))
    return ids, threads, keys


def still_open(d, idx):
    ids, threads, keys = idx
    if d.get("draftId") and d["draftId"] in ids:
        return True
    if d.get("threadId") and d["threadId"] in threads:
        return True
    return any((a, norm_subject(d.get("subject"))) in keys for a in addresses(d.get("to"), d.get("cc")))


# ---------------------------------------------------------------- phrases
def ngrams(words, n):
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


def phrase_counts(results, top=15):
    """Counts across pairs (each pair counts a phrase once): whole changed chunks and 1-3 word n-grams."""
    chunks = {"removed": collections.Counter(), "added": collections.Counter()}
    grams = {"removed": collections.Counter(), "added": collections.Counter()}
    for r in results:
        if r.get("classification") not in ("light_edit", "heavy_edit"):
            continue
        seen = {"removed": set(), "added": set(), "g_removed": set(), "g_added": set()}
        for op in r["word_diff"]:
            for side in ("removed", "added"):
                txt = norm_phrase(op[side])
                if not txt:
                    continue
                if len(txt.split()) <= 12 and txt not in seen[side]:
                    seen[side].add(txt)
                    chunks[side][txt] += 1
                w = txt.split()
                for n in (1, 2, 3):
                    for g in ngrams(w, n):
                        g = norm_phrase(g)
                        if not g or all(x in STOP for x in g.split()) or (n == 1 and len(g) < 3):
                            continue
                        if g not in seen["g_" + side]:
                            seen["g_" + side].add(g)
                            grams[side][g] += 1
    def top_list(c):
        return [{"phrase": p, "pairs": n} for p, n in c.most_common(top)]
    return {"chunks_removed": top_list(chunks["removed"]), "chunks_added": top_list(chunks["added"]),
            "ngrams_removed": top_list(grams["removed"]), "ngrams_added": top_list(grams["added"])}


# ---------------------------------------------------------------- run
def run(drafts, sent, open_drafts=None, now=None, window_days=WINDOW_DAYS, light=LIGHT_THRESHOLD,
        rewrite=REWRITE_THRESHOLD, slack_min=SLACK_MINUTES):
    now = now or dt.datetime.now(dt.timezone.utc)
    for i, d in enumerate(drafts):
        d["_saved"] = parse_time(d.get("saved") or d.get("date"), "(draft %s)" % (d.get("draftId") or i))
        if d["_saved"] is None:
            raise InputError("draft %s has no saved date" % (d.get("draftId") or d.get("subject") or i))
    drafts = dedupe_drafts(drafts)
    sent = [m for m in sent if "DRAFT" not in (m.get("labelIds") or m.get("labels") or [])]
    for i, m in enumerate(sent):
        m["_date"] = parse_time(m.get("date"), "(sent %s)" % m.get("id"))
        m["_key"] = m.get("id") or ("idx%d" % i)
    idx = open_draft_index(open_drafts or [])
    results = []
    for d, m, how in match_all(drafts, sent, window_days, slack_min):
        base = {"account": d.get("account"), "draftId": d.get("draftId"), "threadId": d.get("threadId"),
                "to": d.get("to"), "subject": d.get("subject"), "saved": fmt_ct(d["_saved"]),
                "source": d.get("source", "gmail_draft")}
        if m is None:
            window_over = now >= d["_saved"] + dt.timedelta(days=window_days)
            is_open = still_open(d, idx) if open_drafts is not None else None
            if is_open and not window_over:
                reason = "pending"
            elif is_open:
                reason = "still_in_drafts"
            elif is_open is False:
                reason = "deleted"
            else:
                reason = "unknown" if window_over else "pending"
            base.update({"classification": "never_sent", "never_sent_reason": reason, "matched_by": None,
                         "sent_id": None})
        else:
            base.update({"matched_by": how, "sent_id": m.get("id"), "sent_threadId": m.get("threadId"),
                         "sent_date": fmt_ct(m["_date"]), "sent_account": m.get("account"),
                         "hours_to_send": round((m["_date"] - d["_saved"]).total_seconds() / 3600.0, 1)})
            base.update(compare(d, m, light))
            if base["similarity"] < rewrite:
                base["doubtful_match"] = "similarity %.2f < %.2f: may be a fresh reply, not an edit of this draft" % (
                    base["similarity"], rewrite)
            if how == "threadId" and base["subject_change"]["changed"] is False and base["recipients"]["removed"] and not base["recipients"]["sent"]:
                base["doubtful_match"] = "no recipient overlap"
        results.append(base)
    counts = collections.Counter(r["classification"] for r in results)
    reasons = collections.Counter(r.get("never_sent_reason") for r in results if r["classification"] == "never_sent")
    changes = counts["light_edit"] + counts["heavy_edit"] + sum(n for k, n in reasons.items() if k != "pending")
    report = {
        "generated": fmt_ct(now),
        "settings": {"window_days": window_days, "light_threshold": light, "rewrite_threshold": rewrite,
                     "slack_minutes": slack_min},
        "totals": {"drafts": len(results), "matched": sum(1 for r in results if r.get("sent_id")),
                   "by_class": {k: counts.get(k, 0) for k in ("sent_as_is", "light_edit", "heavy_edit", "never_sent")},
                   "never_sent_reasons": dict(reasons), "changes": changes},
        "patterns": patterns(results),
        "phrases": phrase_counts(results),
        "pairs": results,
    }
    return report


def patterns(results):
    m = [r for r in results if r.get("sent_id")]
    if not m:
        return {}
    def n(f):
        return sum(1 for r in m if f(r))
    return {
        "matched_pairs": len(m),
        "avg_similarity": round(sum(r["similarity"] for r in m) / len(m), 3),
        "avg_word_change": round(sum(r["word_count"]["change"] for r in m) / len(m), 1),
        "shorter": n(lambda r: r["word_count"]["change"] < 0),
        "longer": n(lambda r: r["word_count"]["change"] > 0),
        "opening_changed": n(lambda r: r["opening"]["opening_changed"]),
        "greeting_changed": n(lambda r: r["opening"]["greeting_changed"]),
        "signoff_changed": n(lambda r: r["signoff"]["changed"]),
        "recipients_changed": n(lambda r: r["recipients"]["removed"] or r["recipients"]["added"]),
        "subject_changed": n(lambda r: r["subject_change"]["changed"]),
        "numbers_or_prices_added": n(lambda r: any(re.search(r"\$\d|\d+\s*%|\d+\s*(mins?|minutes|x/wk|months?)|https?://", op["added"])
                                                    and not re.search(r"\$\d|https?://", op["removed"]) for op in r["word_diff"])),
        "questions_added": n(lambda r: any("?" in s for s in r["opening"]["sentences_added"])),
        "doubtful_matches": n(lambda r: r.get("doubtful_match")),
    }


def text_summary(rep, max_diff=600):
    t = rep["totals"]
    L = ["draft_vs_sent: %d drafts, %d matched | sent_as_is %d, light_edit %d, heavy_edit %d, never_sent %d"
         % (t["drafts"], t["matched"], t["by_class"]["sent_as_is"], t["by_class"]["light_edit"],
            t["by_class"]["heavy_edit"], t["by_class"]["never_sent"])]
    if t["never_sent_reasons"]:
        L.append("never_sent reasons: " + ", ".join("%s %d" % kv for kv in sorted(t["never_sent_reasons"].items())))
    p = rep["patterns"]
    if p:
        L.append("Patterns: avg similarity %.2f, avg word change %+.1f (%d shorter, %d longer); opening changed %d, "
                 "greeting changed %d, sign-off changed %d, recipients changed %d, numbers/prices/links added %d, "
                 "doubtful matches %d" % (p["avg_similarity"], p["avg_word_change"], p["shorter"], p["longer"],
                                          p["opening_changed"], p["greeting_changed"], p["signoff_changed"],
                                          p["recipients_changed"], p["numbers_or_prices_added"], p["doubtful_matches"]))
    ph = rep["phrases"]
    for k, label in (("chunks_removed", "Cut most"), ("chunks_added", "Added most")):
        items = [x for x in ph[k] if x["pairs"] >= 2][:8] or ph[k][:5]
        if items:
            L.append("%s: %s" % (label, "; ".join('"%s" x%d' % (x["phrase"], x["pairs"]) for x in items)))
    for k, label in (("ngrams_removed", "Words cut in 2+ drafts"), ("ngrams_added", "Words added in 2+ drafts")):
        items = [x for x in ph[k] if x["pairs"] >= 2][:12]
        if items:
            L.append("%s: %s" % (label, ", ".join('"%s" x%d' % (x["phrase"], x["pairs"]) for x in items)))
    L.append("")
    for r in rep["pairs"]:
        head = "- [%s] %s | %s | saved %s" % (r["classification"], r.get("subject"), _short_to(r.get("to")), r["saved"])
        if r.get("sent_id"):
            head += " | sent %s (%s, sim %.2f, words %+d)" % (r["sent_date"], r["matched_by"], r["similarity"],
                                                             r["word_count"]["change"])
        else:
            head += " | %s" % r["never_sent_reason"]
        L.append(head)
        if r.get("doubtful_match"):
            L.append("    DOUBTFUL: " + r["doubtful_match"])
        if r.get("warning"):
            L.append("    WARNING: " + r["warning"])
        if r["classification"] in ("light_edit", "heavy_edit"):
            o = r["opening"]
            if o["greeting_changed"]:
                L.append('    greeting: "%s" -> "%s"' % (o["greeting_draft"], o["greeting_sent"]))
            if o["opening_removed"]:
                L.append('    opening removed: "%s"' % " ".join(o["opening_removed"])[:200])
            if o["opening_added"]:
                L.append('    opening added: "%s"' % " ".join(o["opening_added"])[:200])
            if r["signoff"]["changed"]:
                L.append('    sign-off: "%s" -> "%s"' % (r["signoff"]["draft"], r["signoff"]["sent"]))
            if r["recipients"]["removed"] or r["recipients"]["added"]:
                L.append("    recipients: removed %s, added %s" % (r["recipients"]["removed"], r["recipients"]["added"]))
            d = r["word_diff_inline"]
            L.append("    diff: " + (d if len(d) <= max_diff else d[:max_diff] + " ..."))
    return "\n".join(L)


def _short_to(to):
    a = addresses(to)
    return ", ".join(a) if a else (to or "")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare Penny's saved Gmail drafts with what Ryne sent (read-only).")
    ap.add_argument("--drafts", action="append", help="drafts JSON/JSONL (repeatable). Default: %s" % DEFAULT_LOG)
    ap.add_argument("--sent", action="append", required=True, help="sent-mail JSON (search_emails/read_email output; repeatable)")
    ap.add_argument("--open-drafts", action="append", help="current list_drafts output (repeatable); tells deleted from still open")
    ap.add_argument("--now", help="reference time (default: now), e.g. '2026-10-23 10:30 CT' or ISO")
    ap.add_argument("--window-days", type=float, default=WINDOW_DAYS)
    ap.add_argument("--light-threshold", type=float, default=LIGHT_THRESHOLD)
    ap.add_argument("--rewrite-threshold", type=float, default=REWRITE_THRESHOLD)
    ap.add_argument("--slack-minutes", type=float, default=SLACK_MINUTES)
    ap.add_argument("--format", choices=("json", "text"), default="json", help="stdout format")
    ap.add_argument("--out", help="also write the full JSON report here")
    a = ap.parse_args(argv)
    try:
        drafts = load_records(a.drafts or [DEFAULT_LOG], ("drafts", "messages"))
        sent = load_records(a.sent, ("messages", "sent"))
        open_d = load_records(a.open_drafts, ("drafts", "messages")) if a.open_drafts else None
        now = parse_time(a.now, "(--now)") if a.now else None
        if not 0 < a.light_threshold <= 1 or not 0 <= a.rewrite_threshold <= 1 or a.window_days <= 0:
            raise InputError("thresholds must be in (0,1] and window-days > 0")
        rep = run(drafts, sent, open_d, now, a.window_days, a.light_threshold, a.rewrite_threshold, a.slack_minutes)
    except InputError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=1, ensure_ascii=False)
    if a.format == "text":
        print(text_summary(rep))
    else:
        print(json.dumps(rep, indent=1, ensure_ascii=False))
    return 1 if rep["totals"]["changes"] else 0


if __name__ == "__main__":
    sys.exit(main())
