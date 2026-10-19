# Email and Newsletter Marketing Research for Achieve Sports Performance
Prepared 2026-10-14. Applies to The Achieve Minute (short value emails with a P.S. plug) and the quarterly newsletter, sent from Mailchimp. Every number below links to its source. Where no source was found, there is no number.

House rules for every recommendation: no prices in emails, no em dashes, never use the word "complimentary", evaluations are offered in the evenings, and Ryne approves every draft before it sends.

## 1. Cadence, frequency, and send timing
- **Mailchimp's send-time research:** Across Mailchimp's whole data set, weekdays do best and about 10 AM local time is the broadest peak. But 10 AM is the best time for only a small share of recipients (about 6 to 7 percent), so there is no single best time. Sources: [Mailchimp send-time insights](https://mailchimp.com/resources/insights-from-mailchimps-send-time-optimization-system/), [analysis of that data](https://jacobfilipp.com/maildata/insights-from-mailchimps-send-time-optimization-system/index.html).
- **Send Time Optimization:** Mailchimp's feature delivers each email within 24 hours of the date you pick, at the time that contact usually engages. It needs the Standard plan or higher, enough engagement history, and scheduling at least 48 hours ahead. Source: [Mailchimp help](https://mailchimp.com/help/use-send-time-optimization/).
- **What the experts do:** Ben Settle sends one short plain-text email every day and sells in every one ([Ben Settle](https://bensettle.com/blog/how-to-make-6-figures-per-year-writing-one-email-per-day/)). Ann Handley's Total Annarchy goes out every two weeks and is personal and built on stories ([Campaign Monitor case study](https://www.campaignmonitor.com/blog/email-marketing/how-ann-handley-grew-her-newsletter/)). What they share is a fixed, predictable schedule. How often you send matters less than sending on schedule.
- **For Achieve:** Send The Achieve Minute once a week, on the same weekday every time. Parents of school-age athletes tend to read in the evening after practice, but that is my guess, not a sourced fact, so test it (section 9). The quarterly newsletter stays separate and goes out at the start of each season: fall, winter, spring, and summer. Don't send daily until the weekly email has held steady for one quarter.

## 2. List growth and lead magnets
- **Hormozi ($100M Leads):** A lead magnet should fully solve one narrow problem and, in doing so, reveal the next problem, which the paid offer solves. He names three types: reveal a problem (a diagnosis), give a sample or trial, or give one step of a multi-step process. Make it good enough that you could charge for it, and end with one clear call to action. Source: [$100M Leads summary](https://lythrumpress.com.au/chapter/100m-leads-by-alex-hormozi-section-2/).
- **Ramit Sethi:** Go for quality subscribers over raw numbers. Solve an urgent pain, promote the lead magnet where the audience already spends time, and make signing up easy. Source: [I Will Teach You To Be Rich](https://www.iwillteachyoutoberich.com/how-to-build-an-email-list/).
- **Morning Brew's referral program:** Referrals are widely reported to have driven a large share of its growth. Second-hand reports put the referral share of growth anywhere from about 30 percent to as high as 80 percent in early periods. Source: [Referral Rock](https://referralrock.com/blog/morning-brew-referral-program/). Their setup used personal referral links and rewards that grew at each milestone.
- **Lead magnet ideas for Achieve (all diagnosis-style, all leading to the eval):** "Swim Dryland Readiness Check" (5 at-home tests a parent can film), "Is Your Athlete's Jump Telling You Something? (what force plates measure)", "In-Season Strength Checklist for HS Athletes". Every one ends with the evening evaluation as the next step.
- **Where to collect signups:** the eval intake form (with a consent checkbox), the front desk QR code, the website footer, Instagram bio, and handouts for team and club parents.

## 3. Segmentation
Set up Mailchimp tags or groups: **Role** (Parent, Athlete 13+, Adult client), **Sport** (Swim, Other), **Status** (Lead, Evaluated, Active, Former). Always segment by role and by swim versus other sports. Send one Achieve Minute to everyone but swap in a segment-specific P.S. (Mailchimp conditional merge tags or separate sends). Leave athletes under 13 off the list entirely (see section 10).

## 4. Welcome and nurture sequence
New subscribers are at their most engaged when they first sign up, so automate a short sequence (Mailchimp Customer Journeys):
1. Day 0: Deliver the lead magnet. Answer first, then give one sentence on who Ryne is.
2. Day 2: The proof: 130 college commits (about 70 percent D1), 6 Olympic Trials qualifiers.
3. Day 5: How the eval works (force plates, then a written program). Evaluations are in the evenings, and the call to action is to reply to book.
4. Day 9: A story about one named athlete, used with permission.
5. Day 14: Hand off to the weekly Achieve Minute.
Every sequence email goes to Ryne for approval before the automation is turned on.

## 5. Deliverability
- **Gmail and Yahoo rules (in force since 2024):** Bulk senders must have SPF, DKIM, and DMARC (p=none at minimum), with the From domain aligned. Marketing email must support one-click unsubscribe, and unsubscribes must be honored within 2 days (48 hours). Keep spam complaints under 0.3 percent, ideally under 0.1 percent. Sources: [Gmail sender guidelines](https://support.google.com/mail/answer/81126), [Gmail FAQ](https://support.google.com/a/answer/14229414?hl=en), [Yahoo Sender Hub](https://senders.yahooinc.com/best-practices/).
- **Mailchimp setup:** Account & billing > Domains > authenticate achievesportsperformance.com. This adds 2 CNAME records (DKIM) and 1 TXT record (DMARC). Validation can take up to 48 hours. Send from the work mailbox, never from a gmail.com address. Source: [Mailchimp domain authentication](https://mailchimp.com/help/set-up-email-domain-authentication/).
- **Plain vs designed, and image-to-text ratio:** Mailchimp advises keeping text above 20 percent of the email and using several content blocks instead of one large image. Source: [Mailchimp content for deliverability](https://mailchimp.com/resources/email-content-for-deliverability/). For Achieve: The Achieve Minute should look like a personal letter, with mostly text, at most one image, and few links. The quarterly newsletter can carry Designer's card, but the key copy should be live text, not baked into the image.
- **List hygiene:** Use double opt-in for public forms. Never import scraped or purchased lists or team rosters that didn't opt in. Remove hard bounces.

## 6. Subject lines and preview text
Mailchimp allows subject lines up to 150 characters but recommends 60 or fewer ([Mailchimp](https://mailchimp.com/help/create-ab-tests/)). Subject lines that are specific and concrete fit the brand: "The jump test that predicts swim starts." Always write preview text that continues the subject line instead of repeating it. CAN-SPAM bans misleading subject lines ([FTC](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)). Stick to one consistent From name, for example "Ryne at Achieve".

## 7. Benchmarks (use with caution)
| Source | Category | Open | Click | Unsub |
|---|---|---|---|---|
| [Mailchimp](https://mailchimp.com/resources/email-marketing-benchmarks/) (data last updated Dec 2023) | Education + Training | 35.64% | 3.02% | 0.18% |
| Mailchimp | All users | 35.63% | 2.62% | 0.22% |
| [SaaS Scored](https://saasscored.com/blog/email-marketing-benchmarks-by-industry), compiling MailerLite/ActiveCampaign/Moosend data | Health & Fitness | 47.81% | 1.45% | 0.29% |
| SaaS Scored | Sports & Recreation | 47.69% | 1.27% | 0.16% |

**Apple MPP:** Apple Mail Privacy Protection loads emails automatically, which records "opens" nobody made. Litmus reports Apple (including MPP) at roughly half of all tracked opens (49.79 percent in March 2025) and says MPP-affected opens can exceed 50 percent of opens. Sources: [Litmus market share](https://www.litmus.com/email-client-market-share/), [Litmus MPP center](https://www.litmus.com/apple-mail-privacy-protection-resources). Treat open rate as a rough trend signal only, useful mainly for spotting a sudden drop that points to a deliverability problem.

## 8. Measuring what matters
Track these each month in a simple sheet:
1. **Replies** per send. The P.S. asks for a reply, so replies are the main signal.
2. **Evaluations booked** that can be traced back to an email (ask "how did you hear" at booking, and use the reply keyword such as "dryland").
3. **Click rate** on the single link.
4. **Unsubscribes and spam complaints** (complaints must stay under 0.1 percent).
5. **List growth** net of unsubscribes.
Opens are tracked only to spot deliverability trends.

## 9. A/B testing in Mailchimp
Mailchimp A/B tests one variable at a time (subject line, From name, content, or send time) with up to 3 variations. The test must go to at least 10 percent of the list, and Mailchimp recommends at least 5,000 contacts per variation for reliable results. Send-time tests go to 100 percent of the list. Multivariate tests allow up to 8 combinations. Sources: [Create A/B test](https://mailchimp.com/help/create-ab-tests/), [About A/B tests](https://mailchimp.com/help/about-ab-tests/), [Multivariate](https://mailchimp.com/help/create-multivariate-tests/).
**For Achieve:** The list is almost certainly far below 5,000 per variation, so treat test results as directional only. Pick winners by clicks, not opens, because MPP inflates opens. Test one thing per month: first send day/time (e.g., Tue 7 PM vs Sun 7 PM CT), then the subject line style, then where the P.S. sits.

## 10. Re-engagement and sunsetting
Mailchimp can find inactive contacts (contact rating or no recent engagement). Send them a re-engagement campaign, then archive those who still don't respond. Archiving removes them from the audience but keeps their data. Sources: [Identify inactive](https://mailchimp.com/help/identify-inactive-subscribers/), [Re-engage](https://mailchimp.com/help/re-engage-inactive-subscribers/), [Archive](https://mailchimp.com/help/remove-inactive-contacts/).
**For Achieve:** Every quarter, find contacts with no clicks for 6 months (judge by clicks, because MPP opens can't be trusted). Send them 2 short emails, for example "Still want these? Reply yes." Archive anyone who doesn't respond. Graduated seniors could move to an adult or alumni segment instead of getting cut.

## 11. Legal
- **CAN-SPAM (FTC):** No false headers or misleading subject lines. Identify the email as an ad where that applies. Include a valid physical address (4020 Fox Valley Center Drive, Aurora, IL). Include a clear opt-out that keeps working for 30 days after sending. Honor opt-outs within 10 business days (Gmail and Yahoo require 2 days, so in practice the deadline is 2 days). Being a member doesn't exempt someone from these protections. Sources: [FTC compliance guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business), [FTC 2023 blog](https://www.ftc.gov/business-guidance/blog/2023/08/when-sending-commercial-email-businesses-cant-unsubscribe-can-spam-compliance).
- **Consent:** Use an explicit opt-in checkbox, not pre-checked, and keep a record of it (Mailchimp logs signup source and time). Clients aren't on the marketing list automatically just because they are clients.
- **Minors / COPPA:** COPPA generally requires verifiable parental consent before collecting personal information, including an email address, from a child under 13. The amended rule took effect June 23, 2025, with compliance required by April 22, 2026. Sources: [eCFR 16 CFR 312](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312), [Federal Register 2025](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule), [FTC press release](https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-finalizes-changes-childrens-privacy-rule-limiting-companies-ability-monetize-kids-data). **For Achieve:** Collect parent emails only for anyone under 13 (athletes start at 11). For athletes 13 to 17, a parent should opt them in or be copied. Get written permission before naming or showing any minor athlete. This is general research, not legal advice; check with counsel.

## 12. Expert frameworks, condensed
- **Hormozi:** Lead magnets that reveal the next problem. Give, give, give, then ask. Source above.
- **Ben Settle:** Send daily, keep it short and in plain text, show personality, and sell in every email. Lesson for Achieve: a small sell in every email, which is what the P.S. does.
- **Ramit Sethi:** Quality list, solve an urgent pain, earn the right to sell.
- **Morning Brew:** Referral loop with personal links and milestone rewards. Lesson for Achieve: the referral P.S. needs a real reward from Ryne.
- **Justin Welsh:** Saturday Solopreneur goes out every week at the same time and has reportedly grown without a referral program ([Newsletter Engines](https://mikeromaine.com/referral-systems-newsletters/)). Lesson: being consistent beats gimmicks.
- **Ann Handley:** Write to one person, tell stories, keep a personal voice. Grew from 0 to 42,000 subscribers ([Campaign Monitor](https://www.campaignmonitor.com/blog/email-marketing/how-ann-handley-grew-her-newsletter/)).
- **Mailchimp / Litmus research:** Authenticate the domain, keep plenty of real text in the email, judge by clicks over opens, and archive inactive contacts.

## 13. Top recommendations for Achieve
1. Authenticate achievesportsperformance.com in Mailchimp (DKIM plus DMARC p=none) and send only from Ryne's gym address before Issue 1 goes out.
2. Send The Achieve Minute weekly on one fixed evening, and keep the quarterly newsletter as a separate seasonal send.
3. Make The Achieve Minute a plain, letter-style email with one idea, one link at most, and the P.S. as the only ask, asking for a reply keyword.
4. Measure replies and booked evening evaluations first, clicks second, and opens only as a deliverability alarm.
5. Tag every contact by role (parent, athlete 13+, adult) and sport (swim vs other), and vary the P.S. by segment.
6. Build one diagnosis-style lead magnet (Swim Dryland Readiness Check) and put the signup on the eval form, front desk QR code, website, and Instagram.
7. Turn on a 5-email welcome sequence that ends with the evening evaluation invite, after Ryne approves each email.
8. Collect parent emails only for athletes under 13, use unchecked opt-in boxes, and get written permission before naming a minor.
9. Every quarter, send a 2-email re-engagement campaign to contacts with no clicks in 6 months, then archive the ones who still don't respond.
10. Run one A/B test a month in Mailchimp (send day first), pick winners by clicks, and treat results as directional at our list size.
