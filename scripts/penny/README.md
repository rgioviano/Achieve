# Penny scripts

## inbox_triage.py (inbox first pass, Ryne approved 2026-10-23 via Chief)
Read-only. Python 3 standard library only. **Sorts only**: it calls no API, never reads Gmail itself, and never
labels, archives, marks, moves or deletes anything. Penny pulls mail read-only with her Gmail connectors, saves the
JSON, runs this, then does the judgment work (reading, drafting, archiving) herself.

```
python3 /home/box/agent-data/shared/scripts/penny/inbox_triage.py pull_work.json pull_contact.json            # JSON by bucket
python3 /home/box/agent-data/shared/scripts/penny/inbox_triage.py --format text pull_*.json                   # readable summary
python3 /home/box/agent-data/shared/scripts/penny/inbox_triage.py --account work page1.txt page2.txt --out triage.json
python3 /home/box/agent-data/shared/scripts/penny/inbox_triage.py --rules my_rules.json pull.json              # other rules file
```
Exit codes: 0 nothing to act on, 1 items in an actionable bucket (lead_form, payment_alert, client_reply, scheduling,
security_alert; set by `actionable_buckets`), 2 error (bad input or rules: report it, do not guess).

### Input
A JSON list of messages, `{"messages": [...]}` (an `"account"` at the top applies to all its messages), or the
search_emails connector output saved with `write_to_file` (wrapper text before the first `{`/`[` is ignored).
Several files can be passed. Per message: `id`, `threadId`, `from` (or `sender`), `to`, `subject`, `date`,
`snippet` and/or `body` (body wins), `labelIds` (or `labels`), optional `account` (work, contact, personal,
ironblueprint). `--account` fills messages that have none. Snippets are enough; it was tested on snippets only.

### Output
`{"total", "by_account", "counts", "actionable", "actionable_buckets", "buckets": {bucket: [item, ...]}}`.
Each item: `id, threadId, account, from, subject, date, sender_type (self|staff|automated|human), bucket, rule, why`,
plus `scope` on payment alerts (`client_autopay`, `personal_finance`, `vendor_or_business`), `channel: trainheroic`
on TrainHeroic DMs, and `ack_only: true` on short thank-you replies with no question.

### Buckets and where the lines are
| bucket | what goes in |
|---|---|
| lead_form | WordPress "Lead Form -" (also Fw/Fwd of one), Yelp lead messages, a NEW person asking about training (not a reply), staff forwards of an inquiry. Hand to Tally. A lead writing back in a thread is client_reply or scheduling, not lead_form. |
| payment_alert | Mindbody "Automatic Payment ... Has Failed" (scope client_autopay). Personal-finance warnings in the personal account (scope personal_finance, account personal). Vendor payment failures. AutoPay *success* and "payment scheduled" reminders are fyi. |
| client_reply | A parent/client/lead writing to Ryne or staff: holds, pauses, plan/frequency changes, renewals, pricing, payment/card/pass/account problems, injuries, paperwork questions, general replies, thank-yous (ack_only), staff forwards of a client message, TrainHeroic athlete DMs. **If a message has a booking AND an account/payment/plan/health issue, it is client_reply.** |
| scheduling | Only a time: eval request/confirm, reschedule, switch time, cancel or no-show a session, waitlist, availability, calendar Accepted/Declined. |
| security_alert | Suspicious login, new sign-in, Takeout, password reset, codes, MFA, new device, new app connected, owner invites/ownership transfer, vulnerability notices. |
| fyi_notification | Receipts, orders, bank/vendor notices, Mindbody copies, porting status, Ryne's own mail, student observation requests (low priority, never client_reply). |
| promo_junk | Newsletters, marketing, Gmail Promotions, cold sales pitches (incl. fake "Re:" pitches). |
| unknown | Staff notes, vendor support tickets, Numa text relays, personal-account mail from people, anything no rule matched. Read by hand. |

### Rules file (`inbox_triage_rules.json`, loaded by default)
Top level: `bucket_order` (output order), `actionable_buckets` (drive exit 1), `self_addresses` (Ryne; never
client_reply), `staff_addresses` / `staff_domains`, `automated_from_re` (senders that are systems, not people),
`quote_markers_re` (where the new text of a reply ends), `ack_re` / `ack_max_words`, and `rules`.
`rules` are tried **top to bottom; the first match wins**. Every condition in a rule must hold (AND); inside a list,
any entry may match (OR). Fields:
- `id`, `bucket`, `why` (shown in output), `set` (extra fields copied to the item)
- `sender`: list of `self`, `staff`, `automated`, `human`
- `from_re` / `from_not_re`: regex on the From header (lowercased)
- `subject_re` / `subject_not_re`
- `text_re` / `text_all_re` (all must match) / `text_not_re`: on subject + the NEW part of the body/snippet
- `raw_re` / `raw_not_re`: on subject + the whole body/snippet including quoted text
- `is_reply` (subject starts Re:), `is_forward` (Fw:/Fwd:), `labels_any`, `account_any`
Regexes are case-insensitive Python regexes (escape backslashes in JSON). After any edit run the tests.
To add a new cold-pitch sender: add its domain to `pitch_senders`. A new staff member: `staff_addresses`.

### Tests
`python3 -m unittest /home/box/agent-data/shared/scripts/penny/test_inbox_triage.py -v` (48 cases, anonymized
copies of real patterns: every bucket, Ryne's own mail, staff-forwarded leads, AutoPay success vs failure, personal
finance warning, fake-Re pitches, student requests, quote-cutting and comcast.net regressions, CLI exit codes 0/1/2).

### Real-mail check (2026-10-23)
Hand-checked every message, read-only pulls of work + contact (`-in:sent -in:drafts`, archived mail included):
10/16-10/23: 177 (work 141, contact 36); held-out 10/9-10/16: 169 (work 120, contact 49). Final run: 346/346 match
the hand labels, 0 misfiles in lead_form / payment_alert / client_reply. Work files: `/workspace/inbox_triage_test/`
(`handcheck.csv`, pulls, `score.py`). Rules are tuned on this mail, so watch the unknown bucket and fix rules as
new senders show up.

### How Penny calls it (proposal, not yet in any routine; Chief reviews first)
See the report to Chief of 2026-10-23. Summary: pull each account with search_emails (idsOnly false, maxResults 25,
page to the end, write_to_file), run the script on the saved files with `--out`, then act per bucket.

## draft_vs_sent.py (learn how Ryne edits Penny's drafts, Ryne approved 2026-10-23 via Chief)
Read-only. Python 3 standard library only. It calls no API and never sends, edits or deletes a draft or an email.
Penny logs each draft she saves, pulls Sent mail (and the current Drafts list) read-only with her Gmail connectors,
saves the JSON, then runs this.

```
python3 /home/box/agent-data/shared/scripts/penny/draft_vs_sent.py \
  --drafts /home/box/agent-data/penny/draft-log.jsonl \
  --sent sent_work.json --sent sent_contact.json \
  --open-drafts drafts_work.json --open-drafts drafts_contact.json \
  --now "2026-10-30 07:00 CT" --format text --out /home/box/agent-data/penny/draft-vs-sent/2026-10-30.json
```
Exit codes: 0 = no changes (every matched draft was sent as is and nothing is finally never_sent), 1 = changes found,
2 = error (bad or missing input, bad date, bad threshold: report it, do not guess).

### Inputs
- `--drafts` (repeatable; default the draft log): JSON list, `{"drafts": [...]}`, or JSONL. Per draft: `account`,
  `draftId`, `threadId` (null for a new email), `to` (and optional `cc`), `subject`, `saved` (`"YYYY-MM-DD HH:MM CT"`
  or ISO with offset), `body` (plain text; `htmlBody` is used if there is no body). Optional `source`, `provenance`.
  The same `draftId` logged twice keeps only the latest save (Penny's rewrite replaces her earlier version).
- `--sent` (repeatable, required): search_emails / read_email output (`{"messages": [...]}`, a list, or the connector
  text saved with `write_to_file`). Per message: `id`, `threadId`, `to`, `cc`, `subject`, `date`, `body` (read_email)
  or only `snippet`. Messages labelled DRAFT are ignored. A snippet-only match gets a `warning` (partial diff).
- `--open-drafts` (repeatable, optional): list_drafts output. It tells a deleted draft from one still sitting in Drafts.
  Matched by draftId, threadId, or recipient + normalized subject (Gmail gives an opened draft a new `s:` id).

### Matching
Drafts are processed oldest first. Each sent message can match one draft only.
1. **threadId**: a sent message in the draft's thread dated from `saved - 10 min` (`--slack-minutes`) to
   `saved + 3 days` (`--window-days`). If several qualify, the most similar wins.
2. **Fallback**: at least one shared recipient (To/Cc, case-insensitive) **and** the same normalized subject
   (Re:/Fwd:/[EXTERNAL] stripped, curly quotes, case and spacing ignored), in the same window.

### Cleaning before comparing (both sides)
CRLF to LF, HTML to text, quoted reply text cut (`On ... wrote:` even when wrapped, `>` lines, `-----Original
Message-----`, Outlook `From:` + `Sent:` headers), **signature block cut** from the `Ryne Gioviano, MSEd` line or a
`-- ` line down (so a typed signature, a Gmail-added one, a tracking-link one or none all compare equal), curly quotes
straightened, whitespace collapsed. The greeting stays in the words; the sign-off (`Thanks,`, `Thanks!`, `See you at 5!`,
...) is split off and compared on its own.

### Classification
`similarity` = difflib ratio on the cleaned word lists (2 x matching words / total words, 0..1).

| class | rule |
|---|---|
| sent_as_is | cleaned words identical and the same sign-off |
| light_edit | similarity >= 0.85 (`--light-threshold`), or the words are identical and only the sign-off changed |
| heavy_edit | similarity < 0.85 |
| never_sent | no match. `never_sent_reason`: `deleted` (not in the open-drafts list), `still_in_drafts` (still open after the 3-day window), `pending` (window not over yet: **not counted as a change**), `unknown` (no `--open-drafts` given and the window is over) |

A pair with similarity < 0.40 (`--rewrite-threshold`) gets `doubtful_match`: Ryne probably wrote a fresh reply in
the thread instead of editing the draft. Read those by hand before learning from them.
For scale: one or two words changed in a 70-word email is about 0.95+. Rewriting one or two sentences is about 0.80 (Tara 0.82, Britt 0.81, Beth 0.79 on 10/22-23). A rewrite that keeps only
the greeting and a few phrases is below 0.30.

### Output (`--out` JSON, stdout JSON or `--format text`)
`totals` (drafts, matched, by_class, never_sent_reasons, changes), `patterns` (avg similarity and word change,
shorter or longer, opening, greeting, sign-off, recipient and subject changes, numbers/prices/links added, questions added,
doubtful matches), `phrases` (changed chunks and 1 to 3 word n-grams Ryne cut or added, counted **once per pair** across
all pairs, stopword-only n-grams dropped), and `pairs`. Each pair has: account, draftId, threadId, to, subject,
saved, source, matched_by, sent_id, sent_date, hours_to_send, classification, similarity, `word_count`
{draft, sent, change, change_pct}, `word_diff` (ops: removed/added), `word_diff_inline` (`[-cut-] {+added+}`),
`opening` (greeting before/after, first sentence before/after, `opening_removed`/`opening_added` = leading
sentences that disappeared/appeared, `sentences_removed`/`sentences_added` anywhere), `signoff` (before/after,
changed, signature present on each side), `recipients` (removed/added), `subject_change`.

### Tests
`python3 -m unittest /home/box/agent-data/shared/scripts/penny/test_draft_vs_sent.py -v` (46 cases, anonymized
example.com data): parsing (CT and UTC dates, JSON/JSONL/connector text), quote stripping, signature equality,
HTML, every class and threshold, the thread-first and fallback matches, the 3-day window, sent-before-save,
one-use sent, DRAFT labels, dedupe, every never_sent reason, phrase counts, and exit codes 0/1/2.

### First real run (2026-10-23)
Data in /workspace/draft_vs_sent_test/: `drafts_since_1021.json` (9 Gmail drafts rebuilt from the draft log,
get_draft and Penny's pre_draft_check files, each with its `provenance`), `cards_since_1021.json` (2 chat cards from 10/21),
`sent_since_1021.json` (26 sent: work 25, contact 1; 10 read in full), `open_drafts_*.json`, `results*.json`,
`summary*.txt`.
