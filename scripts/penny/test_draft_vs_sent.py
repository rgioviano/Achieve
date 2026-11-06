#!/usr/bin/env python3
"""Unit tests for draft_vs_sent.py (anonymized example.com data). Run:
python3 -m unittest /home/box/agent-data/shared/scripts/penny/test_draft_vs_sent.py -v
"""
import contextlib, io, json, os, sys, tempfile, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draft_vs_sent as dvs  # noqa: E402


def write(path, text):
    with open(path, "w") as fh:
        fh.write(text)

SIG = ("Coach Pat, MSEd, CSCS\nOwner, Example Performance\nwww.example.com\n\n"
       "For scheduling or account questions:\nfront@example.com | Text: 555-01-0001\n")
# the script keys the signature on Ryne's name line; tests use the real first line pattern
RSIG = "Ryne Gioviano, MSEd, CSCS\nOwner, Example Performance\nwww.example.com\n\nFor scheduling or account questions:\nfront@example.com | Text: 555-01-0001\n"
NOW = "2026-10-30 12:00 CT"


def draft(body, **k):
    d = {"account": "work", "draftId": k.pop("draftId", "r1"), "threadId": k.pop("threadId", "t1"),
         "to": k.pop("to", "Alex Parent <alex@example.com>"), "subject": k.pop("subject", "Re: Training"),
         "saved": k.pop("saved", "2026-10-22 15:00 CT"), "body": body}
    d.update(k)
    return d


def sent(body, **k):
    m = {"id": k.pop("id", "m1"), "threadId": k.pop("threadId", "t1"), "from": "Coach <coach@example.com>",
         "to": k.pop("to", "Alex Parent <alex@example.com>"), "subject": k.pop("subject", "Re: Training"),
         "date": k.pop("date", "2026-10-22T22:00:00Z"), "labelIds": k.pop("labelIds", ["SENT"]), "body": body}
    m.update(k)
    return m


BASE = ("Hi Alex,\n\nGreat to hear Sam is starting in November. The next step is picking a plan.\n\n"
        "Let us know which plan you want and we'll send the sign-up link.\n\nThanks,\n")


def run(drafts, sents, open_drafts=None, now=NOW, **kw):
    return dvs.run(drafts, sents, open_drafts, dvs.parse_time(now), **kw)


class Parsing(unittest.TestCase):
    def test_parse_time_ct_and_utc(self):
        a = dvs.parse_time("2026-10-22 15:00 CT")
        b = dvs.parse_time("2026-10-22T20:00:00Z")
        self.assertEqual(a, b)  # CDT is UTC-5

    def test_parse_time_bad(self):
        with self.assertRaises(dvs.InputError):
            dvs.parse_time("yesterday-ish")

    def test_norm_subject(self):
        self.assertEqual(dvs.norm_subject("RE: Fwd: [EXTERNAL] Re:  Achieve\u2019s  Program"), "achieve's program")

    def test_addresses(self):
        self.assertEqual(dvs.addresses("A <A@Example.com>, b@example.com", ["c@example.com"]),
                         ["a@example.com", "b@example.com", "c@example.com"])

    def test_load_formats(self):
        with tempfile.TemporaryDirectory() as td:
            p1 = os.path.join(td, "a.json"); write(p1, json.dumps({"account": "contact", "messages": [sent("x")]}))
            p2 = os.path.join(td, "b.jsonl"); write(p2, json.dumps(draft("y")) + "\n" + json.dumps(draft("z")) + "\n")
            p3 = os.path.join(td, "c.txt"); write(p3, "Result:\n" + json.dumps({"messages": [sent("w")]}) + "\nNote: more")
            p4 = os.path.join(td, "d.json"); write(p4, json.dumps([sent("v")]))
            recs = dvs.load_records([p1], ("messages",))
            self.assertEqual(recs[0]["account"], "contact")
            self.assertEqual(len(dvs.load_records([p2], ("drafts",))), 2)
            self.assertEqual(len(dvs.load_records([p3], ("messages",))), 1)
            self.assertEqual(len(dvs.load_records([p4], ("messages",))), 1)

    def test_load_bad_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "bad.json"); write(p, "not json at all")
            with self.assertRaises(dvs.InputError):
                dvs.load_records([p], ("messages",))


class Cleaning(unittest.TestCase):
    def test_strip_on_wrote_and_gt(self):
        c = dvs.clean("Hi Alex,\r\n\r\nSure thing.\r\n\r\nThanks,\r\nOn Oct 22, 2026 at 09:55 -0500, Alex <alex@example.com>, wrote:\r\n> old text\r\n")
        self.assertEqual(c["words"], ["Hi", "Alex,", "Sure", "thing."])
        self.assertEqual(c["signoff"], "Thanks,")

    def test_strip_wrapped_on_wrote(self):
        c = dvs.clean("Hi Alex,\n\nOk.\n\nOn Sat, Sep 26, 2026 10:04 PM, Coach\n<coach@example.com> wrote:\nold")
        self.assertNotIn("old", c["words"])

    def test_strip_outlook_header(self):
        c = dvs.clean("Ok, see you then.\n\nFrom: Alex <alex@example.com>\nSent: Tuesday\nSubject: x\nold stuff")
        self.assertNotIn("stuff", c["words"])

    def test_from_line_without_sent_is_kept(self):
        c = dvs.clean("Hi Alex,\n\nFrom: what we saw, he is ready.\n\nThanks,")
        self.assertIn("ready.", c["words"])

    def test_signature_typed_equals_gmail_added(self):
        typed = dvs.clean("Hi Alex,\n\nSee you Monday.\n\nThanks,\n\n" + RSIG)
        gmail = dvs.clean("Hi Alex,\n\nSee you Monday.\n\nThanks,\n\n-- \nRyne Gioviano, MSEd, CSCS\nOwner\n")
        none = dvs.clean("Hi Alex,\n\nSee you Monday.\n\nThanks,\n")
        self.assertEqual(typed["words"], gmail["words"])
        self.assertEqual(typed["words"], none["words"])
        self.assertTrue(typed["has_signature"])
        self.assertFalse(none["has_signature"])

    def test_tracking_link_signature(self):
        c = dvs.clean("Hi Alex,\n\nOk.\n\nRyne Gioviano, MSEd, CSCS\nOwner https://www.google.com/url?q=http://www.example.com\n")
        self.assertEqual(c["words"], ["Hi", "Alex,", "Ok."])

    def test_html_body(self):
        c = dvs.clean("<div>Hi Alex,</div><div><br></div><div>Ok &amp; done.</div><div><br></div><div>Thanks,</div>", True)
        self.assertEqual(c["words"], ["Hi", "Alex,", "Ok", "&", "done."])
        self.assertEqual(c["signoff"], "Thanks,")

    def test_curly_quotes_and_whitespace(self):
        a = dvs.clean("Hi Alex,\n\nWe\u2019ll   see\n you.\n")
        b = dvs.clean("Hi Alex,\r\n\r\nWe'll see you.\r\n")
        self.assertEqual(a["words"], b["words"])

    def test_greeting_glued_to_text(self):
        c = dvs.clean("Hi Alex, sounds good to me.")
        self.assertEqual(c["greeting"], "Hi Alex,")


class Classify(unittest.TestCase):
    def test_sent_as_is_ignores_signature_and_crlf(self):
        r = run([draft(BASE)], [sent(BASE.replace("\n", "\r\n") + "\r\n\r\n" + RSIG)])
        p = r["pairs"][0]
        self.assertEqual(p["classification"], "sent_as_is")
        self.assertEqual(p["similarity"], 1.0)
        self.assertEqual(r["totals"]["changes"], 0)

    def test_signoff_only_is_light(self):
        r = run([draft(BASE)], [sent(BASE.replace("Thanks,", "Thanks!"))])
        p = r["pairs"][0]
        self.assertEqual(p["classification"], "light_edit")
        self.assertTrue(p["signoff"]["changed"])

    def test_light_edit(self):
        r = run([draft(BASE)], [sent(BASE.replace("picking a plan", "picking a training plan"))])
        p = r["pairs"][0]
        self.assertEqual(p["classification"], "light_edit")
        self.assertGreaterEqual(p["similarity"], 0.85)
        self.assertEqual(p["word_count"]["change"], 1)
        self.assertEqual(p["word_diff"], [{"op": "insert", "removed": "", "added": "training"}])
        self.assertIn("{+training+}", p["word_diff_inline"])

    def test_heavy_edit_and_doubtful(self):
        other = "Hi Alex,\n\nCall me tomorrow about the invoice, there is a problem with the card.\n\nThanks,\n"
        p = run([draft(BASE)], [sent(other)])["pairs"][0]
        self.assertEqual(p["classification"], "heavy_edit")
        self.assertIn("doubtful_match", p)

    def test_threshold_is_configurable(self):
        edited = BASE.replace("The next step is picking a plan.", "Sam will love it here, and his friends train here too.")
        a = run([draft(BASE)], [sent(edited)])["pairs"][0]
        self.assertLess(a["similarity"], 0.85)
        b = run([draft(BASE)], [sent(edited)], light=a["similarity"] - 0.01)["pairs"][0]
        self.assertEqual(a["classification"], "heavy_edit")
        self.assertEqual(b["classification"], "light_edit")

    def test_opening_and_greeting(self):
        new = BASE.replace("Hi Alex,", "Hi Alex and Jo,").replace(
            "Great to hear Sam is starting in November.", "I know we talked a while ago. Great to hear Sam is starting in November.")
        p = run([draft(BASE)], [sent(new)])["pairs"][0]
        o = p["opening"]
        self.assertTrue(o["greeting_changed"])
        self.assertEqual(o["opening_added"], ["I know we talked a while ago."])
        self.assertEqual(o["opening_removed"], [])
        self.assertTrue(o["opening_changed"])

    def test_opening_removed(self):
        new = BASE.replace("Great to hear Sam is starting in November. ", "")
        o = run([draft(BASE)], [sent(new)])["pairs"][0]["opening"]
        self.assertEqual(o["opening_removed"], ["Great to hear Sam is starting in November."])

    def test_recipient_removed(self):
        d = draft(BASE, to="Alex <alex@example.com>, Jo <jo@example.com>")
        p = run([d], [sent(BASE)])["pairs"][0]
        self.assertEqual(p["recipients"]["removed"], ["jo@example.com"])


class Matching(unittest.TestCase):
    def test_thread_match_first(self):
        s1 = sent(BASE, id="a", threadId="t1", subject="Other subject")
        s2 = sent(BASE, id="b", threadId="t9")
        p = run([draft(BASE)], [s2, s1])["pairs"][0]
        self.assertEqual((p["matched_by"], p["sent_id"]), ("threadId", "a"))

    def test_thread_picks_most_similar(self):
        s1 = sent("Hi Alex,\n\nQuick note: running late.\n\nThanks,", id="a", date="2026-10-22T21:00:00Z")
        s2 = sent(BASE, id="b", date="2026-10-22T23:00:00Z")
        p = run([draft(BASE)], [s1, s2])["pairs"][0]
        self.assertEqual(p["sent_id"], "b")

    def test_fallback_recipient_subject(self):
        d = draft(BASE, threadId=None, subject="Training at Example")
        s = sent(BASE, threadId="new1", subject="Re: training at  example", to="alex@EXAMPLE.com")
        p = run([d], [s])["pairs"][0]
        self.assertEqual(p["matched_by"], "recipient+subject")

    def test_fallback_needs_same_subject(self):
        d = draft(BASE, threadId=None, subject="Training at Example")
        s = sent(BASE, threadId="new1", subject="Something else")
        self.assertEqual(run([d], [s], open_drafts=[])["pairs"][0]["classification"], "never_sent")

    def test_window_three_days(self):
        late = sent(BASE, date="2026-10-26T21:00:00Z")      # 4 days after the save
        p = run([draft(BASE)], [late], open_drafts=[])["pairs"][0]
        self.assertEqual(p["classification"], "never_sent")
        ok = sent(BASE, date="2026-10-25T19:00:00Z")        # inside 3 days
        self.assertEqual(run([draft(BASE)], [ok])["pairs"][0]["classification"], "sent_as_is")

    def test_sent_before_save_is_ignored(self):
        early = sent(BASE, date="2026-10-21T15:00:00Z")
        p = run([draft(BASE)], [early], open_drafts=[])["pairs"][0]
        self.assertIsNone(p["sent_id"])

    def test_sent_used_once(self):
        d1 = draft(BASE, draftId="r1", saved="2026-10-22 15:00 CT")
        d2 = draft(BASE, draftId="r2", saved="2026-10-22 15:05 CT")
        r = run([d1, d2], [sent(BASE)], open_drafts=[])
        ids = [p["sent_id"] for p in r["pairs"]]
        self.assertEqual(ids.count("m1"), 1)
        self.assertIn(None, ids)

    def test_draft_labels_in_sent_list_ignored(self):
        p = run([draft(BASE)], [sent(BASE, labelIds=["DRAFT"])], open_drafts=[])["pairs"][0]
        self.assertEqual(p["classification"], "never_sent")

    def test_dedupe_keeps_latest_save(self):
        old = draft("Hi Alex,\n\nOld version.\n\nThanks,", saved="2026-10-22 10:00 CT")
        new = draft(BASE, saved="2026-10-22 15:00 CT")
        r = run([old, new], [sent(BASE)])
        self.assertEqual(r["totals"]["drafts"], 1)
        self.assertEqual(r["pairs"][0]["classification"], "sent_as_is")

    def test_missing_saved_is_error(self):
        d = draft(BASE); d["saved"] = ""
        with self.assertRaises(dvs.InputError):
            run([d], [])


class NeverSent(unittest.TestCase):
    def test_deleted(self):
        p = run([draft(BASE)], [], open_drafts=[])["pairs"][0]
        self.assertEqual(p["never_sent_reason"], "deleted")

    def test_still_in_drafts_after_window(self):
        p = run([draft(BASE)], [], open_drafts=[{"draftId": "r1"}])["pairs"][0]
        self.assertEqual(p["never_sent_reason"], "still_in_drafts")

    def test_pending_inside_window_is_not_a_change(self):
        r = run([draft(BASE)], [], open_drafts=[{"draftId": "rX", "threadId": "t1"}], now="2026-10-23 09:00 CT")
        self.assertEqual(r["pairs"][0]["never_sent_reason"], "pending")
        self.assertEqual(r["totals"]["changes"], 0)

    def test_open_draft_matched_by_recipient_subject(self):
        od = [{"draftId": "s:999", "to": "alex@example.com", "subject": "Re: Training"}]
        d = draft(BASE, threadId=None)
        self.assertEqual(run([d], [], open_drafts=od)["pairs"][0]["never_sent_reason"], "still_in_drafts")

    def test_unknown_without_open_list(self):
        self.assertEqual(run([draft(BASE)], [])["pairs"][0]["never_sent_reason"], "unknown")


class Phrases(unittest.TestCase):
    def test_counts_across_pairs(self):
        drafts, sents = [], []
        for i in range(3):
            body = "Hi Alex,\n\nThe eval takes about an hour. See the plan %d.\n\nThanks," % i
            drafts.append(draft(body, draftId="r%d" % i, threadId="t%d" % i))
            sents.append(sent(body.replace("an hour", "45 mins") + " Pricing starts at $189/mo.", id="m%d" % i, threadId="t%d" % i))
        r = run(drafts, sents)
        rem = {x["phrase"]: x["pairs"] for x in r["phrases"]["chunks_removed"]}
        self.assertEqual(rem.get("an hour"), 3)
        add = {x["phrase"]: x["pairs"] for x in r["phrases"]["ngrams_added"]}
        self.assertEqual(add.get("mins"), 3)
        self.assertEqual(r["patterns"]["numbers_or_prices_added"], 3)

    def test_stopword_ngrams_dropped(self):
        r = run([draft("Hi Alex,\n\nWe can do it.\n\nThanks,")], [sent("Hi Alex,\n\nWe can do it for you.\n\nThanks,")])
        grams = [x["phrase"] for x in r["phrases"]["ngrams_added"]]
        self.assertNotIn("for you", grams)


class Cli(unittest.TestCase):
    def _files(self, td, drafts, sents, opened=None):
        dp = os.path.join(td, "d.jsonl"); write(dp, "".join(json.dumps(d) + "\n" for d in drafts))
        sp = os.path.join(td, "s.json"); write(sp, json.dumps({"messages": sents}))
        args = ["--drafts", dp, "--sent", sp, "--now", NOW]
        if opened is not None:
            op = os.path.join(td, "o.json"); write(op, json.dumps({"drafts": opened}))
            args += ["--open-drafts", op]
        return args

    def _main(self, args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = dvs.main(args)
        return code, out.getvalue()

    def test_exit0_no_changes_and_out_file(self):
        with tempfile.TemporaryDirectory() as td:
            outp = os.path.join(td, "r.json")
            code, out = self._main(self._files(td, [draft(BASE)], [sent(BASE)]) + ["--out", outp])
            self.assertEqual(code, 0)
            with open(outp) as fh:
                self.assertEqual(json.load(fh)["totals"]["by_class"]["sent_as_is"], 1)
            self.assertEqual(json.loads(out)["totals"]["changes"], 0)

    def test_exit1_changes_text_format(self):
        with tempfile.TemporaryDirectory() as td:
            code, out = self._main(self._files(td, [draft(BASE)], [sent(BASE.replace("plan.", "plan for him."))]) + ["--format", "text"])
            self.assertEqual(code, 1)
            self.assertIn("light_edit 1", out)
            self.assertIn("diff:", out)

    def test_exit1_deleted_draft(self):
        with tempfile.TemporaryDirectory() as td:
            code, _ = self._main(self._files(td, [draft(BASE)], [], opened=[]))
            self.assertEqual(code, 1)

    def test_exit2_bad_input(self):
        with tempfile.TemporaryDirectory() as td:
            bad = os.path.join(td, "bad.json"); write(bad, "{oops")
            code, _ = self._main(["--drafts", bad, "--sent", bad])
            self.assertEqual(code, 2)

    def test_exit2_missing_file(self):
        code, _ = self._main(["--drafts", "/nonexistent/x.jsonl", "--sent", "/nonexistent/y.json"])
        self.assertEqual(code, 2)

    def test_exit2_bad_threshold(self):
        with tempfile.TemporaryDirectory() as td:
            code, _ = self._main(self._files(td, [draft(BASE)], [sent(BASE)]) + ["--light-threshold", "1.5"])
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
