# Achieve Minute: Best Send Day and Time (research, Oct 14 2026)

## Recommendation
- **Primary: Tuesday, 7:30 AM CT.** It's a weekday morning and fits the parent routine before drop-off. Tuesday was the best day for opens and clicks in Omnisend's 2026 data. In Ryne's own history, morning sends had the highest median click rate.
- **Backup / test: Sunday, 7:00 PM CT.** That's when families plan the week. Sunday sends had Ryne's highest median click rate, but there were only 5 of them.
- **How to decide:** run each slot for 4 weeks and keep the same time every week. Judge on **clicks and replies, not opens**, because Apple Mail Privacy Protection makes open counts and open times unreliable. Keep the winner.
- **Content timing:** for meet- or game-related issues, a Thursday evening send can land closer to the weekend. That's optional, and only for topical issues.

## Ryne's own Mailchimp data (All Subscribers, read-only)
- 217 campaign reports exist. The monthly newsletter has gone to All Subscribers since 2020. The list now has about 1,150 to 1,190 recipients per send.
- Recent reported open rates are 49% to 69%. **With Apple proxy opens excluded,** recent sends drop to 16% to 31%. For example, the Summer 2026 newsletter shows 64.9% reported but 28.9% excluding proxy opens. Clicks are low, about 0.6% to 1.6% per send recently.
- **24-hour open timelines (5 recent sends):**

| Send (CT) | Excl.-proxy open rate | 24h pattern |
|---|---|---|
| Wed 10/08/25 4:10 PM | 30.7% | 320 opens in the first hour, 15 clicks in 24h, small bump at 10 PM |
| Mon 7/6/26 11:19 AM | 28.9% | 338 opens in the first hour, small bump at 10 PM |
| Sat 12/6/25 1:07 PM | 28.8% | 292 in the first hour, 13 clicks |
| Thu 3/5/26 3:50 PM | 19.5% | 125 then 134 in the first two hours, 6 clicks |
| Mon 4/6/26 1:36 PM | 15.7% | 134 in the first hour, 9 clicks |

- **Takeaways:**
  - Most opens and clicks happen within 1 to 2 hours of the send (part of that first-hour spike is Apple prefetch), so the send time itself matters.
  - There is a consistent second, smaller bump around 10 to 11 PM CT. Parents read late.
  - Almost nothing happens from about 1 AM to 7 AM.
- **Median click rate by send day, 2023 to 2026 (41 newsletters):**
  - Sun 2.5% (5 sends), Fri 1.9% (4), Tue 1.8% (8), Wed 1.6% (5), Thu 1.4% (7), Sat 1.4% (7), Mon 1.0% (5)
  - By time of day: morning 1.8% (9), evening 1.9% (8), midday 1.3% (9), late afternoon 1.4% (15)
- **Caveat:** the samples are tiny, and click rates fell over time no matter the day. Sends have never been timed on purpose, so treat this data as a hint, not proof.

## Mailchimp features
- Send Time Optimization (based on clicks) and Timewarp require the Standard plan or higher. The API only reports "monthly" as the plan type. The account has 17 audiences, more than the Essentials (3) or Standard (5) limits, which suggests a legacy plan. Check under Account > Billing.
- Timewarp doesn't matter much here, since nearly everyone is in Central time.

## Industry research
- **Omnisend (2026, ~26B emails):**
  - Tuesday leads for opens (31.3%) and clicks (0.81% click-to-sent). Friday leads for conversions.
  - Best hours: 9 AM for opens, 4 PM for clicks, 7 AM for conversions.
  - https://www.omnisend.com/blog/best-time-to-send-email/
- **Klaviyo (2023 data):**
  - Wednesday and Thursday are best overall. Weekday differences are tiny: open rates run from 12.14% to 12.52% Monday through Friday.
  - https://www.klaviyo.com/blog/best-day-to-send-emails
- **Brevo:**
  - Tuesday and Thursday, 10 AM to 3 PM. Wednesday gets the most clicks. Weekends are weakest.
  - https://www.brevo.com/blog/best-time-to-send-email/
- **MoEngage EU 2025 benchmarks:** no significant difference by send day.
  - https://info.moengage.com/hubfs/EU%20Marketing/EU%20Email%20Benchmarks%20Report%202025.pdf
- **Parent audiences** (weak evidence: vendor blogs from school-communication companies, and they contradict each other):
  - Daystage says Sunday 6 to 9 PM or Monday 7 to 9 AM, and that a consistent send time builds a reading habit. https://www.daystage.com/blog/guides/school-newsletter-open-rates-research
  - Another Daystage piece says Tuesday to Thursday, 7 to 9 AM. https://www.daystage.com/blog/principals/school-newsletter-open-rate
- **Apple Mail Privacy Protection:**
  - Apple preloads emails, so they register as opened even when unread, and open times reflect Apple's prefetch schedule. Use clicks to judge timing.
  - Mailchimp: https://mailchimp.com/help/apple-privacy-faq/
  - Postmark: https://postmarkapp.com/blog/how-apples-mail-privacy-changes-affect-email-open-tracking
  - SendGrid: https://www.twilio.com/docs/sendgrid/for-developers/tracking-events/understanding-apple-mail-privacy-protection-and-open-events
- **Mailchimp plan features:**
  - https://mailchimp.com/help/use-send-time-optimization/
  - https://mailchimp.com/help/use-timewarp/
