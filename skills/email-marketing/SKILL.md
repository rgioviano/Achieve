---
name: email-marketing
description: When planning, writing, reviewing, or measuring marketing emails or newsletters (value emails, welcome sequences, list growth, deliverability, copywriting).
---
# Email marketing

Full sourced research lives beside this file:
- [references/strategy-deliverability-research.md](references/strategy-deliverability-research.md) (cadence, list growth, segmentation, deliverability, benchmarks, testing, legal)
- [references/copywriting-research.md](references/copywriting-research.md) (subject, preview, hooks, structure, P.S., plain vs designed, replies)
- [references/design-research.md](references/design-research.md) (layout, type, color and contrast, images, dark mode, accessibility, Gmail clipping)

## Core rules
1. **Strategy:** every email is useful first; one idea per email; one ask. Small sell in every send (the P.S.), give before asking.
2. **Cadence:** a fixed, predictable schedule beats any "best time." Mailchimp's data peaks near 10 AM weekdays, but that is the best time for only ~6-7% of recipients ([Mailchimp](https://mailchimp.com/resources/insights-from-mailchimps-send-time-optimization-system/)). Default weekly, same day and time; test the slot. Go more frequent only after a stable quarter.
3. **List growth:** a lead magnet should fully solve one narrow problem and reveal the next one the paid offer solves (Hormozi, [$100M Leads](https://lythrumpress.com.au/chapter/100m-leads-by-alex-hormozi-section-2/)); diagnosis style works best. Collect signups wherever the audience already is (intake forms, QR at desk, site footer, social bio). Referral loops need a real reward ([Morning Brew](https://referralrock.com/blog/morning-brew-referral-program/)). Quality over count.
4. **Segmentation:** tag every contact by role, interest/product, and status (lead, customer, former). Send one core email, vary the P.S. by segment.
5. **Welcome sequence:** automate ~5 emails over ~2 weeks: deliver magnet, proof, how the offer works, a real story (with permission), hand off to the regular send. Human approves each before it goes live.
6. **Deliverability:** SPF, DKIM, DMARC (p=none min) with aligned From domain; one-click unsubscribe honored within 2 days; spam complaints <0.3%, target <0.1% ([Gmail](https://support.google.com/mail/answer/81126), [Yahoo](https://senders.yahooinc.com/best-practices/)). Send from your own domain, never a free webmail address ([Mailchimp auth](https://mailchimp.com/help/set-up-email-domain-authentication/)). Keep text >20% of the email, real live text not images ([Mailchimp](https://mailchimp.com/resources/email-content-for-deliverability/)). Double opt-in on public forms; never buy/scrape/import non-opted lists; drop hard bounces.
7. **Subject:** a plain headline that names the topic and the reader; curiosity only if line one pays it off. ≤60 characters recommended ([Mailchimp](https://mailchimp.com/help/create-ab-tests/)). Never misleading (CAN-SPAM). Write 5+ options, pick one. Consistent From name.
8. **Preview text:** always fill it; finish the subject's thought. Blank shows "Hi Name," and wastes the slot.
9. **Body:** open by continuing the subject line. Skeleton: greeting, hook (real moment or plain problem), the tip (what, when, how much), why it works (one sourced line), one line for the secondary reader, sign-off with no ask, P.S., sources. ~150-250 words (house judgment; HubSpot found 300-500 characters had the best click rate, [2014 report](https://cdn2.hubspot.net/hub/53/file-2191769206-pdf/Science_of_Email_Marketing_2014.pdf)). Write for skimmers: first and last lines carry the point. Real stories only.
10. **P.S. / CTA:** the P.S. is the single ask, restates the next step, gives a true reason for now (season, start date; never fake urgency), and scripts the reply (one word). Replies are an engagement signal MPP can't fake.
11. **Design:** simple wins. In every HubSpot A/B test the simpler email won: plain text got 42% more clicks than a GIF version; an image-heavy HTML template got 51% fewer clicks ([HubSpot](https://blog.hubspot.com/marketing/plain-text-vs-html-emails-data)). Look like a personal letter: white, one font, one image max, few links.
12. **Measurement:** judge by replies and booked outcomes first, clicks second, unsubscribes/complaints as guardrails, net list growth monthly. Opens are only a deliverability alarm: Apple MPP is roughly half or more of tracked opens ([Litmus](https://www.litmus.com/email-client-market-share/), [MPP](https://www.litmus.com/apple-mail-privacy-protection-resources)). Benchmarks (Mailchimp, Dec 2023): all users 35.63% open, 2.62% click, 0.22% unsub ([Mailchimp](https://mailchimp.com/resources/email-marketing-benchmarks/)).
13. **Testing:** one variable at a time, up to 3 variations; Mailchimp recommends ≥5,000 contacts per variation ([Mailchimp](https://mailchimp.com/help/about-ab-tests/)), so small lists are directional only. Pick winners by clicks/replies, not opens. One test a month: send time, then subject style, then P.S. placement.
14. **Re-engagement:** quarterly, find contacts with no clicks in 6 months, send 2 short "still want these? reply yes" emails, archive non-responders ([Mailchimp](https://mailchimp.com/help/re-engage-inactive-subscribers/)).
15. **Legal and minors:** CAN-SPAM needs truthful headers/subjects, a physical address, a working opt-out, opt-outs honored within 10 business days (2 days for Gmail/Yahoo in practice) ([FTC](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)). Unchecked opt-in boxes with recorded consent; customers aren't auto-subscribed. COPPA: verifiable parental consent before collecting a child under 13's email; amended rule compliance by April 22, 2026 ([eCFR](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312)). Collect parent emails for under-13s; written permission before naming or showing a minor. Not legal advice.

## Design (from design research)
- Single 600px column on a white background. Keep it simple and letter-like.
- Body copy is live web-safe text (Helvetica/Arial), 16px, line height 1.5, dark gray (e.g. #222222). Brand fonts only inside images.
- Images go on solid backgrounds, not transparent ones, so logos hold up in dark mode. Always fill in alt text, and repeat any key tip from an image as live text.
- Accent color only where it passes WCAG AA contrast on white; links are underlined; a button, if used, is HTML and at least 44px tall.
- Small print (Sources, footer) at about 12px in mid gray.
- Keep the HTML well under Gmail's ~102KB clipping limit.
- No sourced image-to-text ratio exists; follow the "mostly live text" rule instead.

## Send timing (from send-time research)
- Consistency beats the perfect slot: same day and time every week builds a reading habit.
- Industry day differences are tiny (Tuesday slightly ahead in Omnisend 2026; Klaviyo weekday open rates within about 0.4 points). Don't over-optimize.
- Judge timing on clicks and replies, never opens: Apple Mail Privacy Protection auto-opens mail on Apple's schedule and inflates open rates.
- Test method: run one slot for 4 weeks, then a second slot for 4 weeks, same content type, keep the winner by clicks and replies.
- Check the business's own history first (Mailchimp /reports, timeseries) before trusting benchmarks.
- Full notes: references/send-time-research.md

## Per-issue checklist
**Strategy and cadence**
- [ ] One idea, useful this month, fits the calendar; going out on the fixed schedule.
- [ ] Source for every claim found; every story, name, number, or reward confirmed by the owner, else cut.
**List and segmentation**
- [ ] Right segment(s); P.S. variant per segment chosen. No non-opted contacts.
**Deliverability**
- [ ] Domain authenticated, sending from own domain, one-click unsubscribe, physical address in footer.
- [ ] Mostly live text, ≤1 image, few links.
**Subject and preview**
- [ ] 5+ subject options, plain headline ≤60 chars, not misleading.
- [ ] Preview text filled, finishes the subject's thought.
**Body**
- [ ] First line continues the subject; ~150-250 words; skimmer gets it from first and last lines.
- [ ] Tip states what, when, how much; one sourced "why" line; one line for the secondary reader.
- [ ] Closing line signs off with no ask; signature correct.
**P.S.**
- [ ] Only ask in the email; true reason for now; one-word scripted reply.
**Design**
- [ ] Simple, letter-like; test send to phone and Gmail; preview line reads well.
**Measurement and testing**
- [ ] After send: log replies, booked outcomes, clicks, unsubscribes, complaints. Ignore opens except as an alarm.
- [ ] At most one A/B variable this month, judged by clicks/replies.
**Legal and minors**
- [ ] Opt-out works; address present; no minor named/shown without written permission; under-13 contacts are parent emails only.

## Business-specific notes (Achieve Sports Performance)
- Signature (Ryne 2026-10-14): "Thanks," then "Ryne Gioviano, MSEd, CSCS" then "Achieve Sports Performance & Personal Training".
- Footer (Ryne 2026-10-14): "Achieve Sports Performance & Personal Training", street address, link to www.achievesportsperformance.com, unsubscribe.
- Template: every Achieve Minute starts from templates/achieve-minute.html (copy also at /workspace/newsletter/Achieve-Minute-TEMPLATE.html). Same hosted header image, layout, colors, signature, P.S., Sources and footer; only fill the {{placeholders}}. Do not redesign per issue.
- Send time: primary Tuesday 7:30 AM CT, test Sunday 7:00 PM CT (4 weeks each). Optional Thursday evening for meet/game-weekend issues. Own data (2023 to 2026): morning and Sunday sends had the best median click rates; readers show a second bump around 10 to 11 PM CT; real (non-Apple) opens about 16% to 31%, clicks about 0.6% to 1.6%. Sending domain achieve-personaltraining.com is already authenticated (DKIM, SPF, DMARC p=none).
- No prices in any email. No em dashes anywhere. Never use the word "complimentary"; call it an "evaluation" or "20-minute screen."
- Write to the parent first, plus one "Tell your athlete: ..." line.
- The P.S. is the only ask; it rotates with the season (referral P.S. only once a real reward is supplied). Owner approves every draft before it sends.
