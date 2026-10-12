# Meta ads: lock-screen notifications

There are 20 static ads. Each one is an iPhone lock-screen screenshot (1179×2556) showing a notification couples wish they'd get. They were made on 7 Oct 2026.

- **Where to run them:** Stories and Reels show the full image. In the Feed, Meta crops it to 4:5 around the middle, which still keeps the caption and the notifications.
- **No button or offer on the image:** pick "Install now" as Meta's button. Put the promise in the ad's text, for example: "Our promise: fewer fights in 7 days. Start tonight."
- **The 3 ads aimed at men** (13, 15, 10) go in a separate ad set targeted at men. Suggested ad text: "She notices more than you think."

## Ranked, strongest first

| Score | File | Caption |
|---|---|---|
| 10 | Loveth-01-resolved-a-fight | the notification I never thought I'd get |
| 10 | Loveth-02-not-defensive | he's actually changing |
| 9.5 | Loveth-16-let-me-finish | he let me finish. for once |
| 9.5 | Loveth-17-no-but | sorry. no "but" |
| 9.5 | Loveth-05-sorry-first | he said sorry FIRST |
| 9 | Loveth-09-kept-his-word | he kept his word. every single day |
| 9 | Loveth-07-same-fight-faster | same fight as last month. this time it took 9 minutes |
| 9 | Loveth-18-forget-it | I stopped saying "forget it" |
| 9 | Loveth-19-silent-treatment | no silent treatment. 21 days |
| 9 | Loveth-20-phone-down | I didn't even have to ask |
| 8.5 | Loveth-04-talked-it-through | we actually talked instead of shouting |
| 8.5 | Loveth-03-six-days | 6 days. we used to not manage 6 hours |
| 8.5 | Loveth-12-thirty-days | we used to fight every week |
| 8.5 | Loveth-21-really-feeling | he asked how I'm REALLY doing |
| 8 | Loveth-13-trash | she noticed (for men) |
| 8 | Loveth-15-kind-when-angry | she said I've changed (for men) |
| 8 | Loveth-06-noticed-effort | someone finally noticed |
| 8 | Loveth-10-she-noticed | she noticed (for men) |
| 7.5 | Loveth-14-asked-about-her-day | it was that simple? (for men) |
| 7.5 | Loveth-22-sofa | the sofa's just a sofa again |

## Editing them

`source/render_ads.py` builds all 20 with Playwright and Chromium, using the Inter fonts. To change a caption, notification or date, edit the `ads` list in that file and run it from a folder that also contains `logo/Loveth-icon-1024.png`.
