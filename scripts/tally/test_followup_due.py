#!/usr/bin/env python3
"""Tests for followup_due.py. Run: python3 -m unittest /home/box/agent-data/shared/scripts/tally/test_followup_due.py -v
(or python3 test_followup_due.py). Made-up people on example.com and 555 numbers only."""
import csv, datetime as dt, io, json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import followup_due as f

HDR = ["Last Name", "First Name", "Month", "Contact Date", "Stage", "Contact Count", "Referral Source",
       "Eval?", "Sign-Up", "Sign-Up Date", "Email Address", "Phone Number", "Service Type", "Comments",
       "Last Contact", "Next Follow-Up"]
TODAY = dt.date(2026, 10, 22)


def row(last, first, stage="", cc="", email="", phone="", svc="", comments="", lc="", nf=""):
    return [last, first, "October", "10/1/26", stage, cc, "Website", "", "", "", email, phone, svc, comments, lc, nf]


def sheet():
    return [HDR,
        row("Due", "Ann", "Contacted", "1", "ann@example.com", "6305550101", "Athletic Development",
            "Parent Ann. Lead Form; son plays football; wants speed and strength.", "10/20/26", "10/22/26"),
        row("Over", "Bob", "", "3", "bob@example.com", "6305550102", "Semi-Private",
            "Wants small group strength 2x/wk.", "10/10/26", "10/15/26"),
        row("Future", "Cy", "New inquiry", "1", "cy@example.com", "", "", "x", "10/21/26", "10/23/26"),
        row("Booked", "Di", "Eval booked", "2", "di@example.com", nf="10/20/26"),
        row("Signed", "Ed", "Signed", "4", "ed@example.com", nf="10/1/26"),
        row("Park", "Flo", "PARKED", "7", "flo@example.com", nf="10/1/26"),
        row("Rep", "Gus", "Replied", "2", "gus@example.com", nf="10/2/26"),
        row("Lost", "Hal", "Lost", "2", "hal@example.com", nf="10/2/26"),
        row("NoNext", "Ivy", "", "1", "ivy@example.com"),
        row("Blank", "Cnt", "", "", "cnt@example.com", nf="10/22/26"),
        [""] * 16,
        row("Bad", "Date", "", "1", "bad@example.com", nf="soon"),
        ["AVERAGES"] + [""] * 15,
        ["", "", "", "", "", "", "", "", "October", "3", "1", "33%", "", "", "", "10/1/26"],
        row("Below", "Table", "", "1", "below@example.com", nf="10/1/26"),
    ]


class Schedule(unittest.TestCase):
    def test_next_each_step(self):
        first = dt.date(2026, 10, 1)
        want = [dt.date(2026, 10, 3), dt.date(2026, 10, 6), dt.date(2026, 10, 10),
                dt.date(2026, 10, 15), dt.date(2026, 10, 22), dt.date(2026, 10, 31)]
        for step, w in enumerate(want):
            self.assertEqual(f.next_followup(first, step), w)
        self.assertEqual(f.next_followup(first, 6), "parked")
        self.assertEqual(f.next_followup(first, 9), "parked")

    def test_string_dates_and_month_rollover(self):
        self.assertEqual(f.next_followup("10/21/26", 0), dt.date(2026, 10, 23))
        self.assertEqual(f.next_followup("10/21/2026", 5), dt.date(2026, 11, 20))
        self.assertEqual(f.next_followup("2026-12-20", 3), dt.date(2027, 1, 3))
        self.assertEqual(f.fmt_date(dt.date(2026, 11, 2)), "11/2/26")

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            f.next_followup("", 0)
        with self.assertRaises(ValueError):
            f.next_followup("10/1/26", -1)


class Stages(unittest.TestCase):
    def test_stop_words(self):
        for s in ["Replied", "replied", "Eval booked", "EVAL BOOKED", "Booked", "Signed", "signed up",
                  "Parked", "parked ", "Lead replied"]:
            self.assertTrue(f.stage_stops(s), s)
        for s in ["", "New inquiry", "Contacted", "contacted", "Hold", "No-show", "Offer", "Eval done"]:
            self.assertFalse(f.stage_stops(s), s)


class DueList(unittest.TestCase):
    def setUp(self):
        self.res = f.build(sheet(), TODAY)
        self.names = [x["name"] for x in self.res["due"]]

    def test_due_rows(self):
        self.assertEqual(self.names, ["Bob Over", "Ann Due", "Cnt Blank"])  # oldest overdue first

    def test_excluded(self):
        for n in ["Cy Future", "Di Booked", "Ed Signed", "Flo Park", "Gus Rep", "Hal Lost", "Ivy NoNext", "Table Below"]:
            self.assertNotIn(n, self.names)

    def test_fields(self):
        ann = next(x for x in self.res["due"] if x["name"] == "Ann Due")
        self.assertEqual(ann["email"], "ann@example.com")
        self.assertEqual(ann["phone"], "6305550101")
        self.assertEqual(ann["step"], 1)
        self.assertEqual(ann["step_day"], 2)
        self.assertEqual(ann["service_type"], "Athletic Development")
        self.assertNotIn("Parent", ann["asked_about"])
        self.assertIn("football", ann["asked_about"])
        self.assertEqual(ann["days_overdue"], 0)
        bob = next(x for x in self.res["due"] if x["name"] == "Bob Over")
        self.assertEqual((bob["step"], bob["step_day"], bob["days_overdue"]), (3, 9, 7))
        blank = next(x for x in self.res["due"] if x["name"] == "Cnt Blank")
        self.assertIsNone(blank["step"])

    def test_held_replied_and_bad_and_summary_stop(self):
        self.assertEqual([x["name"] for x in self.res["held_replied"]], ["Gus Rep"])
        self.assertEqual([b["name"] for b in self.res["bad_dates"]], ["Date Bad"])
        self.assertTrue(any("AVERAGES" in n for n in self.res["notes"]))


class ContactedAndParked(unittest.TestCase):
    def test_contacted_is_due_and_replied_is_not(self):
        rows = [HDR, row("C", "Con", "Contacted", "2", "con@example.com", nf="9/28/26"),
                row("R", "Rep", "Replied", "2", "rep@example.com", nf="9/28/26")]
        res = f.build(rows, TODAY)
        self.assertEqual([x["name"] for x in res["due"]], ["Con C"])
        self.assertEqual(res["due"][0]["step"], 2)
        self.assertEqual(res["due"][0]["step_day"], 5)
        self.assertEqual([x["name"] for x in res["held_replied"]], ["Rep R"])

    def test_past_day30_flagged_not_parked(self):
        rows = [HDR, row("P", "Past", "Contacted", "7", "past@example.com", nf="10/1/26")]
        res = f.build(rows, TODAY)
        self.assertIn("do not park", res["due"][0]["note"])
        self.assertEqual(f.next_followup("9/1/26", 6), "parked")  # helper logic kept

    def test_script_has_no_write_path(self):
        with open(os.path.join(HERE, "followup_due.py")) as fh:
            src = fh.read()
        for w in ("write_range", "requests", "urllib", "googleapiclient", "open(path, \"w"):
            self.assertNotIn(w, src)


class ParkedRules(unittest.TestCase):
    def test_parked_never_due(self):
        rows = [HDR, row("P", "Pk", "Parked", "7", "pk@example.com", nf="10/1/26"),
                row("Q", "Pk2", "parked (newsletter)", "7", "pk2@example.com", nf="10/1/26")]
        res = f.build(rows, TODAY)
        self.assertEqual(res["due"], [])
        self.assertEqual(res["held_replied"], [])

    def test_reply_booking_signup_take_off_parked(self):
        self.assertEqual(f.stage_after_event("Parked", "reply"), "Replied")
        self.assertEqual(f.stage_after_event("Parked", "booked"), "Eval booked")
        self.assertEqual(f.stage_after_event("PARKED", "signed"), "Signed")
        self.assertEqual(f.stage_after_event("Parked", "send"), "Parked")
        self.assertEqual(f.stage_after_event("Contacted", "reply"), "Replied")
        self.assertFalse(f.is_parked(f.stage_after_event("Parked", "reply")))

    def test_newer_stage_overrides_parked(self):
        # once the Stage cell holds a newer value, the row follows that value, not Parked
        rows = [HDR, row("N", "New", "Contacted", "2", "new@example.com", nf="10/20/26")]
        self.assertEqual([x["name"] for x in f.build(rows, TODAY)["due"]], ["New N"])

    def test_park_candidates_by_date(self):
        note = lambda n, d: f"x. 10/23: Stage Replied\u2192Contacted (Gmail: {n} Ryne emails {d}; no reply)."
        rows = [HDR,
                row("A", "Old", "Contacted", "3", "old@example.com", comments=note(3, "9/5, 9/8, 9/15")),
                row("B", "NoMail", "Contacted", "1", "", comments=note(1, "9/1")),
                row("C", "Recent", "Contacted", "2", "rec@example.com", comments=note(2, "9/23, 9/27")),
                row("D", "Exactly30", "Contacted", "1", "e30@example.com", comments=note(1, "9/22")),
                row("E", "Offer", "Offer", "7", "offer@example.com", comments=note(7, "8/1")),
                row("F", "Replied", "Replied", "1", "rep@example.com", comments=note(1, "8/1")),
                row("G", "Already", "Parked", "3", "al@example.com"),
                row("H", "NoNote", "Contacted", "2", "nonote@example.com", comments="no dates"),
                ["AVERAGES"] + [""] * 15,
                row("I", "Below", "Contacted", "1", "below@example.com", comments=note(1, "8/1"))]
        pc = f.park_candidates(rows, TODAY)
        self.assertEqual([x["name"] for x in pc["park_with_email"]], ["Old A"])
        self.assertEqual(pc["park_with_email"][0]["first_send"], "9/5/26")
        self.assertEqual([x["name"] for x in pc["no_email_listed"]], ["NoMail B"])
        self.assertEqual([x["name"] for x in pc["already_parked_with_email"]], ["Already G"])
        self.assertEqual([x["name"] for x in pc["unknown_first_send"]], ["NoNote H"])

    def test_gmail_first_sends_override(self):
        rows = [HDR, row("A", "Mapped", "Contacted", "1", "map@example.com")]
        pc = f.park_candidates(rows, TODAY, {"map@example.com": dt.date(2026, 9, 1)})
        self.assertEqual([x["name"] for x in pc["park_with_email"]], ["Mapped A"])

    def test_blank_stage_with_evidenced_send_no_reply(self):
        # Tally 10/23: blank Stage + evidenced send + no reply -> by-date candidate, same as Contacted
        note = "x. Gmail: 4 Ryne emails 8/21, 8/24, 8/28, 8/31; no reply."
        rows = [HDR,
                row("A", "BlankNote", "", "", "bn@example.com", comments=note),            # evidence in Comments
                row("B", "BlankGmail", "", "", "bg@example.com"),                          # evidence in --sends-json
                row("C", "BlankReplied", "", "", "br@example.com"),                        # sent, but lead replied
                row("D", "BlankRecent", "", "", "brc@example.com"),                        # sent 10/1: day 21
                row("E", "BlankNever", "", "", "never@example.com", comments="Lead Form"), # no send: not a candidate
                row("F", "BlankNoMail", "", "", "", comments=note),                        # listed, never parked
                row("G", "Eval", "Eval booked", "", "ev@example.com", comments=note)]      # other stages untouched
        sends = {"bg@example.com": {"first_send": "2026-08-25", "sends": 4, "replied": False},
                 "br@example.com": {"first_send": "2026-08-25", "sends": 2, "replied": True},
                 "brc@example.com": {"first_send": "2026-10-01", "sends": 1, "replied": False}}
        pc = f.park_candidates(rows, TODAY, sends)
        self.assertEqual([x["name"] for x in pc["park_with_email"]], ["BlankNote A", "BlankGmail B"])
        self.assertEqual(pc["park_with_email"][0]["first_send"], "8/21/26")
        self.assertEqual(pc["park_with_email"][1]["sends"], 4)
        self.assertEqual([x["name"] for x in pc["skipped_replied"]], ["BlankReplied C"])
        self.assertEqual([x["name"] for x in pc["no_email_listed"]], ["BlankNoMail F"])
        self.assertEqual(pc["unknown_first_send"], [])
        # same via the CLI --sends-json flag
        buf = io.StringIO(); csv.writer(buf).writerows(rows)
        sh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False); sh.write(buf.getvalue()); sh.close()
        sj = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(sends, sj); sj.close()
        out = subprocess.run([sys.executable, os.path.join(HERE, "followup_due.py"), "--sheet", sh.name,
                              "--park-candidates", "--sends-json", sj.name, "--today", "2026-10-22"],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("WITH email (newsletter list): 2", out.stdout)
        self.assertIn("skipped, replied: 1", out.stdout)

    def test_touch_count_path_unchanged(self):
        # due list still follows the schedule; a recent Contacted lead is due on its date, not parked
        rows = [HDR, row("C", "Recent", "Contacted", "2", "rec@example.com", nf="9/28/26")]
        self.assertEqual([x["name"] for x in f.build(rows, TODAY)["due"]], ["Recent C"])

    def test_park_candidates_cli_is_read_only(self):
        rows = [HDR, row("A", "Done", "Contacted", "1", "done@example.com",
                          comments="10/23: Stage Replied\u2192Contacted (Gmail: 1 Ryne email 9/1; no reply).")]
        buf = io.StringIO(); csv.writer(buf).writerows(rows)
        fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False); fh.write(buf.getvalue()); fh.close()
        with open(fh.name) as x:
            before = x.read()
        out = subprocess.run([sys.executable, os.path.join(HERE, "followup_due.py"), "--sheet", fh.name,
                              "--park-candidates", "--today", "2026-10-23"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("WITH email (newsletter list): 1", out.stdout)
        with open(fh.name) as x:
            self.assertEqual(x.read(), before)


class Newsletter(unittest.TestCase):
    def _row(self, last, first, cd, email, stage="Parked"):
        r = row(last, first, stage, "3", email)
        r[3] = cd
        return r

    def test_boundary_missing_date_no_email(self):
        rows = [HDR,
                self._row("A", "Edge", "10/22/25", "edge@example.com"),        # exactly 12 months: on
                self._row("B", "DayOver", "10/21/25", "over@example.com"),     # 12 months + 1 day: off (older)
                self._row("C", "Recent", "9/9/26", "recent@example.com"),
                self._row("D", "NoDate", "", "nodate@example.com"),
                self._row("E", "BadDate", "sometime", "bad@example.com"),
                self._row("F", "NoMail", "9/9/26", ""),
                self._row("G", "NotParked", "9/9/26", "np@example.com", stage="Contacted"),
                ["AVERAGES"] + [""] * 15,
                self._row("H", "Below", "9/9/26", "below@example.com")]
        nl = f.newsletter_list(rows, TODAY)
        self.assertEqual(nl["cutoff"], "2025-10-22")
        self.assertEqual([x["name"] for x in nl["on_list"]], ["Edge A", "Recent C"])
        self.assertEqual([x["name"] for x in nl["off_older"]], ["DayOver B"])
        self.assertEqual([x["name"] for x in nl["off_no_contact_date"]], ["NoDate D", "BadDate E"])
        self.assertEqual([x["name"] for x in nl["off_no_email"]], ["NoMail F"])

    def test_months_ago_leap_day(self):
        self.assertEqual(f.months_ago(dt.date(2028, 2, 29), 12), dt.date(2027, 2, 28))
        self.assertEqual(f.months_ago(dt.date(2026, 1, 15), 12), dt.date(2025, 1, 15))

    def test_cli_output(self):
        rows = [HDR, self._row("A", "Edge", "10/22/25", "edge@example.com"), self._row("B", "Old", "1/1/25", "old@example.com")]
        buf = io.StringIO(); csv.writer(buf).writerows(rows)
        fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False); fh.write(buf.getvalue()); fh.close()
        out = subprocess.run([sys.executable, os.path.join(HERE, "followup_due.py"), "--sheet", fh.name,
                              "--newsletter-list", "--today", "2026-10-22"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("1 on list", out.stdout)
        self.assertIn("Edge A <edge@example.com>", out.stdout)
        self.assertIn("older than 12 months: 1", out.stdout)


class Inputs(unittest.TestCase):
    def _tmp(self, text, suffix):
        fh = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False)
        fh.write(text); fh.close()
        return fh.name

    def test_csv_values_and_connector_json(self):
        buf = io.StringIO(); csv.writer(buf).writerows(sheet()); text = buf.getvalue()
        p1 = self._tmp(text, ".csv")
        p2 = self._tmp(json.dumps({"values": sheet()}), ".json")
        p3 = self._tmp("wrapper text\n" + json.dumps({"spreadsheetId": "x", "ranges": [{"sheet": "2026", "content": text}]}) + "\nend", ".txt")
        for p in (p1, p2, p3):
            res = f.build(f.load_rows(p), TODAY)
            self.assertEqual(len(res["due"]), 3, p)

    def test_columns_found_by_name_not_position(self):
        rows = sheet()
        order = list(range(16)); order[4], order[13] = 13, 4  # swap Stage and Comments
        moved = [[r[i] if i < len(r) else "" for i in order] for r in rows]
        self.assertEqual([x["name"] for x in f.build(moved, TODAY)["due"]], ["Bob Over", "Ann Due", "Cnt Blank"])

    def test_missing_column_and_empty_are_errors(self):
        with self.assertRaises(f.InputError):
            f.build([HDR[:-1]], TODAY)
        p = self._tmp("", ".csv")
        with self.assertRaises(f.InputError):
            f.load_rows(p)

    def test_cli(self):
        script = os.path.join(HERE, "followup_due.py")
        out = subprocess.run([sys.executable, script, "--next", "10/21/26", "--step", "0"], capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "10/23/26")
        out = subprocess.run([sys.executable, script, "--next", "10/21/26", "--step", "6"], capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "parked")
        p = self._tmp("", ".csv")
        out = subprocess.run([sys.executable, script, "--sheet", p], capture_output=True, text=True)
        self.assertEqual(out.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
