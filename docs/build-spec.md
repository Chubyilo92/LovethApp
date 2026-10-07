# Loveth — Stop having the same fight · Build Spec

Oct 6, 2026 · @Macchris

**Status: design locked for MVP (6 Oct 2026).** Build only what is in this doc and the design canvas. No new screens or features without sign-off.

## Purpose and core promise

Loveth is built for one problem: couples who argue frequently. It won't suit everyone, and it doesn't try to. It sells one thing: the couple stops repeating the same fight, because the app keeps them both accountable every day and steps in when an argument starts. Every screen in this flow must leave the user believing that promise before we ask for money.

**The two messages the user must leave onboarding with:**

1. **"It keeps us both accountable in the hard moments."** Not just on good days. When it's 11pm, you're tired and you want to snap, the app is the thing that reminds you both what you promised.
2. **"It helps us in the middle of an argument."** Mid-fight, each of you knows the one thing you promised the other, so the fight stops before it becomes the old fight.

**Principle: we don't ask for anything until we've proved we can deliver.** The user gets a named diagnosis and a daily plan (real value) before the partner invite, and before the paywall.

Throughout this doc the user is **Sarah** and her partner is **Mark**. Loveth is self-contained: no tie-ins to CoupleIn's points, mood check or shared calendar. It has its own Resolve.

## Flow at a glance

&#91;embedded content: Break the Cycle onboarding, 6 screens then the trial\]

Sarah gets her diagnosis and plan before inviting Mark, and commits three times before she sees a price.

## Global rules

These rules apply to every screen below unless the screen says otherwise.

### Roles and names

- **Initiator** = the person who starts Loveth (Sarah in examples). **Partner** = the person they invite (Mark). Either person in a couple can be the initiator.
- In copy, `[Partner]` = the partner's first name typed at screen 1A.1. `[Me]` = the user's own first name, asked at 1A.1.
- Copy never uses he/she/him/her. Always use the name. This keeps copy correct for every couple.
- Banned words anywhere a user can see: rating, score, scoring, winner, loser, points.

### How screens are written in this doc

- Every screen has an ID: `stage.screen` (e.g. 1.3 = Stage 1, screen 3).
- Each screen lists **Shows** (what's on it), **Options** (every tappable thing → what happens) and **Saves** (data written).

### Entry point

- Loveth is its **own app** on the App Store and Google Play, separate from CoupleIn. It only copies CoupleIn's partner-invite approach. First open → 0.1 Why are you here? (see Routes). No account or sign-in until they pay (see Accounts: none until they pay).
- No progress yet → opens 0.1. Progress exists → opens the last unfinished screen. Onboarding complete → opens Home (section: After onboarding).

### Navigation on every onboarding screen (Stages 1–6)

- **Progress bar** at the top, one per route, split into that route's parts by name. Fighting: You two · You · \[Partner\] · The problem · How it goes · Your report. Intimacy: You two · You · \[Partner\] · Closeness · Your report. The hard week: You two · The hard week · You · \[Partner\] · How it goes · Your report. Stages 2–6 show "Step \[n\] of \[n\]" instead. Not shown on 0.1–0.3.
- **Back arrow** (top left) → previous screen, previous answer pre-selected. Not shown on 1A.0, 1A.1 or on success screens. Changing an earlier answer rebuilds the report at 1G.5.
- **Close X** (top right) → bottom sheet: *"Leave for now? Your answers are saved."*
  - **Keep going** → closes the sheet.
  - **Leave** → closes the flow. Progress saved. Next entry resumes on this screen.
  - If the invite has already been sent (screen 3.2 completed), leaving from Stage 4, 5 or 6 sets the couple to **Pulled back** (see Subscription states).
- **Single-choice questions:** tapping an answer highlights it and moves to the next screen after 0.3 seconds. No Continue button.
- **Text and time inputs:** a **Continue** button, disabled until the input is valid.

### Prices

- Show the localised price string supplied by the App Store / Google Play, never a hard-coded price. UK prices: £9.99/month, £49.99/year.

### Accounts: none until they pay

- **No sign-in, no requests, nothing, until they pay.** No sign-up screen, no login, no email field, no prompts or nudges anywhere before payment. On first open the app silently creates an anonymous account (Supabase or Firebase anonymous auth) tied to the device. Name comes from 1A.1; nothing else is asked.
- Couples link through the invite link (deferred deep link). The partner taps **Open it** on the sealed note and is in.
- The subscription belongs to the App Store / Google Play account, so **Restore purchase** always works on a new phone.
- **A real account is created only at payment.** The moment the purchase (or 7-day trial start) succeeds on the paywall, the next screen creates the account in one tap: Sign in with Apple on iOS, Sign in with Google on Android. The anonymous account is upgraded in place (account linking), so nothing they entered is lost and the couple stays linked.
- **Order matters:** store payment sheet first, account second. Never ask for the account before or as a condition of the purchase (Apple rejects apps that make people register before buying).
- Data recovery: once the account exists, signing in with Apple or Google on a new phone brings everything back. Before payment there is nothing to recover: a reinstall starts fresh, and the partner can re-invite them.

## Build standard — native and premium on iOS and Android

The app must feel like it was built by a top product studio for each platform, not generated. Every screen is judged against this section before it ships. **The Lab Report screens on the design canvas are the visual source of truth.** If a screen needs a component that isn't on the canvas or in this section, ask before inventing one.

### What "premium" means here, and what it never looks like

| Always | Never |
| --- | --- |
| Instant response to every tap (visual change under 100 ms) | Spinners in the middle of the screen |
| Content appears in place, nothing jumps (reserved space, skeletons) | Layout shift when data loads |
| One accent colour (#E5401F), used rarely and on purpose | Gradients, glows, glassmorphism inside the app, neon |
| Square, precise geometry: hairline rules, 1.5–2 px borders | Soft drop shadows on every card, pill buttons everywhere |
| Real copy from the spec, the user's own names | Placeholder text, lorem ipsum, generic "Welcome back!" |
| Platform-correct gestures, sheets, pickers, back behaviour | Web-style modals, custom date pickers, fake iOS on Android |
| Motion that explains (where something came from or went) | Bouncing for its own sake, confetti, emoji, mascots, stock illustrations |

### Stack (recommended for one codebase that still feels native)

| Need | Use |
| --- | --- |
| App framework | **Expo (latest SDK), React Native New Architecture, TypeScript.** Loveth is a separate app with its own accounts; reuse CoupleIn code only where it helps (e.g. the invite deep link). |
| Navigation | **expo-router** on native stacks (real iOS swipe-back, real Android predictive back) |
| Animation | **Reanimated** (springs, layout animations) + **Gesture Handler** |
| Haptics | **expo-haptics** (mapped below) |
| Server data | **TanStack Query** with a persisted cache, so every screen opens instantly from cache and refreshes silently |
| Local storage | **MMKV** for the cache and the offline tap queue |
| Subscriptions | **RevenueCat**: one API for App Store and Google Play trials, entitlements, and the Day-5 reminder trigger |
| Notifications | **expo-notifications** with actionable categories (Yes / No on the nightly tap, Yes / Give me a bit on Resolve) |
| Audio | **expo-audio** for Resolve recording, with the waveform from real input levels |
| Lists | **FlashList** for the agreements list and calendars |
| Fonts | Archivo (variable, with width axis) and IBM Plex Mono, bundled locally, never loaded at runtime |

### iOS vs Android: same design, platform-correct behaviour

| Element | iOS | Android |
| --- | --- | --- |
| Back | Edge swipe-back on every pushed screen | System back and predictive back gesture; same screens |
| Bottom sheets (Leave for now?, day details, Give me a bit) | Native sheet with detents and a grabber | Material 3 modal bottom sheet with a drag handle |
| Time picker (check-in time) | Native wheel picker | Native Material time picker (dial / keyboard) |
| Destructive confirm (Leave, End for today) | Native action sheet | Native Material dialog |
| Press feedback | Opacity 0.6 plus scale 0.98 | Material ripple (bounded, #0D0D0D at 12%) plus scale 0.98 |
| Status bar and edges | Safe areas, dark status bar content | Edge-to-edge (required on Android 15+), transparent bars, dark icons |
| Tab bar | Bottom tab bar, 49 pt plus home indicator inset | Bottom navigation, 80 dp, labels always shown |
| Share | Native share sheet | Native share sheet (Intent chooser) |
| Notifications | Actions on long-press; Time Sensitive for the Resolve request only | Actions shown inline; separate channels: Nightly tap, Partner, Resolve, Reminders |
| Text size | Dynamic Type up to Accessibility XL | Font scale up to 200% |

The visual design (colours, type, layout, components) is **identical** on both platforms. Only behaviour, system controls and gestures follow each platform.

### Design tokens

| Token | Light | Dark |
| --- | --- | --- |
| ink (text, primary buttons, bad-day square) | #0D0D0D | #F2F2EE |
| paper (screen background) | #F4F4F1 | #0E0E0F |
| surface (cards, good-day square) | #FFFFFF | #1A1A1C |
| muted surface (partner card) | #E9E9E4 | #232326 |
| rule (hairlines, track) | #D9D9D3 / #E2E2DC | #2C2C2F / #333336 |
| secondary text | #5E5E5A | #A3A39D |
| accent (signal only: badges, today ring, record) | #E5401F | #FF5A38 |
| missed | #B8B8B0 | #4A4A4D |

- **Dark mode:** good day = surface square with an ink border, bad day = filled ink square, so the meaning holds in both themes.
- **Type scale:** Display 44 (Archivo 800, width 78%, caps) · H1 32–36 (700, tracking −2%) · H2 24–27 (700) · Body 16–17 (400–500) · Small 13–14 · Label 10.5–12 (IBM Plex Mono 500, caps, tracking 8%).
- **Spacing:** 4-point grid; screen side margin 24; card padding 16–20; gaps 8 / 10 / 14 / 24.
- **Shape:** 0 radius for cards, buttons and squares (the Lab Report signature). Only avatars and the record button are round.
- **Touch targets:** at least 44 pt (iOS) / 48 dp (Android), including the close and pause icons.

**Warmth pass (Oct 2026), overrides the tokens above where they differ:**

- **Background stays the original white (#F4F4F1) with the original muted and rule colours. Warm paper was tried and reverted.**
- **Black has one meaning.** Black = a bad day (and the main button, which never sits beside the calendar). It is never used for a person. Avatars: initiator = warm sand #E7DAC6, partner = cool slate #D4DCE2, both with an ink initial. Once a photo is added it replaces the circle everywhere.
- **People's own words are set in a serif** (Newsreader, regular / italic): sealed love notes, the note editor, the "what I've noticed" note, and what the listener said back in Resolve. Everything the app says stays in Archivo. Signatures are serif italic ("— Sarah").
- **Milestones say MILESTONE**, plain mono, not an orange "unlocked" tag. The accent is kept for tonight, the seal and the live speaking dot.
- **The tap gets a moment.** On submit: the day's square fills in on the calendar (220 ms), a soft success haptic, and the button reads "Saved" for 600 ms before Done for tonight. No confetti.

### Motion

| Moment | Motion |
| --- | --- |
| Every press | Scale 0.98, spring back (stiffness 400, damping 30) |
| Screen push | Native platform transition (never a custom slide) |
| Report cards | Each card: headline fades and rises 12 px over 400 ms, detail follows 500 ms later; the dynamic name lands alone for 1 s |
| Nightly tap Yes / No | Selected button fills in 150 ms; Submit enables with a 200 ms fade |
| Day square (after tap) | The new square fills from the centre outwards over 300 ms |
| Milestones | The big number counts up from 0 in 600 ms, then the squares fill in sequence (40 ms apart) |
| 22 / 30 good days | Number counts up from yesterday's value |
| Take a break ring | Continuous, linear |
| Record waveform | Driven by real mic input levels at 30 fps |

Every animation respects **Reduce Motion** (iOS) and **Remove animations** (Android): swap movement for a simple 150 ms fade, and drop count-ups to the final number.

### Haptics

| Moment | iOS | Android |
| --- | --- | --- |
| Selecting an answer, Yes / No | Selection | Clock tick |
| Submit nightly tap | Success notification | Confirm |
| Good day revealed for you | Light impact | Light |
| Bad day revealed | None (never punish) | None |
| Milestone unlocked | Success, then heavy impact on the number | Confirm, then long press |
| Record start / stop | Medium impact | Context click |
| We're arguing right now | Medium impact | Context click |

### Loading: skeletons, never spinners

- **Rule:** if content takes longer than **300 ms**, show a skeleton in the exact shape and size of the final layout, so nothing moves when data arrives. Under 300 ms, show nothing extra.
- **Skeleton style:** blocks in the rule colour (#E2E2DC light / #2C2C2F dark), square corners, with a soft shimmer sweeping left to right every 1.2 s. With Reduce Motion: a static block that fades between two shades.
- **Cache first:** every screen renders instantly from the cached copy, then refreshes in the background. Skeletons should only ever appear on the very first load.

| Screen | Skeleton |
| --- | --- |
| Today | Header text bars, your-action card block (two text lines), partner card, two tiles, progress bar |
| Calendar | Both 90-square grids drawn as grey squares, name bars above |
| After the tap | Two day cards, then the grids |
| Resolve summary (AI) | Three cards with 2–3 text lines each, labelled *"Summarising…"*. Expected under 6 s; after 10 s: *"Taking longer than usual"* and **Try again** |
| Resolve solutions (AI) | Three option rows as skeletons |
| Report (first time) | Uses the 1G.4 *"Building your report…"* ticker instead of skeletons, because the wait is part of the delight |

- **Buttons that call the server** (Submit, Start my 7 free days): the label is replaced in place by a small inline progress indicator, the button keeps its size, and it never blocks the screen.

### Instant, offline-proof actions

- **Optimistic taps:** the nightly tap, Yes / No answers, notes and agreement answers update the UI immediately, then sync. If the sync fails, retry silently. After 3 failures, show a small *"Not synced yet. We'll keep trying."* line, never an error dialog.
- **Offline:** a slim banner under the header, *"You're offline. Taps will sync when you're back."* Taps go into the MMKV queue. Resolve AI steps and purchases need a connection, so they show *"Resolve needs a connection"* with **Try again**.

### Empty and error states (each designed, never blank)

| Situation | What shows |
| --- | --- |
| Partner not joined yet | Today partner card: *"Mark hasn't joined yet"* with **Resend invite** |
| No calendar history (day 1) | Grids with today ringed and the line *"Your first square fills in tonight."* |
| No agreements yet | You tab: *"Agreements you make in Resolve live here."* |
| Microphone permission denied | *"Resolve needs your microphone to hear you both"* with **Open settings** |
| Notifications off | Today banner with **Turn on**, using the system settings deep link |
| AI unavailable | Resolve still runs the speak and say-back steps; summaries and solutions show *"We couldn't summarise this one"* with 3 general options to pick from |
| Payment failed / pending | As specified in Stage 6 |

### Accessibility (part of premium, not extra)

- Every control has a VoiceOver / TalkBack label; icon-only buttons are named (*"Take a break"*, *"End session"*).
- Day squares announce their meaning (*"Day 12, good day"*), never just a colour.
- Text contrast at least 4.5:1; the accent is never used for body text.
- Layouts reflow at the largest text sizes: cards grow, nothing truncates mid-word, the two Today tiles stack vertically.

### Performance targets

- Cold start to Today, with cache: **under 1.5 s** on a mid-range phone (e.g. Pixel 7a, iPhone 13).
- 60 fps everywhere, 120 fps on ProMotion and high-refresh Android.
- No screen waits on more than one network request before rendering.

### Definition of done (every screen)

- [ ] Matches the canvas visually in light **and** dark mode
- [ ] Platform-correct back, sheets, pickers and press feedback on iOS **and** Android
- [ ] Skeleton (or instant cached render) and no layout shift
- [ ] Empty, error and offline states designed
- [ ] Haptics and motion as specified, with Reduce Motion handled
- [ ] VoiceOver and TalkBack labels; works at the largest text size
- [ ] Copy exactly as written in this spec, with real names filled in

## Data model

Lean on purpose: only what the app needs to work. All questionnaire answers live in one `answers` record per person, not as separate fields.

### Per user (BTC profile)

| Field | What it is |
| --- | --- |
| id | Anonymous account id until payment; upgraded in place to an Apple/Google account when they pay |
| name | From 1A.1, editable in You |
| auth\_provider | Apple or Google, set at payment; empty before |
| photo | Optional, replaces the initial |
| couple\_id | Their couple |
| role | initiator or partner |
| answers | Everything from the questionnaire, as one record |
| main\_action | The one thing the partner picked for them |
| own\_thing | Their own thing + start date + nights done |
| love\_note | Their sealed note to the partner |
| checkin\_time | Nightly check time |

### Per couple

| Field | What it is |
| --- | --- |
| id | Couple id |
| mode | couple or solo |
| invite\_link + invite\_status | sent / seen / joined / expired, with dates |
| test\_start | Day 1 of the 90-day test |
| subscription | plan, state, renews\_at, day5\_reminder\_sent\_at |
| last\_argument\_at | For the days-without-a-fight count |

### Per night (one row per person checked)

| Field | What it is |
| --- | --- |
| date | The night |
| about | Who was checked |
| result | good / bad / missed |
| note | Optional note for the partner |
| crossed\_line | Yes / no |
| argued\_today | Yes / no (feeds days without a fight) |
| own\_thing | yes / no / blank (private) |

### Per argument (Resolve)

| Field | What it is |
| --- | --- |
| date, together or apart | When and how |
| upset\_first | Who was upset (spoke first) |
| summaries | One calm summary per person (voice recordings deleted after) |
| agreement + day7\_result | What they agreed and whether it worked |

Check-in history and both picks are kept even if the subscription lapses, so a returning couple carries on where they stopped.

## Routes — Why are you here? (Oct 2026)

Loveth now has three routes. The first screen asks why they're here, and everything after it follows that answer. All three routes share the same spine (You, \[Partner\], the report, the daily action, the nightly check, Resolve, the paywall and the 90-day test). Only the problem questions, the pattern and the list of daily actions change.

| Route | Who it's for | Parts used (in order) | Questions |
| --- | --- | --- | --- |
| Break the cycle of fighting | Couples who keep having the same fight | 1A.1–1A.5 · Part B · Part C · Part D · Part E · Part G · own thing | 40 (42 on the "not sure" path) |
| Improve intimacy | Couples where closeness and sex have faded or become a fight | 1A.1–1A.3 · Part B · Part C · IN.1–IN.6 · IN.7–IN.8 · 1E.6 · Part G · own thing | 36 |
| The hard week (PMS or PMDD) | Couples where the same fight comes back in the week or two before a period | 1A.1–1A.4 · PM.0–PM.6 · Part B · Part C · 1E.1–1E.3 · 1E.5–1E.6 · Part G · own thing | 39 |

The question count is worked out from the route's screens, never typed in by hand, so the warning at 0.2 is always right. Optional text questions count.

### 0.1 Why are you here?

First screen on first open, for everyone. No progress bar, no back arrow.

Shows: "Why are you here?" · small line "Pick the one that matters most right now. You can change it later."

Options (each → 0.2): **Break the cycle of fighting** → route = fighting · **Improve intimacy** → route = intimacy · **The hard week**, with a small line underneath "PMS or PMDD" → route = cycle

Saves: route

Ad links: a Meta ad can open the app with the route already chosen (link parameter route=fighting, intimacy or cycle). Then 0.1 is skipped and the user lands on 0.2. If the parameter is lost on install, 0.1 shows as normal.

### 0.2 Are you serious? (reason 1)

The warning is shown straight after the route is picked, whenever the route has more than 15 questions. Every route has more than 15 today, so everyone sees it.

Shows:

- Label: the route name in caps (e.g. IMPROVE INTIMACY)
- Headline: "This is \[n\] questions."
- "That's about \[m\] minutes. We ask this many for two reasons. The first: Loveth only works for people who are serious about changing things. So, honestly:"

Options: **I'm serious** → 0.3 · **I'm just curious** → 0.2C

Saves: intent (serious / curious)

Minutes = questions × 7 seconds, rounded up to the next whole minute.

### 0.2C Just curious

Subtle exclusion: never rude, never pleading. It should feel like a door they're not ready to walk through yet.

Shows:

- Headline: "Loveth isn't for everyone."
- "It's for couples who are done having the same \[fight / distance / hard week\]. It takes honest answers, a check every night and 90 days of keeping your word."
- "Most people look around first. The ones who change things come back when they're ready."
- Small line: "We'll see you when you're ready."

Options: **Close** → closes the app; next open shows 0.1 · small text link **Actually, I'm serious** → 0.3

No drip messages are sent to someone who chose curious, unless they come back and choose serious.

### 0.3 Ready to go? (reason 2)

Replaces 1A.0. Same intent, now route-aware.

Shows:

- Headline: "The second reason: we need to fully understand what we're working on."
- Fighting: "There are 76 different patterns behind arguments, and we need to find yours." · Intimacy: "Closeness fades for different reasons, and the fix depends on which one is yours." · The hard week: "The hard week looks different in every couple, and so does the fix."
- Three lines, each with an icon: Answer honestly, not how you wish it was · Not sure? Say so. A wrong guess gives you the wrong fix · Your answers save as you go
- Small line: "The more specific you are, the more exact your result."

Options: **Ready to go** → notification pre-prompt (as 1A.0 had it) → 1A.1 · **Maybe later** → closes; next open shows 0.3 again

Saves: started\_at

### Rules for every route

These make all three routes work the same way and keep each one safe.

- **The route is never named outside the app.** Not in the invite, not in any push, not on the share card (report card 12), not in the store receipt. Intimacy and The hard week are private.
- **The suggestion comes from the route.** At 1G.1 the top suggestion and the two Also fits come only from the route's own list. More options still shows every daily action, so anything can be picked.
- **They still choose.** Nothing is assigned. The initiator picks for \[Partner\] at 1G.1 and \[Partner\] picks for the initiator at P4, from their own side's list.
- **Every route ends in the same mechanism.** One fixed daily action each, checked by the other every night, for 90 days. Every new action in this section follows the daily action rules (binary, daily, visible to the partner, the same for 90 days).
- **Route-aware copy.** Each route has its own pattern names, report lines, 4.0 copy, 1G.3 options and invite line (below). Everything else is shared.
- **Safety stays on every route.** 1E.6 (and P3 for the partner) is asked on all three routes. The intimacy route adds IN.8.
- **Changing route.** You → Change focus adds **Change what we're working on** → 0.1 → that route's questions, with shared answers (Part A, B, C) preselected → new report → pick → the 90-day test restarts. Same one-change-per-14-days limit.
- **Solo stays on the fighting route** for the MVP. The 1A.5 "Doing this on your own?" link only appears there. The Day 3 solo switch works on every route, using the type table.

### Route-aware copy

| Where | Fighting | Intimacy | The hard week |
| --- | --- | --- | --- |
| 1G.3 options | As now | To feel wanted again · To feel close again · Less pressure, more closeness · To stop feeling like flatmates | To get through the hard weeks without fighting · To feel understood · To stop walking on eggshells · To feel like a team |
| 4.0 body | As now (Gottman & Levenson) | "Left alone, distance in the bedroom rarely fixes itself. It turns into distance everywhere." No source line. | "Left alone, the same week every month becomes the same fight every month." No source line. |
| Paywall subline | As now | "You're at \[IN.1\]. You want \[motivation\]. Let's start." | "The hard week comes back every month. You want \[motivation\]. Let's start." |
| Invite (3.2), second sentence | "\[Me\] also thinks they've found the pattern behind your arguments." | "\[Me\] wants you two to feel closer, and thinks they've found what's in the way." | "\[Me\] has found something that could make things easier between you." |

## Route: Improve intimacy

For couples where sex and closeness have faded, or turned into a fight of their own. In the app it's always called intimacy, never "dead bedroom" (ads can use the phrase; it stings on your own phone).

Two rules that never bend:

- **No action ever obliges sex.** Every daily action is about affection, attention and how a no is handled. Never a number of times, never "have sex".
- **It works for both sides.** The person who wants more and the person who wants less get different questions and different actions, so neither is the problem.

### IN.1 How often now

Shows: "How often are you and \[Partner\] intimate at the moment?" · why-we-ask: "No judgement. We only use this to show you the change later." · "Private. \[Partner\] won't see this."

Options (each → IN.2): Not in months · Once a month or less · 2–3 times a month · About once a week · More than once a week

Saves: intimacy\_now

### IN.2 How often you'd like

Shows: "And how often would you like it to be?"

Options (each → IN.3): same five options, plus Honestly, I'm fine as it is

Saves: intimacy\_want

### IN.3 Who wants more

Shows: "Who usually wants more?"

Options (each → IN.4): Me → side = more · \[Partner\] → side = less · About the same → side = same · It's less about sex, more about feeling close → side = closeness

Saves: intimacy\_side. This decides the IN.5 list.

### IN.4 When it changed

Shows: "When did things change?"

Options (each → IN.5): After kids · Stress at work or with money · After a fight, or something that hurt · Slowly, no one moment · It's always been like this

Saves: intimacy\_change. "After a fight, or something that hurt" sets the pattern to The Cold War, whatever IN.5 says.

### IN.5 What gets in the way (branches by intimacy\_side)

Shows: "What gets in the way most?" One answer. Each answer gives 3 votes to its target and sets the pattern (unless IN.4 overrides it). Each → IN.6.

| Side | Answer | Target it votes for | Pattern |
| --- | --- | --- | --- |
| more (I want more) | \[Partner\] is always too tired | Kiss me for 30 seconds every day | Roommates |
|  | I'm always the one who starts things | Start affection with me once a day | The Pressure Loop |
|  | When \[Partner\] says no, it feels like rejection | Say no kindly | The Pressure Loop |
|  | I don't feel wanted any more | Tell me what you find attractive about me | Roommates |
|  | We never get time alone | Come to bed at the same time as me | Roommates |
|  | Phones in bed | Phone away in bed | Roommates |
|  | Things still feel raw from our fights | Make up within a day | The Cold War |
| less (\[Partner\] wants more) | Every touch feels like it's leading to sex | Touch me without it leading anywhere | The Pressure Loop |
|  | \[Partner\] sulks or goes cold when I say no | Don't sulk when I say not tonight | The Pressure Loop |
|  | I'm too exhausted. I do most of the work at home | Do their share without being asked | The Load |
|  | I don't feel close to \[Partner\] outside the bedroom | Give me real time every day | Roommates |
|  | \[Partner\] only notices me when they want something | Notice and appreciate me | The Pressure Loop |
|  | Things still feel raw from our fights | Make up within a day | The Cold War |
| same | We're both too tired | Kiss me for 30 seconds every day | Roommates |
|  | Neither of us makes the first move | Start affection with me once a day | Roommates |
|  | We never get time alone | Come to bed at the same time as me | Roommates |
|  | Phones in bed | Phone away in bed | Roommates |
|  | Too much on our plates | Do their share without being asked | The Load |
|  | Things still feel raw from our fights | Make up within a day | The Cold War |
| closeness | Less everyday affection than before | Show affection every day | Roommates |
|  | We never get time alone | Come to bed at the same time as me | Roommates |
|  | Phones in bed | Phone away in bed | Roommates |
|  | I feel taken for granted | Notice and appreciate me | Roommates |
|  | Too much on my plate to feel close | Do their share without being asked | The Load |
|  | Things still feel raw from our fights | Make up within a day | The Cold War |

Saves: intimacy\_sticking, intimacy\_pattern

### IN.6 The last time

Shows: "Think about the last time one of you reached for the other. In a few words, what happened?" · text field (up to 120 characters), optional

Options: Continue → IN.7 · Skip → IN.7

Saves: last\_time\_example (quoted on report card 8, as in the fighting route)

### IN.7 Your side (private)

Same screen as 1E.5 with intimacy options: Start things more often · Say no more kindly · Tell \[Partner\] what I like · Stop keeping count · Make more time for us · I'm not sure. → IN.8

Saves: self\_reflection

### IN.8 Pressure question (private)

Shows: "Do you ever feel pressured into sex or touch you don't want?" · "Private. \[Partner\] will never see this answer."

Options: No → 1E.6 · I'd rather not say → 1E.6 · Sometimes → IN.8S · Yes → IN.8S

Saves: pressure\_flag, with the same storage rules as safety\_flag (user only, never on the couple, never in analytics).

IN.8S support screen: same layout and rules as 1E.6S. "Nobody should feel pressured. This app isn't the right tool for that, but these people are. Free and confidential." Call Rape Crisis 24/7 Support Line → 0808 500 2222 · Call National Domestic Abuse Helpline → 0808 2000 247 · Quick exit · I picked the wrong answer. While pressure\_flag is true, opening Loveth shows IN.8S: no invite, no paywall. Verify both numbers before launch.

Then 1E.6 (the general safety question) → 1G.1 as normal.

### Intimacy patterns (report card 7 and the paywall bullet)

| Pattern | Description (card 7) | We'd guess… (card 6, when no dynamic is found) | This is fixable (card 9) | +1 vote |
| --- | --- | --- | --- | --- |
| The Pressure Loop | One of you reaches out, the other feels pressured and pulls back, so the first reaches out more. Both of you end up feeling rejected. | the last time one of you reached for the other, it ended with both of you feeling worse. | When touch stops meaning "sex next", the pressure goes, and wanting comes back. | Touch me without it leading anywhere |
| Roommates | No big fight, just less and less. Tired, busy, phones, and before you know it you're flatmates who love each other. | you go to bed at different times most nights. | Closeness is a habit, not a mood. Thirty seconds a day rebuilds it. | Kiss me for 30 seconds every day |
| The Cold War | Fights that never really ended are still in the room. It's hard to want someone you're still hurt by. | there's an argument from months ago neither of you has really let go. | Make up properly, and closeness has somewhere to come back to. | Make up within a day |
| The Load | One of you is carrying so much that there's nothing left at the end of the day, least of all desire. | one of you is still doing jobs when the other is already relaxing. | Lighten the load by one job a day and there's energy left for each other. | Do their share without being asked |

Report differences on this route: card 7 headline "Your pattern: \[intimacy pattern\]" with the description above (no fight frequency line) · card 8 "It's really about: \[sticking point\]" plus their own words from IN.6 · card 6 and 9 use the dynamic as normal when one is found, otherwise the pattern lines above · card 11 adds "Then: \[intimacy\_now\]. You want: \[intimacy\_want\]."

1G.1 on this route: top suggestion and Also fits come only from the intimacy list (every target in the IN.5 table, plus Show affection every day). **Kiss me for 30 seconds every day always appears in the top three.** What good looks like (1G.2) for the kiss is prefilled: "A proper kiss, not a peck. It doesn't have to lead anywhere."

### Partner flow on this route

The partner never sees the route name until they join. P1's black card reads: "\[Partner\] wants you two to feel closer. They've done their part." P3 includes IN.8 after the safety question. At P4, **Help me work it out** asks IN.3 and IN.5 from the partner's own side (they answer for themselves, never inferred from the initiator), then the list. **I know what I'd pick** goes straight to the intimacy list.

### Proof it's working (intimacy only)

At the 30 and 60 check-in milestones and on Day 90, each person is asked privately: "How often have you been intimate in the last month?" (IN.1 options). Shown back only once both have answered, as plain words: "When you started: once a month or less. Now: about once a week." Never as a score, never compared between partners. If it went down: "Closeness comes back slowly. Keep going." This is the number that shows the app is paying for itself.

### Your own thing on this route

| Side | Top suggestion (BEST FOR YOU) | Two more |
| --- | --- | --- |
| more | Ask \[Partner\] about their day before anything physical | Give one hug a day with nothing after it · Let a "not tonight" go without a sigh or a sulk |
| less | Reach for \[Partner\] once a day, even just a hug | Tell \[Partner\] one thing you like about them · If it's not tonight, say when might be better |
| same / closeness | Reach for \[Partner\] once a day, even just a hug | Phone down 30 minutes before bed · Tell \[Partner\] one thing you like about them |

## Route: The hard week (PMS or PMDD)

For couples where the same fight comes back in the week or two before a period. It names it from the first screen, because the people this is for already know, and they're motivated. It's never about blame, and never medical advice.

### PM.0 PMS and PMDD

Shows:

- Label: THE HARD WEEK · PMS OR PMDD
- Headline: "When the hard week brings the same fight."
- "PMDD (premenstrual dysphoric disorder) is a severe form of PMS that mainly affects mood in the week or two before a period. Either way, this route helps you handle that week together."
- "It's not about blame, and it's not medical advice."
- Consent: "Some answers here are about health. We keep them private: \[Partner\] never sees them." Checkbox **I agree**, required to continue.

Options: Continue (box ticked) → PM.1

Saves: health\_consent\_at. Health data is special-category data under UK GDPR: legal sign-off on the consent wording before launch.

### PM.1 Who has the hard weeks

Shows: "Who has the hard weeks?"

Options (each → PM.2): Me → who = me · \[Partner\] → who = partner · Both of us → who = both

Saves: cycle\_who. Copy on PM.2–PM.4 says "you" or "\[Partner\]" to match.

### PM.2 PMS or PMDD

Shows: "Is it PMS or PMDD?"

Options (each → PM.3): PMS · PMDD, diagnosed · I think it might be PMDD · Not sure

Might be or Not sure adds one line under the next screen's question: "A GP can check. Noting how \[you feel / Partner feels\] each day for two cycles is usually the first step."

Saves: cycle\_kind

#### PMS vs PMDD: what changes

PMDD here means "PMDD, diagnosed" or "I think it might be PMDD". PMS and Not sure follow the PMS column.

|  | PMS | PMDD |
| --- | --- | --- |
| Report, card 8 extra line | "PMS is common, and it's real. Handled together, the hard week gets easier." | "This isn't moodiness. PMDD is real, and it's hard on both of you. Handled together, it gets easier." |
| 1G.1 and P4, when the person with the hard weeks is picking | PM.5 order as written | The PM.5 answer stays the top suggestion. Don't put my mood down to my cycle and Take my feelings seriously fill the two Also fits places, because feeling disbelieved hurts most with PMDD |
| Hard week switch, how long it stays on | From PM.3 | From PM.3, never less than 10 days |
| Support pushes | The 21-line sets below | The same 21-line sets, running at least 10 days |
| Support | Samaritans card only if Feeling low or tearful is picked at PM.4 | Samaritans card at PM.4, plus a permanent Support row in You → Help: Samaritans 116 123 · talk to your GP |

Neither version gives medical advice or suggests treatment. Verify the Samaritans number before launch.

### PM.3 How long before

Shows: "How many days before a period do things change?"

Options (each → PM.4): A few days · About a week · Up to two weeks · It varies

Saves: cycle\_window (sets how long Hard week stays on, below)

### PM.4 What changes

Shows: "What changes most? Pick up to 2."

Options (multi-select, max 2): Snapping over small things · Feeling low or tearful · Feeling unloved or pushed away · Needing space · Everything feels like too much · Anger that feels bigger than the problem

Continue → PM.5. If Feeling low or tearful is picked, or cycle\_kind is PMDD (diagnosed or might be), a support card shows once before PM.5: "If it ever feels like too much, you don't have to wait for the week to pass. Samaritans, free, any time: 116 123. Your GP can help too." Options: Call Samaritans → dialler · Continue → PM.5.

Saves: cycle\_changes

### PM.5 What makes it worse (branches by cycle\_who)

Shows: "When the hard week hits, what makes it worse?" One answer. Each answer gives 3 votes to its target. Each → PM.6.

| Who has it | Answer | Target it votes for |
| --- | --- | --- |
| me | \[Partner\] says it's "just your period" | Don't put my mood down to my cycle |
|  | \[Partner\] takes it personally and fights back | Ask what I need before reacting |
|  | \[Partner\] leaves me alone with it | Ask how I'm really doing |
|  | \[Partner\] doesn't believe it's real | Take my feelings seriously |
|  | Nothing changes at home when I'm struggling | Do their share without being asked |
|  | What I said gets held against me afterwards | Leave the past in the past |
| partner | Things get said that really hurt | Tell me you're struggling, don't take it out on me |
|  | I never know what's coming | Don't leave me guessing |
|  | Small things blow up fast | Keep a calm voice |
|  | \[Partner\] shuts me out | Tell me when they need quiet, instead of going silent |
|  | It never gets talked about afterwards | Come back and talk it through |
| both | We both get snappy at the same time | Keep a calm voice |
|  | Neither of us asks what the other needs | Ask how I'm really doing |
|  | Things get said that really hurt | Tell me you're struggling, don't take it out on me |
|  | We blame everything on our cycles | Don't put my mood down to my cycle |
|  | Nothing gets talked about afterwards | Come back and talk it through |

Saves: cycle\_sticking

### PM.6 The last time

Shows: "Think about the last hard week. In a few words, what happened?" · text field (up to 120 characters), optional. Continue or Skip → 1B.0

Saves: last\_time\_example

Then Part B, Part C, 1E.1–1E.3 (with the why-we-ask line "When the hard week hits, how do your fights go?"), 1E.5, 1E.6, Part G. The cycle from 1E.1–1E.3 votes and names the pattern as normal.

### Report differences on this route

Card 7: "Your hard-week pattern: \[cycle name\]" with the cycle description · card 8: "It's really about: \[sticking point\]" plus their own words · cards 6 and 9 use the dynamic if found, otherwise the cycle lines (already in the spec). The words PMS and PMDD appear on card 8 only, never on the share card.

1G.1: top suggestion and Also fits come only from the PM.5 list for that side, plus the cycle's target.

### Hard week (this route only)

Hard weeks are hard on both people, and often the partner is the most exhausted. **Each person has their own Hard week switch** on Home, and either can turn theirs on when it starts. Nothing about the cycle is tracked or predicted, and it's never on by default.

|  | How it works |
| --- | --- |
| What starts | When either switch goes on, support pushes start for **both** people (Support pushes, below) |
| What each person sees | Only their own switch. Turning yours on never turns the other person's on, so nobody can tell who started it. Under the switch: "Only you see this switch. Turning it on starts support for you both. Nobody is told." First tap: a sheet, "This starts kind reminders for you both. \[Name\] won't know it was you, and no message ever says why." · Got it |
| Support card and sheet | Shown to the partner of the person with the hard weeks while support is running, whoever turned it on |
| How long | The PM.3 window (a few days = 4, about a week = 7, up to two weeks = 14, it varies = 10; PMDD never less than 10). Support stops when the window ends, or when everyone who turned a switch on has turned it off. Turning your own switch off never stops support the other person started. Either person can mute their own pushes in You → Notifications |

#### Support pushes (both people)

It doesn't matter who presses Hard week. Once it's on, support pushes start for **both** people: three a day each, all different for 7 days (21 each), every one with the other person's name. Each set has one job: stop a fight before it starts, and remind them they're loved. On longer windows, day 8 starts the set again from day 1.

Rules: title is always "Loveth". **Lock-screen safe:** no line mentions a hard week, a period, PMS, PMDD or who pressed the switch. Times are each person's local time. Paused only while Resolve is running (that line moves to the next slot). \[your note phrase\] = a chip phrase from the note they sealed (3.1 or P2); \[their note phrase\] = from the note the other person sealed for them. If a note is missing, the fallback line is used. No emoji. Copy never uses he/she: always the name.

**For the partner** (\[Name\] = the person with the hard weeks)

| Day | 08:00 · Start soft | 13:00 · A small gesture | 18:00 · The home stretch |
| --- | --- | --- | --- |
| 1 | Good morning. Today's only goal: no fight with \[Name\]. You don't have to win anything. | Send \[Name\] a sweet text right now. Two words is enough: 'Love you.' | Heading home to \[Name\]? Walk in calm. First words: 'How was your day?' |
| 2 | Remember why you love \[Name\]. You wrote it yourself: "\[your note phrase\]". | Plan to pick up \[Name\]'s favourite treat on the way home today. Small things say 'I'm on your side'. | If something sharp comes from \[Name\] tonight, don't answer the words. Answer the person. |
| 3 | \[Name\] loves you. Even on the days it doesn't sound like it. | Text \[Name\]: 'Proud of you.' No reason needed. | Tonight, ask \[Name\] one thing: 'What would help right now?' Then do just that. |
| 4 | Start the day with a hug for \[Name\]. No words needed. | \[Name\] wrote to you: "\[their note phrase\]". Still true today. | Feeling it heat up with \[Name\]? Say 'I need 20 minutes' and come back. That's not losing. |
| 5 | Be the calm one for \[Name\] today. It's the most loving thing you'll do. | Make \[Name\] a cup of tea today without being asked. Small things land big right now. | Don't go to bed on a fight with \[Name\]. One 'I love you' closes the day. |
| 6 | \[Name\] chose you, and still does. Carry that into today. | Send \[Name\] a photo of the two of you. Remind \[Name\] who you are together. | Tired? With \[Name\] tonight, kind beats right. |
| 7 | Seven days of keeping the peace with \[Name\]. That's love in action. | Plan something small for you and \[Name\] this weekend. Something to look forward to helps. | You kept the peace with \[Name\] today. That's love too. Sleep well. |

**For the person with the hard weeks** (\[Name\] = their partner). If both have hard weeks, both get this set.

| Day | 08:00 · Start soft | 13:00 · A small gesture | 18:00 · The home stretch |
| --- | --- | --- | --- |
| 1 | Good morning. \[Name\] loves you. You wouldn't be doing Loveth together if \[Name\] didn't. | Text \[Name\]: 'Glad it's you.' It'll make \[Name\]'s day. | If it starts to rise tonight, tell \[Name\]: 'It's not you, it's today.' Then breathe. |
| 2 | Remember why you chose \[Name\]. You wrote it yourself: "\[your note phrase\]". | \[Name\] once wrote to you: "\[their note phrase\]". \[Name\] still means it. | Need space tonight? Tell \[Name\] 'I need 20 minutes' instead of going quiet. \[Name\] will understand. |
| 3 | Be gentle with yourself today. \[Name\] is on your side. | Send \[Name\] a sweet text. Two words: 'Love you.' | Snapping at \[Name\] isn't who you are. Say how you feel instead. \[Name\] can handle the truth. |
| 4 | Today's goal: no fight with \[Name\]. You're on the same team. | Ask \[Name\] for a hug when you need one. Asking is strong, not needy. | Before you react tonight, ask yourself: is this about \[Name\], or about today? |
| 5 | Every calm moment with \[Name\] counts. Today's no different. | Thank \[Name\] for one small thing today. It means more than you think. | If something came out wrong with \[Name\], say sorry tonight, not tomorrow. Short and real is enough. |
| 6 | You're not too much. \[Name\] loves you, all of you. | Send \[Name\] a photo that makes you smile. Let \[Name\] in on your day. | Let \[Name\] look after you tonight. Saying yes to help is love too. |
| 7 | \[Name\] chose you, and still does. Start today knowing that. | Plan something small with \[Name\] for the weekend. Something to look forward to helps you both. | You and \[Name\] made it through today together. That's what counts. Sleep well. |

Fallbacks when a note is missing: partner day 2 morning → "Remember why you fell for \[Name\]. Think of one reason before the day starts." · partner day 4 midday → "Tell \[Name\] one thing you love about \[Name\] today. Out loud." · person with the hard weeks day 2 morning → "Remember why you chose \[Name\]. Think of one reason before the day starts." · day 2 midday → "Text \[Name\] a thank-you for something small today."

#### Partner support mode

For the person living with someone else's hard week. It runs for the window above, then stops on its own.

- **Support pushes for both people**, three a day each (Support pushes, below).
- **A support card on Home** while it's on: "Your week · day \[n\] of \[window\]" (never the words hard week, so a glance at the screen gives nothing away), the latest push line, and three buttons: **Take 20 minutes** (the Resolve break timer, just for them) · **We're arguing right now** (Resolve) · **It's a lot for me too** (opens the partner support sheet).
- **Partner support sheet:** "Living with a hard week is exhausting. That's real, and it doesn't make you a bad partner." · what helps (keep your own action, don't argue the point, ask what's needed, look after yourself) · "If it's getting too much for you too, Samaritans are free, any time: 116 123." · Got it.
- **The nightly check is unchanged.** Hard weeks don't pause the 90-day test or excuse anyone's action, but the C4 bad-day screen adds one line during a hard week: "Hard weeks are part of it. What counts is the trend."

#### Recognising the partner

- **Report (initiator is the partner of the person with the hard weeks):** card 9 adds "And you've been carrying a lot too. Loveth supports you when the hard week starts."
- **Partner flow (the person who joins is the partner of the person with the hard weeks):** P5 reveal adds "Hard weeks are hard on you too. When one starts, tap Hard week and we'll support you."
- **Own thing:** the partner list above already includes "Don't take a snap personally: let it go, talk later".

Data: hard\_week {started\_by, start, end}. Never shown on the calendar, never in analytics with the route name, never in any push text beyond the copy above.

### Partner flow on this route

The invite never mentions PMS or PMDD. P1's black card reads: "\[Partner\] has found something that could make the hard weeks easier for you both." At P4 the partner picks from the opposite side's list: if the initiator said me, the partner gets the partner list; if partner, the me list; if both, the both list. P4 also has a small link **This isn't about hard weeks for us** → the full fighting list with Help me work it out, so nobody is pushed into a label they don't accept.

### Your own thing on this route

| Who | Top suggestion (BEST FOR YOU) | Two more |
| --- | --- | --- |
| Has the hard weeks (including both) | On a hard day, tell \[Partner\] before it comes out sideways | When a hard week starts, turn on Hard week so \[Partner\] knows · After a snap, say sorry the same day |
| Partner of someone who does | On a hard day, ask what \[Partner\] needs before reacting | Do one extra job on a hard day without being asked · Don't take a snap personally: let it go, talk later |

## Path check (Oct 2026)

Every answer on every route was traced to the daily action it ends in, and each action was checked against the daily action rules: binary, checkable every day (a Don't is a good day if it didn't come up; a conditional Do says what counts as a good day when it didn't come up), visible to the person checking, and the same for 90 days.

| Route | Paths checked | Result |
| --- | --- | --- |
| Fighting (sticking points, scenarios, dynamics, cycles, start-doing list) | 97 | 5 broken links and 2 gaps, all fixed below |
| Intimacy (4 sides × their answers, 4 patterns) | 29 | All end in a valid daily action |
| The hard week (3 sides × their answers) | 16 | All end in a valid daily action |
| Your own thing (all route suggestions) | 15 | All daily and relationship-scoped |

Fixed in the fighting route:

- **Start-doing list:** three items didn't match any daily action, so the app would have had nothing to show. Now: Tell me what they appreciate about me · Ask about my day before picking up their phone · Plan time for just us every week · Say thanks for what I do · Give me 10 minutes of real conversation after work · Write my own.
- **D1 vote** didn't match its action's exact text. Now votes for Say "I need 20 minutes" and come back.
- **D4r vote** didn't match. Now votes for Tell me what they really think.
- **Money action** used £\[amount\], but no screen ever asked for it. Now picking that action at 1G.1 (or P4) asks "Over what amount?" £50 · £100 · £250 · Other, saved as money\_amount.
- **1D.13 Walking away mid-conversation** pointed at the going-silent action. It now votes for Say "I need 20 minutes" and come back, which is the behaviour described.

## Stage 1 — Getting to the exact problem

One person makes this decision alone. They will only trust us if, by the end, we have described *them*, *their partner* and *their exact problem* better than they could themselves. So Stage 1 learns about three things in order: who you are, who \[Partner\] is (as you see them), and the specific problem. Then it joins them up in a personal report that explains *why* your fights go the way they do.

- **Length:** 30–38 screens, about 4 minutes. Tap answers only, except names and optional text.
- **Screen IDs** in this stage use the part letter: 1A.1, 1B.3 and so on.
- **Progress bar** uses the route's parts (see Navigation).
- **A "why we ask" line** sits under the first question of each part (copy given below), so the length feels purposeful.
- **Every "this or that" question** also offers **Somewhere in between**, so nobody is forced into a box.

### Part A — You two

#### 1A.0 Before we start (replaced by 0.3, see Routes)

Sets expectations: this works because it narrows down the exact issue, and that takes honest answers and a few minutes. Users who opt in here are the ones who finish.

- **Shows:**
  - Headline: *"This isn't a quick quiz."*
  - *"To find what's really behind your arguments, we'll ask about you, your partner and how your fights actually go. There are 76 different patterns, and we need to find yours."*
  - Three lines, each with an icon: **Answer honestly**, not how you wish it was · **Not sure? Say so.** A wrong guess gives you the wrong fix · **Take your time.** About 4 minutes, and your answers save as you go
  - Small line: *"The more specific you are, the more exact your result. Rushed answers get a generic one."*
- **Options:** **I'm ready to dig in** → notification permission (pre-prompt: "We'll save your answers and remind you if life gets in the way." → system prompt) → 1A.1 · **Not now** → closes; next open shows 1A.0 again
- **Saves:** started\_at

#### 1A.1 Partner's name

- **Shows:** *"First, who are we doing this with?"* · text field, placeholder *"Their first name"*
- **Options:** **Continue** (1–30 characters) → 1A.2 · **X** → exits, nothing saved
- **Saves:** partner\_first\_name, role = initiator

#### 1A.2 How long together

- **Shows:** *"How long have you and \[Partner\] been together?"*
- **Options (each → 1A.3):** Less than a year · 1–3 years · 3–10 years · More than 10 years
- **Saves:** together\_length

#### 1A.3 Living together

- **Shows:** *"Do you live together?"*
- **Options (each → 1A.4):** Yes, just us · Yes, with kids · Not yet
- **Saves:** living

#### 1A.4 How often

- **Shows:** *"How often do you and \[Partner\] argue?"*
- **Options (each → 1A.5):** Every day · A few times a week · About once a week · Less than once a week
- **Saves:** frequency

#### 1A.5 The fork

- **Shows:** *"If \[Partner\] could change one thing, do you know what it would be?"*
- **Options (each → 1B.0):**
  - **Yes, I know exactly** → sets path = known
  - **I have an idea** → sets path = known
  - **Honestly, I'm not sure. It's just always tense** → sets path = unsure
- **Saves:** path. This decides which version of Part D the user gets. Everyone does Parts B and C.

### Part B — About you

This is where the user starts to feel understood. Every question is about *them*, not the relationship. Single choice, each answer → next screen.

#### 1B.0 Your style

- **Shows:** *"Let's start with you. Four quick this-or-that questions to work out how you argue."* · why-we-ask line: *"Most fights aren't about the topic. They're about two different people wired differently."*
- **Options:**
  - Continue → 1B.1. No "I already know my type" shortcut: we never ask for, show or name four-letter personality types (trademark). Our own system only.
- **Saves:** nothing on this screen

#### 1B.1–1B.4 Your style (four this-or-that questions)

Each question sets one of our four axes: **Recharge** (Out / In), **Focus** (Facts / Big picture), **Decide** (Head / Heart), **Pace** (Planned / Flexible). "Somewhere in between" stores the axis as balanced and the report uses the balanced wording. This is Loveth's own system: no third-party type names, letters or descriptions anywhere in the app, store listing or ads.

| Screen | Question | Option A → axis | Option B → axis |
| --- | --- | --- | --- |
| 1B.1 | After a long, draining day, what recharges you? | Being around people, talking it out → Out | Quiet time on my own → In |
| 1B.2 | When \[Partner\] explains a problem, what do you want first? | The facts: what happened, exactly → Facts | The bigger picture: what it means for us → Big picture |
| 1B.3 | In the middle of a disagreement, what matters more to you? | Getting to what's fair and logical → Head | Feeling understood → Heart |
| 1B.4 | Plans change at the last minute. You… | Get thrown. I like knowing what's happening → Planned | Roll with it → Flexible |

- **Saves:** into the person's one `answers` record.
- Note for the report: the person is shown as their argument type (e.g. The Keeper) with a plain-English description. Never four letters. It's a style, never presented as a diagnosis.

#### 1B.5 How you fight

- **Shows:** *"When an argument starts, what do you usually do?"*

| Option | Saves conflict\_style |
| --- | --- |
| Push to sort it out right now | pursuer |
| Need space before I can talk | withdrawer |
| Go along with it to keep the peace | peacekeeper |
| Dig in. I don't back down when I'm right | defender |
| Look for a middle ground quickly | compromiser |

#### 1B.6 What you need when you're upset

- **Shows:** *"When you're upset, what do you most want from \[Partner\]?"*
- **Options → my\_upset\_need:** Comfort: a hug, reassurance · Just listen, let me vent · Help me fix the problem · Give me space · An apology

#### 1B.7 What makes you feel loved

- **Shows:** *"What makes you feel most loved?"*
- **Options → my\_love\_style:** Hearing it: compliments, "I love you" · Time together, properly present · Help without being asked · Hugs, closeness, touch · Thoughtful little gifts or surprises

#### 1B.8 What gets under your skin

- **Shows:** *"What gets under your skin fastest?"*
- **Options → my\_trigger:** Being ignored · Being criticised · Being told what to do · Things being unfair · Being lied to · Feeling rushed

#### 1B.9 You under stress

- **Shows:** *"Be honest: how do you act when you're stressed?"*
- **Options → my\_stress:** Go quiet · Get snappy · Overthink everything · Keep busy and avoid it

#### 1B.10 After a fight

- **Shows:** *"After a fight, what do you need to feel okay again?"*
- **Options → my\_repair:** To talk it all through · A proper apology · Time on my own · For things to go back to normal without a big talk

#### 1B.11 How long it takes

- **Shows:** *"And how long does that usually take?"*
- **Options → my\_recovery:** Minutes · A few hours · About a day · Several days

### Part C — About \[Partner\], as you see them

The same questions, answered about the partner. Comparing the two sets is what produces the insight (Part F). Every question here also has **I'm not sure** (stored as unknown and left out of the comparison).

#### 1C.0 Intro

- **Shows:** *"Now \[Partner\]. Answer how \[Partner\] comes across to you. There are no wrong answers."* · why-we-ask line: *"\[Partner\] will answer for themselves when they join. You might be surprised how well you know each other."*
- **Options:** **Continue** → 1C.1 · **I know \[Partner\]'s type** → 16-type grid → 1C.5

| Screen | Question | Options | Saves |
| --- | --- | --- | --- |
| 1C.1 | After a long day, what recharges \[Partner\]? | People and talking (E) · Time alone (I) · In between · Not sure | partner\_type, letter 1 |
| 1C.2 | When you raise a problem, what does \[Partner\] go for first? | The facts and details (S) · The bigger picture (N) · In between · Not sure | partner\_type, letter 2 |
| 1C.3 | In a disagreement, what does \[Partner\] care about more? | What's fair and logical (T) · Feeling understood (F) · In between · Not sure | partner\_type, letter 3 |
| 1C.4 | When plans change last minute, \[Partner\]… | Gets thrown (J) · Rolls with it (P) · In between · Not sure | partner\_type, letter 4 |
| 1C.5 | When an argument starts, \[Partner\] usually… | Pushes to sort it now · Needs space first · Goes along to keep the peace · Digs in · Looks for middle ground · Not sure | partner\_conflict\_style |
| 1C.6 | When \[Partner\] is upset, what do they want from you? | Comfort · To vent · A fix · Space · An apology · Not sure | partner\_upset\_need |
| 1C.7 | What makes \[Partner\] feel most loved? | Hearing it · Time together · Help · Touch · Little gifts · Not sure | partner\_love\_style |
| 1C.8 | What gets under \[Partner\]'s skin fastest? | Being ignored · Being criticised · Being told what to do · Unfairness · Being lied to · Feeling rushed · Not sure | partner\_trigger |
| 1C.9 | How does \[Partner\] act when stressed? | Goes quiet · Gets snappy · Overthinks · Keeps busy · Not sure | partner\_stress |

Each answer → next screen. 1C.9 → 1D.1 (path = known) or 1D.10 (path = unsure).

**When \[Partner\] joins**, they answer Part B about themselves (see Partner flow). Their own answers replace the guesses for the insight, and both see a **How well do you know each other?** card: *"You got 6 of 9 right about \[Partner\]."*

### Part D — The exact problem

Two routes to the same place: one specific behaviour. People who know the problem name it in 3 taps. People who don't answer six scenario questions, and the answers that point the same way reveal it for them.

#### Route 1 — "I know" (path = known)

##### 1D.1 What it's about (pick up to 3)

- **Shows:** *"What do your arguments start over? Pick up to 3."* · why-we-ask: *"The topic is just the doorway. We'll find what's really behind it."* Multi-select chips; a 4th tap shows *"Pick your top 3"* and is ignored.
- **Options:** Chores and fairness · Not feeling listened to · How things are said · Money · Phones and attention · Family and friends · Feeling less close · Little things that turn big
- **Continue** (1+ picked) → 1D.2 if 2–3 picked, → 1D.3 if 1 picked
- **Saves:** topics

##### 1D.2 The one that hurts most

- **Shows:** *"Which one hurts the most?"* Only the topics picked at 1D.1. Each → 1D.3
- **Saves:** main\_topic

##### 1D.3 The sticking point (branches by main\_topic)

- **Shows:** *"What's the real sticking point with \[main\_topic\]?"* The answers for that topic (four to seven). Each → 1D.4
- **Saves:** sticking\_point. Each answer gives 2 votes to its target (scoring in Part G).

| main\_topic | Sticking point | Target it votes for |
| --- | --- | --- |
| Chores and fairness | \[Partner\] does less than their share | Do their share without being asked |
|  | I have to ask every single time | Notice what needs doing and do it |
|  | What I do never gets noticed | Say thanks for what I do |
|  | Jobs get started but not finished | Finish what they start |
| Not feeling listened to | \[Partner\] interrupts me | Listen without interrupting |
|  | \[Partner\] gets defensive | Hear me out without getting defensive |
|  | \[Partner\] turns it back on me | Don't turn the blame back on me |
|  | \[Partner\] changes the subject | Stay on topic |
|  | \[Partner\] is on the phone while I talk | Put the phone down when we talk |
|  | My feelings get brushed off | Take my feelings seriously |
|  | \[Partner\] jumps straight to fixing it | Listen first, fix later |
| How things are said | Constant criticism | Stop the criticism |
|  | Being told what to do | Ask, don't tell |
|  | Bringing up the past | Leave the past in the past |
|  | Sarcasm | Say it straight, no sarcasm |
|  | Raised voice | Keep a calm voice |
|  | Eye-rolling and sighing | Drop the eye-rolls and sighs |
|  | Criticising me in front of others | Keep criticism private |
| Money | Spending without talking first | Check with me before big spends |
|  | Keeping money things from me | Be open about money |
|  | We want different things for our money | Talk about money calmly, not in a fight |
|  | Who earns more comes up in arguments | Leave earnings out of arguments |
| Phones and attention | Phones at meals | No phones at meals |
|  | Phones in bed | Phone away in bed |
|  | Phones during conversations | Put the phone down when we talk |
|  | Scrolling instead of time together | Give me real time every day |
| Family and friends | \[Partner\] takes their side over mine | Back me up in front of others |
|  | Too much time with them, not enough with me | Make time for us first |
|  | Disrespecting my family | Speak kindly about my family |
|  | Agreeing to plans without asking me | Check with me before saying yes to plans |
| Feeling less close | Not enough time together | Plan time for just us every week |
|  | Less affection than before | Show affection every day |
|  | Feeling taken for granted | Notice and appreciate me |
|  | Everything's about what \[Partner\] wants | Ask what I'd like to do |
| Little things that turn big | Running late | Be on time, or tell me early |
|  | Forgetting what we agreed | Remember what we agreed |
|  | Leaving mess | Tidy up after themselves |
|  | Changing plans last minute | Stick to the plans we make |

##### 1D.4 The last time

- **Shows:** *"Think about the last time this happened. In a few words, what did \[Partner\] do?"* · text field (up to 120 characters), optional
- **Options:** **Continue** → 1D.5 · **Skip** → 1D.5
- **Saves:** last\_time\_example. Quoted back on the report so the user sees their own words.

#### Route 2 — "I'm not sure" (path = unsure)

Six scenario questions about real moments. People answer honestly about a scene more easily than about a label. Every option votes for one target; **None of these** is a real answer (no vote, counted for the "mostly none" rule in Part G). A **Skip** link under each question also casts no vote. Each answer → next screen; 1D.15 → 1D.5.

| Screen | Question | Option → target it votes for (1 vote) |
| --- | --- | --- |
| 1D.10 | Think about your last proper argument. What did \[Partner\] do that made it worse? | Interrupted or talked over me → Listen without interrupting · Got defensive → Hear me out without getting defensive · Brushed it off → Take my feelings seriously · Turned it back on me → Don't turn the blame back on me · Went silent or walked off → Stay in the conversation, even when it's hard · Raised their voice → Keep a calm voice |
| 1D.11 | When you bring up something that's bothering you, \[Partner\] tends to… | Get defensive → Hear me out without getting defensive · Play it down → Take my feelings seriously · Bring up something I did → Don't turn the blame back on me · Change the subject → Stay on topic · None of these |
| 1D.12 | What stings most about how \[Partner\] talks to you in an argument? | Sarcasm → Say it straight, no sarcasm · Raised voice → Keep a calm voice · The silent treatment → Stay in the conversation, even when it's hard · Eye-rolls and sighs → Drop the eye-rolls and sighs · None of these |
| 1D.13 | What turns a small thing into a big fight fastest? | Bringing up the past → Leave the past in the past · Raised voices → Keep a calm voice · Walking away mid-conversation → Say "I need 20 minutes" and come back · Not paying attention, phone out → Put the phone down when we talk · None of these |
| 1D.14 | When you're venting about your day, \[Partner\]… | Jumps straight to fixing it → Listen first, fix later · Turns it to their own day → Keep the focus on me when I'm upset · Looks at their phone → Put the phone down when we talk · Says I'm overreacting → Take my feelings seriously · None of these |
| 1D.15 | After a fight, what do you wish \[Partner\] did? | Said sorry first sometimes → Say sorry first sometimes · Came back and talked it through → Come back and talk it through · Didn't sulk for days → Make up within a day · Actually changed what caused it → Follow through on what we agree · None of these |

#### Both routes

##### 1D.5 When it happens

- **Shows:** *"When do most arguments happen?"*
- **Options (each → 1E.1):** Evenings after work · Mornings · Weekends · Over text · When one of us is tired or hungry · Any time
- **Saves:** when\_argue

### Part E — How your fights play out

#### 1E.1–1E.3 Start, middle, end (sets the cycle)

- **Why-we-ask (on 1E.1):** *"Every couple has a pattern. Three questions and we'll name yours."*
- Each answer carries a cycle tag. Each answer → next screen; 1E.3 → 1E.4.

| Screen | Question | Answer | Cycle tag |
| --- | --- | --- | --- |
| 1E.1 | How does it usually start? | Something small snaps and it blows up | buildup |
|  |  | Things I've bottled up all come out at once | buildup |
|  |  | One of us brings up something from the past | replay |
|  |  | One of us goes quiet and the other pushes | shutdown |
|  |  | A comment comes out the wrong way | shouting |
| 1E.2 | What happens in the middle? | We both get louder | shouting |
|  |  | It gets personal | shouting |
|  |  | Old arguments come back up | replay |
|  |  | One of us shuts down or walks off | shutdown |
|  |  | I hold back what I really feel | buildup |
| 1E.3 | How does it usually end? | Silence for hours or days | shutdown |
|  |  | It fades and nobody says sorry | buildup |
|  |  | We make up, but it happens again | replay |
|  |  | One of us always gives in | buildup |
|  |  | Someone storms off | shouting |

- **Cycle rule:** the tag that appears most wins. If all three differ, the 1E.2 tag wins. **Saves:** cycle\_type.

#### 1E.4 Who makes up first

- **Shows:** *"Who usually makes the first move to make up?"*
- **Options (each → 1E.5):** Me · \[Partner\] · It depends · Nobody really
- **Saves:** first\_mover

#### 1E.5 Your side (private)

- **Shows:** *"Be honest: what could you do better?"* · *"Private. \[Partner\] won't see this."*
- **Options (each → 1E.6):** Be more patient · Raise things sooner instead of bottling them up · Listen more · Keep my tone calmer · Let go of the past · Give \[Partner\] space when they need it · I'm not sure
- **Saves:** self\_reflection (never shown to the partner)

#### 1E.6 Safety question (private)

- **Shows:** *"Do you ever feel afraid of \[Partner\], or that \[Partner\] controls who you see or what you spend?"* · *"Private. \[Partner\] will never see this answer."*
- **Options:** No → 1G.1 · I'd rather not say → 1G.1 · Sometimes → 1E.6S · Yes → 1E.6S
- **Saves:** safety\_flag = true for Sometimes or Yes, otherwise false. Stored on the user only, never on the couple record, never sent to the partner, never in analytics.

#### 1E.6S Support screen

- **Shows:** *"You deserve to feel safe. This app isn't the right tool for that, but these people are. Free and confidential."* No progress bar, no back arrow.
- **Options:**
  - **Call National Domestic Abuse Helpline (24 hours)** → phone dialler, 0808 2000 247
  - **Call Men's Advice Line** → phone dialler, 0808 801 0327
  - **Call Galop (LGBT+)** → phone dialler, 0800 999 5428
  - **Quick exit** → closes Loveth immediately
  - **I picked the wrong answer** → back to 1E.6 with nothing selected; clears safety\_flag
- **Rule:** while safety\_flag is true, opening Loveth shows 1E.6S. No invite, no paywall.

### Part F — The insight engine (no screens, runs after 1E.6)

This is the logic that turns answers into the "that's exactly us" moment. It compares the user's answers (Part B) with how they see \[Partner\] (Part C), finds the clashes, and names them. Each clash also casts votes for the one thing (Part G). Any comparison where either side is "Not sure" or "In between" is skipped.

#### Personality lines

The report describes each person in plain English, one phrase per letter, joined into one sentence: *"You \[phrase 1\], \[phrase 2\], \[phrase 3\] and \[phrase 4\]."* Their argument type shows small underneath (e.g. THE KEEPER).

| Letter | Phrase |
| --- | --- |
| E | recharge by being around people |
| I | recharge with quiet time alone |
| S | go by the facts |
| N | think in the bigger picture |
| T | lead with logic and fairness |
| F | lead with feelings |
| J | like things settled and planned |
| P | like to go with the flow |
| X (in between) | are a bit of both on \[that axis\] |

#### Named dynamics

Check every row. A row is **found** when its condition is true. "Me" = the user's answer, "P" = how they see \[Partner\].

| # | Name | Condition | Report copy | Votes for \[Partner\]'s one thing |
| --- | --- | --- | --- | --- |
| D1 | Chase and retreat | Me = pursuer and P = withdrawer | You want to sort it out now. \[Partner\] needs space first. The more you push, the further \[Partner\] pulls back, and the further \[Partner\] pulls back, the harder you push. | +2 Say "I need 20 minutes" and come back |
| D1r | Chase and retreat | Me = withdrawer and P = pursuer | You need space before you can talk. \[Partner\] wants it sorted now. The more \[Partner\] pushes, the more you shut down, and that makes \[Partner\] push harder. | +2 Give me 20 minutes before we talk it through |
| D2 | Two fires | Both pursuer or defender (any mix) | You both need to settle it right now, and neither of you backs down. Nobody slows it down, so it goes from 0 to 100. | +2 Keep a calm voice |
| D3 | The silent build-up | Both withdrawer or peacekeeper (any mix) | You both avoid it. Nothing gets said, so it builds until it all comes out at once over something tiny. | +2 Raise things calmly when they happen |
| D4 | The one who always gives in | Me = peacekeeper and P = defender | You keep the peace by giving in. \[Partner\] digs in. It ends the fight, but it doesn't end the problem, and it builds resentment. | +2 Meet me halfway sometimes |
| D4r | The one who always gives in | Me = defender and P = peacekeeper | \[Partner\] gives in to keep the peace, so you rarely hear what \[Partner\] really thinks, until it comes out sideways. | +2 Tell me what they really think |
| D5 | Fixer and feeler | my\_upset\_need ≠ partner\_upset\_need | When you're upset you want \[my need\]. When \[Partner\] is upset they want \[their need\], so that's what \[Partner\] gives you. You both try, and you both miss. | +1 the target for my need: comfort → Comfort me first, before anything else · vent → Listen first, fix later · fix → Help me sort it, not just sympathise · space → Give me space when I ask for it · apology → Say sorry first sometimes |
| D6 | Facts and feelings | Me = F and P = T | You need to feel understood. \[Partner\] argues about what's fair. You end up having two different arguments at once. | +1 Acknowledge how I feel before the facts |
| D6r | Facts and feelings | Me = T and P = F | You argue about what's fair. \[Partner\] needs to feel understood first. Until that happens, the facts don't land. | +1 Say what's actually wrong, clearly and calmly |
| D7 | Lost in translation | my\_love\_style ≠ partner\_love\_style | You feel loved through \[my style\]. \[Partner\] shows love through \[their style\]. \[Partner\] may be trying hard in a language you don't hear. | +1 the target for my style: hearing it → Tell me what they appreciate about me · time → Give me real time every day · help → Do their share without being asked · touch → Show affection every day · gifts → Do one thoughtful thing for me each week |
| D8 | Recharge clash | Me = E and P = I | After a long day you need to talk; \[Partner\] needs quiet. That's why evenings are so tense. | +1 Give me 10 minutes of real conversation after work (+1 more if when\_argue = Evenings after work) |
| D8r | Recharge clash | Me = I and P = E | After a long day you need quiet; \[Partner\] needs to talk. That's why evenings are so tense. | +1 Give me 20 quiet minutes when I get home, then we talk (+1 more if when\_argue = Evenings after work) |
| D9 | Pressing the button | my\_trigger = Being ignored and partner\_stress = Goes quiet · or my\_trigger = Being criticised and partner\_stress = Gets snappy · or my\_trigger = Being told what to do and P = defender | When \[Partner\] is stressed, \[Partner\] \[goes quiet / gets snappy / digs in\], and that's exactly what gets under your skin. | +1 Tell me when they need quiet, instead of going silent · Say it kindly, even when stressed · Ask, don't tell (matching the condition) |
| D10 | Planner and free spirit | Me = J and P = P | You like things settled; \[Partner\] likes to keep options open. Last-minute changes feel like disrespect to you and like nothing to \[Partner\]. | +1 Stick to the plans we make |
| D10r | Planner and free spirit | Me = P and P = J | \[Partner\] likes things settled; you like to keep options open. What feels relaxed to you feels unreliable to \[Partner\]. | no vote (it's about the user's own behaviour) |
| D11 | Details and big picture | S and N differ | One of you talks about what happened; the other talks about what it means. You can both be right and still not hear each other. | no vote, report only |

- **Saves:** dynamics\_found (list of IDs).
- **Which dynamics reach the report:** the first two found, in this priority order: D1/D1r, D4/D4r, D2, D3, D5, D6/D6r, D7, D8/D8r, D9, D10/D10r, D11.
- **None found** (rare; usually lots of "Not sure"): the report uses the cycle alone and adds *"\[Partner\] fills in their side when they join, and your picture gets sharper."*
- **When \[Partner\] joins** and answers Part B themselves, rerun the engine with their real answers. If the top dynamic changes, both see it on Home as *"Your dynamic, now with both sides."*

### Part G — The one thing and your report

#### How the suggestion is worked out

Every possible "one thing" is a target, matched by its exact text. Answers across the questionnaire vote for targets. When different answers point at the same target, that's the signal: the user told us the same thing in different ways without realising.

| Source | Votes |
| --- | --- |
| Sticking point (1D.3, known route) | +2 to its target |
| Each scenario answer (1D.10–1D.15, not-sure route) | +1 to its target |
| Dynamics found (Part F) | +1 or +2 as listed |
| Cycle (1E.1–1E.3) | +1: buildup → Raise things calmly when they happen · replay → Leave the past in the past · shutdown → Stay in the conversation, even when it's hard · shouting → Keep a calm voice |
| First mover = Me (1E.4) | +1 to Say sorry first sometimes |

- **Ranking:** most votes first. Ties: the sticking-point target first, then the dynamic's target (in Part F priority order), then the order answered.
- **Strongest signal:** the top target gets this badge if it has 3+ votes, with a reason line naming where it came from, e.g. *"Came up 3 times: your sticking point, Chase and retreat, and how your fights end."*
- **Mostly none** (not-sure route only): if the user answered None of these on 4 or more of 1D.11–1D.15 and no target has 2+ votes, switch to the start-doing list (below) with the headline *"Nothing jumps out in how \[Partner\] argues. So pick something for \[Partner\] to start doing."*
- **Saves:** target\_votes (target → votes, sources).

#### 1G.1 The one thing

- **Shows:** *"If \[Partner\] changed one thing, what would help most?"*
  - Top target with the Strongest signal badge and reason line (if 3+ votes)
  - Next two targets under **Also fits**
  - **More options** (collapsed): every other target with votes first, then the full list of daily actions grouped by topic, so any daily action can always be picked
  - **Write my own**
- **Options:** tap any target → 1G.2 · **Write my own** → text field (5–60 characters) → **Continue** → 1G.2
- **Vague nudge:** if the written text is only a vague word or phrase (nicer, better, more loving, less annoying, respect me, be kind), show once: *"That's hard to check day to day. What would \[Partner\] actually do differently on a good day?"* The field stays editable; the second tap on Continue always goes through.
- **Start-doing list** (mostly-none rule): Tell me what they appreciate about me · Ask about my day before picking up their phone · Plan time for just us every week · Say thanks for what I do · Give me 10 minutes of real conversation after work · Write my own
- **Saves:** one\_thing\_for\_partner

#### The daily action: one fixed do or don't

The questionnaire traces the fights down to the smallest behaviour behind them. That behaviour becomes each person's **daily action**: one thing they either do or don't do, every day, for the whole 90 days. It never changes during the cycle. Each night the partner taps whether it happened. That's the whole mechanism.

**Rules**

1. **Binary.** It either happened or it didn't. No scales, no "sort of".
2. **Daily.** It must be checkable every single day, fight or no fight. Behaviours that only exist mid-argument are rewritten as the everyday version ("Say 'I need 20 minutes'" becomes *Don't walk off without saying when you'll be back*).
3. **Visible to the partner.** The partner must be able to answer the nightly question from what they saw.
4. **Same action, every day, for 90 days.** It only changes at Day 90 (Keep or Pick new).
5. **Two kinds:**
   - **Don't** (stop the behaviour): a good day is a day it **didn't** happen. If the situation never came up, that's a good day.
   - **Do** (the daily opposite): a good day is a day it **did** happen. Used when the fix is to build the opposite habit, e.g. a partner who is critical must compliment once a day.

**Every suggestion in the questionnaire maps to one daily action.** The user always sees the daily action text, never the suggestion text. Where a problem has both a Don't and a Do, **the top suggestion shows the Don't and the Do version is the first "Or choose" option**.

| Suggestion (from the questionnaire) | Daily action shown | Kind | Nightly question to the partner | Good day when | Reached from |
| --- | --- | --- | --- | --- | --- |
| Listen without interrupting | Don't interrupt me | Don't | Did \[Partner\] interrupt you today? | No | Sticking point · 1D.10 |
| Hear me out without getting defensive | Don't get defensive | Don't | Did \[Partner\] get defensive with you today? | No | Sticking point · 1D.10, 1D.11 |
| Don't turn the blame back on me | Don't turn the blame back on me | Don't | Did \[Partner\] turn the blame back on you today? | No | Sticking point · 1D.10, 1D.11 |
| Take my feelings seriously | Don't brush off how I feel | Don't | Did \[Partner\] brush off how you felt today? | No | Sticking point · 1D.10, 1D.14 |
| Listen first, fix later | Don't jump to fixing when I'm venting | Don't | Did \[Partner\] jump to fixing when you were venting? | No | Sticking point · 1D.14 · D5 |
| Keep the focus on me when I'm upset | Don't turn it to yourself when I'm upset | Don't | Did \[Partner\] turn it to themselves when you were upset? | No | 1D.14 |
| Stay on topic | Don't change the subject when I raise something | Don't | Did \[Partner\] change the subject when you raised something? | No | Sticking point · 1D.11 |
| Acknowledge how I feel before the facts | Don't argue facts before acknowledging how I feel | Don't | Did \[Partner\] argue facts before acknowledging how you felt? | No | D6 |
| Comfort me first, before anything else | Comfort me first when I'm upset | Do | When you were upset today, did \[Partner\] comfort you first? (no upset today = good day) | Yes | D5 |
| Help me sort it, not just sympathise | Help me sort it when I ask | Do | When you asked for help today, did \[Partner\] help you sort it? (didn't ask = good day) | Yes | D5 |
| Keep a calm voice | Don't raise your voice at me | Don't | Did \[Partner\] raise their voice at you today? | No | Sticking point · 1D.10, 1D.12, 1D.13 · Shouting Match cycle · D2 |
| Say it straight, no sarcasm | No sarcasm with me | Don't | Was \[Partner\] sarcastic with you today? | No | Sticking point · 1D.12 |
| Drop the eye-rolls and sighs | No eye-rolls or sighs at me | Don't | Did \[Partner\] roll their eyes or sigh at you today? | No | Sticking point · 1D.12 |
| Keep criticism private | Don't criticise me in front of others | Don't | Did \[Partner\] criticise you in front of others today? | No | Sticking point |
| Stop the criticism · Say it kindly, even when stressed | Don't criticise me without acknowledging what I also do well · **or** Compliment me once a day | Don't · Do | Did \[Partner\] criticise you today without acknowledging what you do well? · Did \[Partner\] compliment you today? | No · Yes | Sticking point · D9 |
| Leave the past in the past | Don't bring up the past if we agreed to move on | Don't | Did \[Partner\] bring up something you'd agreed to move on from? | No | Sticking point · 1D.13 · Replay cycle |
| Leave earnings out of arguments | Don't bring up who earns more | Don't | Did \[Partner\] bring up who earns more today? | No | Sticking point |
| Ask, don't tell | Don't give me orders, ask me kindly | Don't | Did \[Partner\] give you orders instead of asking kindly? | No | Sticking point · D9 |
| Stay in the conversation, even when it's hard | Don't go silent on me for more than 30 minutes | Don't | Did \[Partner\] go silent on you for more than 30 minutes? | No | 1D.10, 1D.12, 1D.13 · Shutdown cycle |
| Say "I need 20 minutes" and come back | Don't walk off without saying when you'll be back | Don't | Did \[Partner\] walk off without saying when they'd be back? | No | D1 |
| Give me 20 minutes before we talk it through · Give me space when I ask for it | Don't push me to talk when I ask for space | Don't | Did \[Partner\] push you to talk when you asked for space? | No | D1r · D5 |
| Make up within a day · Come back and talk it through | Don't go to bed still not speaking | Don't | Did you go to bed with \[Partner\] still not speaking to you? | No | 1D.15 |
| Tell me when they need quiet, instead of going silent | Don't go quiet without telling me why | Don't | Did \[Partner\] go quiet without telling you why? | No | D9 |
| Raise things calmly when they happen | Don't save things up and explode (raise one issue at a time) | Don't | Did \[Partner\] explode over things they'd saved up, or pile on several issues at once? | No | Build-up cycle · D3 |
| Tell me what they really think | Don't say "fine" when it isn't | Don't | Did \[Partner\] say "fine" when it clearly wasn't? | No | D4r |
| Say what's actually wrong, clearly and calmly | Don't make me guess what's wrong | Don't | Did \[Partner\] make you guess what was wrong today? | No | D6r |
| Meet me halfway sometimes | Don't dig in on small decisions | Don't | Did \[Partner\] refuse to meet you halfway on something small? | No | D4 |
| Say sorry first sometimes | Make the first move to make up after a disagreement | Do | After any disagreement today, did \[Partner\] make the first move to make up? (no disagreement = good day) | Yes | Who makes up first = Me · 1D.15 |
| Say thanks for what I do | Thank me for something every day | Do | Did \[Partner\] thank you for something today? | Yes | Sticking point |
| Notice and appreciate me · Tell me what they appreciate about me | Tell me one thing you appreciate about me, every day | Do | Did \[Partner\] tell you something they appreciate about you today? | Yes | Sticking point · D7 |
| Show affection every day | Show me affection every day | Do | Did \[Partner\] show you affection today (a hug, a kiss, holding hands)? | Yes | Sticking point · D7 |
| Do one thoughtful thing for me each week | Do one small thoughtful thing for me every day | Do | Did \[Partner\] do something thoughtful for you today? | Yes | D7 |
| Give me real time every day · Plan time for just us every week · Make time for us first | Give me 10 minutes of full attention every day | Do | Did \[Partner\] give you 10 minutes of full attention today? | Yes | Sticking point (×3) · D7 |
| Give me 10 minutes of real conversation after work | Talk with me for 10 minutes after work | Do | Did \[Partner\] talk with you properly after work today? | Yes | D8 |
| Give me 20 quiet minutes when I get home, then we talk | Don't start a serious talk in my first 20 minutes home | Don't | Did \[Partner\] start a serious talk in your first 20 minutes home? | No | D8r |
| Ask about my day before picking up their phone | Ask about my day before picking up your phone | Do | Did \[Partner\] ask about your day before picking up their phone? | Yes | Start-doing list |
| Do their share without being asked · Notice what needs doing and do it | Do one job every day without being asked | Do | Did \[Partner\] do a job today without being asked? | Yes | Sticking point (×2) · D7 |
| Finish what they start | Don't leave jobs half-done | Don't | Did \[Partner\] leave a job half-done today? | No | Sticking point |
| Tidy up after themselves | Don't leave mess for me | Don't | Did \[Partner\] leave mess for you today? | No | Sticking point |
| Follow through on what we agree · Remember what we agreed | Don't break what we agreed | Don't | Did \[Partner\] go back on something you'd agreed? | No | Sticking point · 1D.15 |
| Put the phone down when we talk | No phone while I'm talking to you | Don't | Was \[Partner\] on their phone while you were talking to them? | No | Sticking point (×2) · 1D.13, 1D.14 |
| No phones at meals | No phone at meals | Don't | Was \[Partner\] on their phone at a meal today? | No | Sticking point |
| Phone away in bed | No phone in bed | Don't | Was \[Partner\] on their phone in bed? | No | Sticking point |
| Check with me before big spends · Be open about money | Don't spend over £\[amount\] without talking to me. We're a team! (amount asked when picked: £50 · £100 · £250 · Other) | Don't | Did \[Partner\] spend over £\[amount\] without talking to you? | No | Sticking point (×2) |
| Talk about money calmly, not in a fight | Don't bring up money mid-argument | Don't | Did \[Partner\] bring up money in an argument today? | No | Sticking point |
| Check with me before saying yes to plans | Don't agree to plans for us without asking me | Don't | Did \[Partner\] agree to plans for you both without asking? | No | Sticking point |
| Ask what I'd like to do | Ask what I'd like before deciding for us | Do | Did \[Partner\] ask what you'd like before deciding something for you both? (nothing decided = good day) | Yes | Sticking point |
| Stick to the plans we make | Don't change our plans last minute | Don't | Did \[Partner\] change your plans last minute? | No | Sticking point · D10 |
| Be on time, or tell me early | Don't be late without telling me | Don't | Was \[Partner\] late without telling you? | No | Sticking point |
| Back me up in front of others | Don't take their side against me in front of others | Don't | Did \[Partner\] take someone else's side against you today? | No | Sticking point |
| Speak kindly about my family | Don't speak badly about my family | Don't | Did \[Partner\] speak badly about your family today? | No | Sticking point |
| Kiss me for 30 seconds every day | Kiss me for 30 seconds every day | Do | Did \[Partner\] kiss you for 30 seconds today? | Yes | Intimacy IN.5 · Roommates pattern |
| Start affection with me once a day | Reach for me once a day (a kiss, a hug, holding me) | Do | Did \[Partner\] reach for you today? | Yes | Intimacy IN.5 |
| Touch me without it leading anywhere | Show me affection that doesn't have to lead anywhere, every day | Do | Did \[Partner\] show you affection today without expecting more? | Yes | Intimacy IN.5 · Pressure Loop pattern |
| Say no kindly | If it's not tonight, say it kindly | Don't | Did \[Partner\] turn you down coldly today? (didn't come up = good day) | No | Intimacy IN.5 |
| Don't sulk when I say not tonight | Don't sulk or go cold when I say not tonight | Don't | Did \[Partner\] sulk or go cold after you said not tonight? (didn't come up = good day) | No | Intimacy IN.5 |
| Tell me what you find attractive about me | Tell me one thing you find attractive about me, every day | Do | Did \[Partner\] tell you something they find attractive about you today? | Yes | Intimacy IN.5 |
| Come to bed at the same time as me | Come to bed at the same time as me | Do | Did \[Partner\] come to bed at the same time as you? | Yes | Intimacy IN.5 |
| Don't put my mood down to my cycle | Don't put my mood down to my cycle | Don't | Did \[Partner\] put your mood down to your cycle today? (didn't come up = good day) | No | PMS or PMDD PM.5 |
| Ask what I need before reacting | On a hard day, ask what I need before reacting | Do | On a hard day today, did \[Partner\] ask what you needed before reacting? (no hard day = good day) | Yes | PMS or PMDD PM.5 |
| Ask how I'm really doing | Ask how I'm really doing, every day | Do | Did \[Partner\] ask how you were really doing today? | Yes | PMS or PMDD PM.5 |
| Tell me you're struggling, don't take it out on me | Tell me you're struggling instead of taking it out on me | Don't | Did \[Partner\] take a hard day out on you today? (didn't come up = good day) | No | PMS or PMDD PM.5 |
| Don't leave me guessing | Don't leave me guessing how you're feeling | Don't | Did \[Partner\] leave you guessing how they were feeling today? (didn't come up = good day) | No | PMS or PMDD PM.5 |

- **Write my own** at 1G.1 asks two extra things: **Is this a Do or a Don't?** and the nightly question is generated as *"Did \[Partner\] \[their words\] today?"*, shown for the writer to confirm or edit (up to 80 characters).
- **Vague-word check** applies to the daily action, not just the wording: if it can't be answered yes or no about one day, show *"Can \[Partner\] answer this yes or no about today? Make it something they either do or don't."*
- **Saves:** daily\_action (text), action\_kind (do / dont), nightly\_question.

#### 1G.2 What doing well looks like

- **Shows:** *"What would it look like if \[Partner\] did this well? We'll show \[Partner\] this, so it's clear."* · text field (up to 120), placeholder *"e.g. telling me calmly when something bugs them"*
- **Options:** **Continue** → 1G.3 · **Skip** → 1G.3
- **Saves:** well\_looks\_like

#### 1G.3 What you want most

- **Shows:** *"What do you want most from this?"*
- **Options (each → 1G.4):** Fewer arguments · To feel close again · To feel heard · To stop walking on eggshells · A calmer home for the kids (only if living = Yes, with kids)
- **Saves:** motivation

#### 1G.4 Loading

- **Shows:** *"Building your report…"* with three lines ticking in, 0.8 seconds apart: *Reading your style · Comparing you and \[Partner\] · Finding your pattern*. → 1G.5 automatically.

#### 1G.5 Your report

This is the moment of delight: the user should feel seen, surprised and hopeful, in that order. The report is revealed one full-screen card at a time, like Spotify Wrapped, never as a list.

**How it works**

- Each card fills the screen, in the Lab Report style (paper background, ink type, the accent at most once per card; no gradients, no pink). Big text, one idea per card.
- **Tap the right side or swipe left** → next card. **Swipe right** → previous card. Progress dots across the top. **X** → the usual "Leave for now?" sheet.
- Each card's headline animates in first, then its detail 0.5 seconds later.
- First card: swiping right goes back to 1G.3.

| # | Card | Headline | Content |
| --- | --- | --- | --- |
| 1 | Opening | **We've figured you two out.** | *"Tap to see what we found."* |
| 2 | Strengths | **First, what's good about you two** | Two strength lines (table below). Always positive, never a "but". |
| 3 | You | **You** | You \[personality line\]. When you're upset, you need \[my\_upset\_need\]. You feel loved through \[my\_love\_style\]. What gets to you fastest: \[my\_trigger\]. Type \[my\_type\], small. |
| 4 | \[Partner\] | **\[Partner\], as you see them** | Same layout from Part C; unknown answers left out. Footer: *"\[Partner\] gets to say if you're right."* |
| 5 | Your dynamic | **You two are \[dynamic name\].** (very large, alone for 1 second, then the copy fades in) | The top dynamic's copy (Part F). Second dynamic, if found, as a smaller line: *"With a bit of \[second name\]: \[first sentence of its copy\]"* |
| 6 | Our guess | **We'd guess…** | The prediction line for the top dynamic (table below), something the user never told us. Two buttons: **That's so us** · **Not quite**. Either → next card. Saves prediction\_reaction. |
| 7 | Your pattern | **Your pattern: \[cycle name\]** | \[Cycle description\]. It tends to kick off \[when phrase\]. Frequency line as before. |
| 8 | The exact problem | Known route: **It's really about \[sticking\_point\]** · Not-sure route: **It kept coming up: \[top target\]** | Known: *You said: "\[last\_time\_example\]"* if given. Not sure: the strongest-signal reason line. |
| 9 | The good news | **This is fixable.** | The hope line for the top dynamic (table below). |
| 10 | What breaks it | **What breaks it** | \[Partner\] works on: **\[one\_thing\_for\_partner\]**. What good looks like: \[well\_looks\_like\]. Your side (private): *"And you'd like to \[self\_reflection\]."* Always ends: *"\[Partner\] picks one thing for you too. Fair's fair."* |
| 11 | Your goal | **In 90 days: \[motivation\]** | *"One small thing each, every day."* |
| 12 | Your card | **Your dynamic card** | A designed card to keep or share: Loveth logo, *"\[Me\] & \[Partner\]"*, the dynamic name, the two strength lines. Never includes the problem, the one thing, self\_reflection or any private answer. Buttons: **Share** → native share sheet with the card as an image · **Save image** → photos · **Next** |
| 13 | Check | **Does this sound like you two?** | Options below. |

**Card 13 options**

- **Spot on** → 2.1a
- **Mostly** → sheet *"Want to tweak anything first?"* · **Carry on** → 2.1a · **Tweak something** → the "What did we miss?" chooser
- **Not really** → "What did we miss?" chooser
- **"What did we miss?" chooser:** Me → 1B.1 · \[Partner\] → 1C.1 · The problem → 1D.1 or 1D.10 (by path) · Our pattern → 1E.1. Previous answers stay pre-selected. After the last screen of that part, the report rebuilds and reopens at card 1. The second time card 13 is reached, **Not really** and **Mostly** both go to 2.1a (no loop).
- **Saves:** report\_reaction (spot\_on / mostly / not\_really), report\_edits (which part). Target: 70%+ Spot on. Below that, the questions need work.

**Strength lines (card 2):** check in this order and show the first two that apply. The fallback always applies.

| Condition | Strength line |
| --- | --- |
| Both F | You both lead with feelings. That's exactly why it hurts so much when you're not understood. |
| Both T | You both care about what's fair. Once you agree the rules, you'll both stick to them. |
| Both J | You both like things settled, so a plan you make together will actually hold. |
| Both E | You both recharge together. Time as a couple genuinely fills you both up. |
| Both I | You both value quiet, so you can give each other space without it meaning anything bad. |
| E/I or S/N differ | You balance each other: \[Partner\] brings what you don't, and the other way round. |
| first\_mover = Me | You're the one who reaches out first. That takes guts, and it's a big part of why you're still going. |
| self\_reflection given (not "I'm not sure") | You named something you could do better. Most people never do, and it's the strongest sign this will work. |
| together\_length 3+ years and frequency Every day or A few times a week | You've argued this much and you're still here, still trying. That says a lot about you two. |
| motivation = To feel close again or To feel heard | You want to feel close, not to win. That's exactly the right goal. |
| Fallback | You're here looking for a fix, not a fight. That's the step most couples never take. |

**Prediction and hope lines (cards 6 and 9):**

| Dynamic | We'd guess… (card 6) | This is fixable (card 9) |
| --- | --- | --- |
| D1 Chase and retreat | the worst ones happen late at night, when you want to settle it before bed and \[Partner\] just wants it to stop. | Chase and retreat is one of the most fixable patterns there is. \[Partner\] doesn't have to talk sooner, just say when they'll be back. |
| D1r Chase and retreat | you've said "can we talk about this later?" and \[Partner\] heard "I don't care." | Chase and retreat is one of the most fixable patterns there is. You get your 20 minutes; \[Partner\] gets a time you'll come back. |
| D2 Two fires | you both remember the last big fight differently, and you each think you were right. | When two strong people both slow down by one notch, the whole fight changes. |
| D3 The silent build-up | there's something that's bothered you for weeks that you still haven't said. | The build-up only works in silence. Saying small things early takes all its power away. |
| D4 / D4r The one who always gives in | (D4) you've said sorry for things that weren't really your fault, just to end it. (D4r) \[Partner\] has said "fine" when it really wasn't. | Peace that's real feels completely different from peace that's kept. One honest conversation a week gets you there. |
| D5 Fixer and feeler | you've both said "I was only trying to help" after a fight. | You're both already trying. You're just aiming at the wrong target, and that's the easiest thing to fix. |
| D6 / D6r Facts and feelings | (D6) you've heard "that's not what I said" and thought "that's not the point." (D6r) you've been told you're "not listening" when you were sure you were. | Feelings first, facts second. Once you both know the order, most arguments get half as long. |
| D7 Lost in translation | \[Partner\] has done something for you and felt hurt you didn't notice. | You're not short on love, just on translation. That's learnable in weeks, not years. |
| D8 / D8r Recharge clash | the first 30 minutes after work are the riskiest part of your day. | Fix 30 minutes a day and you fix most of your fights. |
| D9 Pressing the button | you can tell \[Partner\]'s had a bad day within seconds of them walking in. | Once you both know where the button is, it's surprisingly easy not to press it. |
| D10 / D10r Planner and free spirit | (D10) "we'll see" is one of the phrases that winds you up most. (D10r) you've been called unreliable for something that felt minor to you. | You don't need to become the same person. You need a few plans you both keep. |
| D11 Details and big picture | you've argued about what was actually said. | Agree what happened, then talk about what it means. In that order, you'll be on the same side. |
| No dynamic (by cycle) | buildup: the last big one started over something tiny. · replay: an old fight came up in the last argument. · shutdown: someone ended the last fight by leaving the room. · shouting: you both said something you didn't mean last time. | \[Cycle name\] is a pattern, not a personality. Patterns can be broken. |

| cycle\_type | Cycle name | Description |
| --- | --- | --- |
| buildup | The Build-up | Small things pile up unsaid, then one tiny thing sets everything off. |
| replay | The Replay | Arguments don't stay about today. Old fights keep coming back into new ones. |
| shutdown | The Shutdown | One of you goes quiet, the other pushes harder, and nothing gets settled. |
| shouting | The Shouting Match | It gets loud and personal fast, and what you actually meant gets lost. |

| when\_argue | When phrase |
| --- | --- |
| Evenings after work | in the evenings, after a long day |
| Mornings | in the mornings, before the day's even started |
| Weekends | at weekends, when you finally have time together |
| Over text | over text, where tone gets lost |
| When one of us is tired or hungry | when one of you is tired or hungry |
| Any time | at any time, with no warning |

### Customisation map

No answer is asked for show. This is where each one changes the app after the report.

| Answer | Where it's used |
| --- | --- |
| partner\_first\_name | Every screen, push and email |
| together\_length | Report extra line: under a year → *"Catching this early is the best time to fix it."* · more than 10 years → *"Old habits change with daily practice."* |
| living | Unlocks "A calmer home for the kids" at 1G.3 |
| frequency | Report pattern card · paywall subline |
| my\_type, partner\_type | Report · Part F dynamics · \[Partner\]'s own answers replace the guess when they join |
| conflict\_style (both) | Dynamics D1–D4 · the heads-up push copy for D1 couples: *"Remember: \[Partner\] needs 20 minutes, then talks."* |
| upset\_need, love\_style (both) | Dynamics D5, D7 · \[Partner\]'s Home card *"What \[Me\] needs when upset: \[need\]"* |
| my\_trigger, partner\_stress | Dynamic D9 |
| main\_topic, sticking\_point, last\_time\_example | Report · top vote at 1G.1 |
| scenario answers (1D.10–1D.15) | Votes at 1G.1 · the strongest-signal reason line |
| when\_argue | Report · default check-in time at 2.1c (Evenings after work → 21:30, otherwise 21:00) · heads-up push (below) · Over text → report line *"Save the big talks for face to face."* |
| cycle\_type | Report · one vote at 1G.1 · \[Partner\]'s suggestions at P4 |
| my\_recovery | C2: if About a day or Several days and \[Partner\] said *Not today* about you → *"Try to make up before bed tonight."* |
| first\_mover | +1 vote for Say sorry first sometimes |
| self\_reflection | Report private card · private Home card *"Your own goal: \[self\_reflection\]"* |
| one\_thing\_for\_partner, well\_looks\_like | Reveal, Home cards, every daily check-in question and push |
| motivation | Report goal card · paywall subline · Day 90: *"You wanted \[motivation\]. Look how far you've come."* |
| dynamics\_found | Report · paywall bullet (below) · Home *"Your dynamic"* card |

**Paywall subline (6.1, under the headline):** *"You argue \[frequency\]. You want \[motivation\]. Let's start."* (Less than once a week → *"The same fight keeps coming back. You want \[motivation\]. Let's start."*)

**Paywall top bullet:** *"Built for \[dynamic name\]: \[one\_thing\_for\_partner\]"*. If no dynamic, uses the cycle name.

**Heads-up push** (on by default, toggle in settings): a nudge just before arguments usually start, to both partners once both have picked.

| when\_argue | Sent | Message |
| --- | --- | --- |
| Evenings after work | 17:30 weekdays | Evenings are when it usually kicks off. Remember: \[one thing for you\]. |
| Mornings | 07:30 daily | Mornings can be tense. Remember: \[one thing for you\]. |
| Weekends | 10:00 Sat and Sun | Weekend together. Remember: \[one thing for you\]. |
| When one of us is tired or hungry | 17:30 daily | Long day? Remember: \[one thing for you\]. |
| Over text / Any time | Not sent | — |

## Stage 2 — Your daily action

The report traced the fights to the smallest behaviour. This stage shows her the one daily action that fixes it and lets her try the nightly tap, before she's asked to invite anyone or commit to anything.

### 2.1a Your daily action

- **Shows:**
  - Headline: *"Here's how we break \[pattern\]."*
  - **\[Partner\]'s daily action** card: a **Do** or **Don't** badge, then the daily action in large type (e.g. **Don't get defensive**) · *"Every day for 90 days. Every night, you tap whether \[Partner\] did it."*
  - **Your daily action** card: *"\[Partner\] picks yours when they join, and taps for you every night."*
  - Why it works: *"Big fights start with small things. Fix the small thing every day and the big fights run out of fuel. Neither of you marks yourself, so you keep each other honest."*
- **Options:** **Show me the nightly tap** → 2.1b · Back arrow → 1G.5 (last card)

### 2.1b Try the nightly tap

- **Shows:** label *"This is all you do each night"*, then the real C1 question for \[Partner\]'s action, e.g. *"Did \[Partner\] get defensive with you today?"* with **Yes** and **No**.
- **Options:** tap either → the card shows the result: **Good day** or **Bad day**, a 90-square calendar with today's square filling white (good) or black (bad), and: *"That's it. 5 seconds a night. \[Partner\] does the same for you."* · **Continue** → 2.1c
- **Saves:** demo\_done = true. The demo tap is never stored as a real day.

### 2.1c Pick your time

- **Shows:** *"When should we ask you each night?"* · time picker: wheel, 15-minute steps, device 12/24-hour setting. Default: Evenings after work → 21:30, otherwise 21:00 · *"Pick a time you're home and winding down."*
- **Options:** **Set my time** → 2.2 · Back arrow → 2.1b
- **Saves:** checkin\_time + device time zone

### 2.2 Notification permission

Shown only if the app doesn't already have notification permission; otherwise 2.1c goes straight to 3.1.

- **Shows:** *"We'll remind you at \[time\]. Turn on notifications so you never miss a day."*
- **Options:**
  - **Turn on notifications** → system permission prompt → 3.1 whatever the answer
  - **Not now** → 3.1
- **Saves:** notification permission status. If off, Home shows a banner (see Home) and the Day-5 reminder still goes by email.

## Stage 3 — Invite the partner

The user writes a short love note to the partner and seals it inside the invite. The invite says a note exists but never shows the words: the partner can only open it by joining the app. The partner's first contact with the app is a compliment, not a complaint, and curiosity does the work. Sending is required to continue on the fighting route. On the intimacy and hard week routes, 3.2 also offers I'll send it later, so nobody gets stuck before they're ready to ask.

### 3.1 Seal a note

- **Shows:** label 3.1 · SEALED FOR \[PARTNER\] · "What do you love about \[Partner\]?" · "Pick up to three. We'll seal it in \[Partner\]'s invite. \[Partner\] only sees it once they join."
- **Chips (multi-select, max 3):** Makes me laugh · Always has my back · Works so hard for us · Calm when I'm not · Makes me feel safe · Still gets me · Good with my family · + Add your own (opens a 3–40 character field). The top two are preselected so the box is never empty.
- **Prefilled text box (editable, 300 max):** "\[Partner\], I know there are things we need to improve, but here's what I love about you and why I'll keep choosing us: \[chip 1 as a phrase\], and \[chip 2 as a phrase\]." The sentence rewrites itself live as chips change until the user types in the box; after that, chips no longer overwrite their words.
- **Chip phrases:** Makes me laugh → you make me laugh when I'm stressed · Always has my back → you always have my back · Works so hard for us → you work so hard for us · Calm when I'm not → you stay calm when I can't · Makes me feel safe → you make me feel safe · Still gets me → you still get me better than anyone · Good with my family → you're so good with my family.
- Lock line above the button: "Sealed until \[Partner\] joins."
- **Options:** Seal it for \[Partner\] (needs 1+ chip or 20+ characters) → 3.2 · Back arrow → 2.1c
- **Saves:** love\_note\_text, love\_note\_chips, love\_note\_sealed\_at. (Replaces nice\_words\_about\_partner.)

### 3.2 Send the invite

- **On load:** create couple\_id and invite\_link if they don't exist yet.
- **Shows:** a preview of the message exactly as the partner will receive it:

> &#91;Me\] wrote something about you and sealed it. You can only open it in the app. \[Me\] also thinks they've found the pattern behind your arguments. Want to see if \[Me\] got you right? Open it here: \[invite\_link\]
>
> Link preview: black card, sealed envelope with the accent seal, "SEALED · FOR \[PARTNER\]", title "\[Me\] wrote something about you". The note's words never appear in the message, the preview or any push.

- **Options:**
  - **Send to \[Partner\]** → native share sheet (WhatsApp, iMessage, etc.) with the message above.
    - iOS share completed → 4.0. iOS share cancelled → stays on 3.2.
    - Android (can't confirm the send) → returning to the app counts as sent → 4.0.
  - **Copy message** → copies the message to the clipboard, toast *"Copied"*, and adds a button **I've sent it** → 4.0.
  - **Edit message** → back to 3.1. Intimacy and hard week routes only: a small text link I'll send it later → 4.0 with the invite unsent. They pay and start their own thing straight away; Home's status slot shows the invite card, the Stage 5 drip (J1–J3) runs, and sending is always one tap from Home.
- **Saves:** invite\_sent\_at.

### Invite link rules

- One link per couple. Resending reuses it.
- Valid for 30 days. After that, opening it shows *"This invite has expired. Ask \[Me\] to send a new one."* and the initiator's Home **Resend invite** makes a new link.
- One partner per link. If someone opens it after the partner has joined: *"This invite has already been used."*
- The initiator can't join their own link (same account → *"This is your own invite. Send it to \[Partner\]."*).

### 4.0 Are you ready to fix this?

Initiator only. Shown once, straight after the invite is sent or put off (3.2) and before the commitment questions. Never shown to the partner and never in the invite. Full-screen black, no back button. This is the turn from "we see you" to "now commit".

- **Label:** BEFORE YOU COMMIT, then the pattern name in accent (e.g. CHASE AND RETREAT).
- **Headline:** "Left unfixed, this is the pattern that breaks couples up."
- **Body (criticism, defensiveness, blame patterns):** "A study that followed married couples for 14 years found that couples stuck in criticism and defensiveness during arguments were the ones who split earliest, most within the first 7 years." Source line: GOTTMAN & LEVENSON, 2000.
- **Body (shutdown, silence, avoidance patterns):** "The same research found couples who avoid conflict and go cold don't split as early, but they drift: most later breakups came from distance, not shouting." Source line: GOTTMAN & LEVENSON, 2000.
- **Question:** "Are you ready to fix this?" Sub-line: "Starts with your 90-day test."
- **Yes, I believe in us** → 4.1. Saves ready = yes. Light haptic.
- **No, not really** → honest exit sheet: "That's OK. Your answers are saved. If that changes, everything is here." Buttons: **Close** · **Actually, let's try**. Saves ready = no; onboarding drip pauses 3 days, then resumes from Stage 2 messages.
- **Copy rule:** never say "you will break up" or quote a number of years we can't source. Only cite the study as written above. Legal sign-off before launch (UK advertising rules on health/outcome claims).
- **Naming:** the 90-day cycle is called **the 90-day test** everywhere a user sees it (report, 2.1a, invite, partner reveal, Home, Day 90).
- **Analytics:** ready\_shown, ready\_yes, ready\_no, ready\_no\_then\_return.

## Stage 4 — Commitment questions

Three to four small yeses straight after the invite is sent. Every question uses the user's own report, so each yes is a yes to *their* problem, not to an app. Every answer moves forward; none of them end the flow.

`[pattern]` below = the top dynamic's name, or the cycle name if no dynamic was found. `[their thing]` = one\_thing\_for\_partner in lower case.

### 4.1 Ready

- **Shows:** *"Ready to break \[pattern\] with \[Partner\]?"*
- **Options:** Yes, I'm ready → 4.2 · I'm nervous, but yes → 4.2
- **Saves:** commit\_ready

### 4.2 Patient

- **Shows:** *"Are you ready to be patient with \[Partner\] while they learn to \[their thing\]?"*
- **Options:** Yes, I'll be patient → 4.3 (or 4.4 if self\_reflection is "I'm not sure") · I'll try my best → same
- **Saves:** commit\_patient
- **Rule:** each person only ever sees this question about the other person.

### 4.3 Your side

Only shown if the user named something at 1E.5.

- **Shows:** *"You said you'd like to \[self\_reflection\]. Will you work on that too?"*
- **Options:** Yes, I will → 4.4 · I'll try → 4.4
- **Saves:** commit\_self

### 4.4 Priority

- **Shows:** *"What matters more to you: saving money, or \[motivation, lower case\]?"* (e.g. *"…or feeling close again?"*)
- **Options:** \[motivation\] → 5.1 · Saving money → 4.5
- **Saves:** commit\_priority

### 4.5 Fair point (only after "Saving money")

- **Shows:** *"Fair. That's why the first 7 days are free."*
- **Options:** **Continue** → 5.1

## Stage 5 — Trial promise

One screen that states the deal out loud before any price appears.

### 5.1 Give us 7 days

- **Shows:** *"We don't ask for anything until we've proved we can deliver. Give us 7 days. If it's not working for you, end the trial."*
- **Options:**
  - **Sounds good** (primary button) → 6.1
  - **We'd rather argue** (text link) → bottom sheet 5.2

### 5.2 Bottom sheet

- **Shows:** *"Ha. That's the cycle talking. Try 7 days?"*
- **Options:**
  - **Okay, 7 days** → 6.1
  - **Leave** → closes; couple set to **Pulled back**

## Stage 6 — Paywall

The user picks a plan, the store takes card details and the 7-day free trial starts. One subscription covers the couple.

**Two-page paywall (Oct 2026, overrides older paywall copy):**

- **Page 1, the offer:** label FOR \[ME\] & \[PARTNER\] · headline "Would you rather keep £1 a week, or be happier with \[Partner\]?" · six tiles, 2 × 3, each an icon + 3–4 words + one short line: sell benefits, never features: Stop asking for the same thing twice / \[Partner\] gets one clear promise, checked nightly · Know exactly what to work on / Your own goal, matched to how you argue · Calm a fight before it spirals / Step by step, both of you heard (accent icon) · Hear what they actually meant / AI turns heated words into plain ones · Agree a fix you'll both keep / Checked again after 7 days · See the peace add up / Every calm day counted, together · black bar "One price covers you both · \[PARTNER\] JOINS FREE" · price anchor: "One counselling session ~~£50–£100~~" vs "Loveth, a whole year £49.99, under £1/wk" · **Start my 7 free days** → page 2 · bell line "We remind you on Day 5. Cancel in 2 taps." Close X is faint and appears after 2 seconds.
- **Page 2, plans:** STEP 2 OF 2 · "Less than one date night." · "For a whole year, for both of you. Things will change in 7 days." · Yearly (preselected) / Monthly · trial timeline · **Start my 7 free days** · bold bell line "We'll remind you on \[date\], 2 days before you pay."
- Verify the counselling price range against current UK prices before launch. Never claim the app stops fights or replaces therapy.

### 6.1 Pick a plan

- **Shows (top to bottom):**
  - Headline: *superseded: see Two-page paywall above*
  - Feature list: Keeps you both accountable, especially on the hard days · Help in the middle of an argument: you both know what you promised · A 10-second daily check-in for both of you · See your progress together on one calendar
  - Two plan cards (below)
  - Trial timeline visual with real dates: **Day 1 \[today\]** Trial starts · **Day 5 \[date\]** We remind you · **Day 7 \[date\]** Full commitment
  - Main button: **Start my 7 free days**
  - Small print: *"£0 today. You'll be charged \[price\] on \[Day 7 date\] unless you cancel. We'll remind you on \[Day 5 date\]. Cancel anytime in your phone's subscription settings."*
  - Footer links: Restore purchases · Terms of use · Privacy policy

| Plan card | Price line | Line under | Default |
| --- | --- | --- | --- |
| Yearly, badge "Best value" | £49.99 / year | Under £1 a week for both of you | Selected |
| Monthly | £9.99 / month | Cancel anytime | Not selected |

- **Options:**
  - Tap a plan card → selects it (only one selected at a time); small print updates to that price.
  - **Start my 7 free days** → store purchase sheet for the selected plan (outcomes below).
  - **Restore purchases** → checks the store. Active subscription found → 6.1b (signing in brings their data back). None → toast *"No purchase found."*
  - **Terms of use** / **Privacy policy** → open in an in-app browser.
  - Back arrow → 5.1.
  - Close X → *"Leave for now?"* sheet. **Leave** → exits; couple set to **Pulled back**.
- **If the user isn't eligible for a free trial** (already used one on this store account): button reads **Start now**, timeline hidden, small print *"You'll be charged \[price\] today."*

### Purchase outcomes

| Store result | What happens |
| --- | --- |
| Success | Verify the receipt on the server → payer\_id = this user, save trial\_start / trial\_end, sub\_state = Trial active → 6.1b |
| User closes the store sheet | Stay on 6.1, no message |
| Payment failed | Toast *"That didn't go through. Please try again."* Stay on 6.1 |
| Pending (e.g. Ask to Buy) | 6.3, sub\_state = Pending. Unlock when the store confirms |

### 6.1b Save your account

Right after a successful purchase or trial start, before 6.2. Also after Restore purchase on a new phone, and for a partner who takes over and pays (P11).

Shows: "You're in. One tap to keep it safe." · "So your answers, notes and days come back if you ever change phone." · **Sign in with Apple** · **Sign in with Google** (both buttons on both platforms; Apple first on iOS, Google first on Android).

Options: either → the platform sign-in sheet → the anonymous account is upgraded in place, nothing lost → 6.2. Cancelled or failed → stays here with Try again. After a second failure, Do this later appears → 6.2, and Home shows a slim "Keep your progress safe" bar until it's done.

Saves: auth\_provider, email as shared (Apple's hidden relay address is fine; the Day-5 email goes to it). No email field and no password, ever.

### 6.2 You're in

- **Shows:** *"You're in. Day 1 starts now."* · *"We'll remind you on \[Day 5 date\], two days before you're charged."* · Partner status line: *"\[Partner\] is already here."* or *"Next: \[Partner\] joins from your invite."*
- **Options:** **Go to Home** → Home · **Resend invite** (only if the partner hasn't joined) → share sheet from 3.2

### 6.3 Waiting for approval

- **Shows:** *"Waiting for approval. We'll let you know as soon as it's through."*
- **Options:** **OK** → closes.

## Partner flow

The partner joins through the invite link. In this section `[Me]` = the partner and `[Partner]` = the initiator. The partner joins free only if the initiator has started the trial; otherwise the partner is offered the bill.

### P0 Opening the link

| Partner's situation | What happens |
| --- | --- |
| Loveth not installed | App Store / Google Play → install → P0b via deferred deep link (developer picks the tool) |
| Loveth already installed | Link opens the app → P0b |
| Deferred link lost after install | First screen shows **Got an invite?** → paste link → P0b |
| Link expired, used, or own link | Messages in Invite link rules (Stage 3) |

- **On join:** save partner\_id and partner\_joined\_at; send the initiator *"\[Partner\] has joined."*

### P0b The sealed note

The first screen a new partner sees, before any account exists. It is the gate: the note opens only when they tap Open it, which links them to the couple. There is no sign-up.

- **Shows:** FROM \[PARTNER\] · SEALED · "\[Partner\] wrote something about you." · "It's sealed. Join to open it." · large black envelope with the accent seal and \[Partner\]'s initial · meta line "\[n\] THINGS \[PARTNER\] LOVES · WRITTEN \[time\]".
- **Options:** one button, Open it. No sign-up or login. Line: "Free for you. No sign-up."
- On Open it: the envelope opens (seal breaks, flap lifts, 400 ms, success haptic) → P1. The anonymous account and couple link are created in the background while the animation plays.
- If the partner leaves here: push 2 hours later "Your note from \[Partner\] is still sealed."

### P1 The note, opened

- **Shows:** FROM \[PARTNER\] · OPENED · the full love note, large, in quotes, signed "— \[Partner\]" · then a black card: YOUR PART · "\[Partner\]'s done theirs. They think they've found the pattern behind your arguments." · "Show them who you really are. About 4 minutes."
- **Options:** Do my part → P3 · Write one back first → P2
- The note stays in Settings → "Your notes" for the whole 90-day test, and resurfaces on Home after the first bad day.

### P2 Write one back

- **Shows:** the same screen as 3.1 with the names swapped: P2 · WRITE ONE BACK · "What do you love about \[Partner\]?" · "Pick up to three. We'll seal it and send it to \[Partner\]. Only they can open it." · same chips (top two preselected) · same prefilled box: "\[Partner\], I know there are things we need to improve, but here's what I love about you and why I'll keep choosing us: \[chip phrases\]." · lock line "Sealed for \[Partner\]".
- **Options:** Seal it for \[Partner\] → P3 · Back arrow → P1
- **Sends:** push to the initiator "\[Me\] sealed a note for you" / "\[Me\] joined, and wrote something about you. Tap to open it." The words are never in the push. Tapping it plays the envelope opening, then shows the note: FROM \[ME\] · OPENED · the note · black card "\[ME\] HAS JOINED · \[Me\]'s doing their part right now. When they're done, you'll both see how well you know each other, and your 90-day test starts." · Back to Today.
- **Saves:** love\_note\_text, love\_note\_chips, love\_note\_sealed\_at (partner's). Both notes live in Settings → Your notes.

### P3 Safety question

Same screen, rules and support screen as 1E.6 / 1E.6S, about the initiator. Answer never shared.

- **Options:** No / I'd rather not say → P3b · Sometimes / Yes → 1E.6S

### P3b About you

The partner answers Part B about themselves (1B.0–1B.11, same screens, same copy), with the intro: *"Now you. \[Partner\] has already told us how you come across. Here's your chance to say who you really are."*

- **After 1B.11** → **How well do you know each other?** card: *"\[Partner\] got \[n\] of 9 right about you."* plus the one they got most wrong, e.g. *"\[Partner\] thinks you need space when upset. You said you want comfort."* → **Continue** → P4
- The insight engine (Part F) reruns with both people's own answers. The initiator sees their own **How well do you know each other?** card next time they open Home.
- **Saves:** the partner's my\_type, conflict\_style, my\_upset\_need, my\_love\_style, my\_trigger, my\_stress, my\_repair, my\_recovery

### P4 The one thing

- **Shows:** *"If \[Partner\] changed one thing, what would help most?"* Same screen and scoring as 1G.1, from the partner's side. Votes come from the initiator's cycle\_type and from the dynamics found using both people's own Part B answers. Two buttons first: \*\*Help me work it out\*\* → the six scenario questions (1D.10–1D.15, about the initiator) → the list · \*\*I know what I'd pick\*\* → straight to the list.
- **Options:** any answer → P4b · Write my own → text field (5–60) → **Continue** → P4b
- **Saves:** one\_thing\_for\_partner (partner's). Both have now picked, so goal\_start = today.

### P4b Your own thing (partner)

Same screen as the initiator's own-thing picker, from the partner's side.

- **Shows:** "And your own thing? Something you'll check yourself. Only you see it." · top suggestion from his argument type (from his P3b answers, using the Solo table) marked BEST FOR YOU · 2 more suggestions · See all options.
- **Options:** **Pick it** → P5 (required, no skip).
- **Saves:** own\_thing (partner's). He starts checking it the same night the test starts.

### P5 The reveal

Shown now to the partner; the initiator sees the same reveal next time they open Home (plus a push).

- Shows: "Your 90-day test starts today." · "\[Partner\] picked for you: \[initiator's pick\]" with what good looks like · "You picked for \[Partner\]: \[partner's pick\]" · "First check-in tonight at \[checkin\_time\]. Every night, you each tap whether the other kept to it."
- **Options:** **Got it** → P6

### P6 Check-in time

- **Shows:** *"\[Partner\] checks in at \[initiator's time\]. Same for you?"*
- **Options:** **Yes, same time** → P7 · **Pick a different time** → time picker (as 2.1c) → **Continue** → P7
- Then the notification permission screen (as 2.2) if needed.
- **Saves:** checkin\_time (partner's).

### P7 Patient

- **Shows:** *"Are you ready to be patient with \[Partner\] as \[Partner\] improves?"*
- **Options:** Yes, I'll be patient · I'll try my best → both go to the P8 branch

### P8 Branch on the couple's subscription state

| sub\_state | Partner goes to |
| --- | --- |
| Trial active or Subscribed | P9 "You're both in" → Home |
| Invited (initiator hasn't reached a decision yet) | P10 Waiting → Home (waiting state) |
| Pulled back | P11 Takeover |

### P9 You're both in

- **Shows:** *"You're both in. Your first check-in is tonight at \[time\]."*
- **Options:** **Go to Home** → Home

Then a one-tap sign-in card, worded for the partner: "One tap to keep your side safe. Nothing to pay." · Sign in with Apple · Sign in with Google · Later. Same upgrade as 6.1b. Later → Home shows the slim "Keep your progress safe" bar until it's done. Shown only once the couple has paid (here, or when P10 turns into "You're both in"), so the partner is never asked for anything before payment either.

### P10 Waiting

- **Shows:** *"\[Partner\] is finishing setting up. We'll let you know when you're both ready."*
- **Options:** **OK** → Home (waiting state). If the initiator then pays → push *"You're both in."* If the initiator pulls back → the partner's next open goes to P11.

### P11 Takeover

Never says or hints that the initiator declined.

- **Shows:** *"\[Partner\]'s already done the hard part. \[Partner\] has named what you're both working on, and wanted to make the final decision with you. All that's left is starting. Want to be the one who makes it happen?"*
- **Options:** **Let's start** → 4.3 → 5.1 → 6.1 (same screens, names swapped, the partner becomes payer) · Close X → *"Leave for now?"* sheet; leaving keeps everything saved.
- **If the partner pays:** initiator gets *"\[Partner\]'s covered it. You're both in."* and full access free.
- **If nobody pays:** both stay Pulled back. Either person can open Loveth later and go straight to 6.1; no questions repeated.

## After onboarding — Home, check-in, calendar, settings

Home is one screen whose cards change with the couple's state. The daily check-in is the product; everything else supports it.

### H1 Home

#### Today screen and the nightly check (final layout, Oct 2026)

This is the approved layout. It overrides Home order (below) and earlier H1 and C1 details where they differ. Mockups of all four states are in the repo: docs/loveth/screens (Chubyilo92/CoupleIn).

**The idea:** Today has one job per moment. In the day, it shows the one thing you're doing. At check-in time, the same screen turns into the check. Nothing else moves, so it always feels like the same page.

**Daytime (04:00 until check-in time), top to bottom**

1. **Header:** the date in mono ("Wednesday 7 October"), "Hi, \[Me\]", both avatars.
2. **Day progress, directly under the name.** "Day \[n\] of 90" plus a reward line, a 90-segment bar (days done = ink, today = accent) and milestone marks under it: Start · 30 · 45 · 60 · 75 · 90. Reward lines: Day 1 "Day one. The hardest part's done." · Days 2–22 "Building the habit" · 23–44 "A quarter of the way" · 45–59 "Halfway there" · 60–74 "Two thirds done" · 75–89 "The final stretch" · 90 "You made it". When the night is locked in, today's segment fills with the same 220 ms fill as the calendar square.
3. **Hero card: Your action today.** DO or DON'T badge, then "\[Partner\] asked you:" and the action in the partner's own words, in the serif (Newsreader), in quotes. Footer: "\[Partner\] checks you at \[time\]" and their private run ("5 in a row"). Slim own-thing row at the bottom of the same card. The action is always shown as a quote from the person who picked it, so first-person wording like "Ask how I'm really doing" reads correctly on the other person's phone.
4. **We're arguing right now:** one full-width button with the accent pause icon and "Talk it through, step by step".
5. **Hard week row** (hard week route): collapsed to one switch row when off. While support is running it expands into one card: the switch, "Your week · day \[n\] of \[window\]", the latest support line, and Take 20 minutes · It's a lot for me too.
6. **Tonight line:** "Tonight at \[time\] · You asked \[Partner\]:" with the partner's action quoted in the serif, and a bell hint "We'll remind you at \[time\]. Your check opens right here."
7. Status slot (agreement, trial, invite) and the below-the-fold bars, as in Home order.

**At check-in time (until 04:00): same screen, only the top changes**

- The hero card is replaced by **Tonight's check**: accent label "TONIGHT'S CHECK · OPEN UNTIL 04:00", "You asked \[Partner\]:" and the quote, "Did \[Partner\] keep to it today?", and the two answers right on the card: **Yes, \[Partner\] did** (white, GOOD DAY) · **No, \[Partner\] didn't** (black, BAD DAY).
- Your own action moves into a small grey card under it: "Your action · \[Partner\] checks you tonight" and the quote.
- The Tonight line disappears, because the check is live. We're arguing right now and the Hard week row stay exactly where they were.
- **How the app tells them:** the push at check-in time ("How did \[Partner\] do today? 10 seconds."), a "1" badge on the app icon from check-in time until they lock in, and a small accent dot on the Today tab if they're on Calendar or You.
- After locking in, the card reads "Day \[n\] locked in" with the partner's status until 04:00.

**The check (C1, as approved)** Opened from the push, the card, or by tapping Yes or No on the card (that answer arrives pre-selected). Top: "Day \[n\] · Tonight's check" and a close ×. Then: "You asked \[Partner\]:" and the quote · "Did \[Partner\] keep to it today?" · two large answer buttons · the own-thing row ("…Did you?" Yes / No) · the We argued today checkbox · + Add a note for \[Partner\] (optional; Something crossed the line lives inside the note) · the line "Missing a night tells \[Partner\] you're not noticing the effort." · **✓ Lock in Day \[n\]**.

#### Home order (final, Oct 2026): overrides earlier H1 layouts where they differ

Top to bottom. Nothing is removed: lower-priority cards wait for the status slot or sit below the fold.

1. Thin bars, only when needed: offline · notifications off · Keep your progress safe.
2. Header: "\[Day\] \[date\] · Day \[n\] of 90", "Hi, \[Me\]", both avatars. No settings gear (settings live in the You tab).
3. Main card. From check-in time to 04:00: Tonight's tap. Otherwise the first state that applies: partner not joined · partner picking · reveal · your action. Your action card holds your own-thing row inside it.
4. &#91;Partner\]'s action card (smaller).
5. The two tiles: Tonight's check · We're arguing right now. On the hard week route, the slim Hard week switch row sits directly under the tiles, always visible.
6. One status slot, showing only the highest that applies: Hard week support card > agreement card (7 days after Resolve) > trial card (payer, during the trial) > invite card (partner not joined).
7. Below the fold: days without a fight · good days together this month · next milestone (thin bars) · last 7 days.

- **Header:** *"Day \[n\] of 90"* (counted from goal\_start; before both have picked: *"Getting started"*) · settings gear (top right) → S1.
- **Trial card** (payer only, during trial): *"Free trial: \[x\] days left."* If the partner hasn't joined, adds *"\[Partner\] hasn't joined yet."*
- **Notifications banner** (only if notifications are off): *"Turn on notifications so you don't miss a check-in."* → phone notification settings.

**Standard daytime view (before tonight's tap opens).** This is what users see most of the time, so it keeps their own action front and centre all day.

- Header: *"***\[Day\] \[date\] · Day \[n\] of 90" and a large "Hi, \[Me\]" so it's always clear whose phone this is. Top right: both initials, the user's filled and labelled "You", the partner's outlined (photos replace them once added)**.
- **Your action today** card (largest element): the user's daily action, *"\[Partner\] taps for you tonight"* and their own run (*"5 in a row"*), which only they see.
- **\[Partner\]'s action** card (smaller, grey): their action and *"You tap for \[Partner\] at \[time\]"*.
- **Good days together · this month:** *"\[n\] / 20"* with a progress bar to the target.
- **Next milestone:** name and progress (*"14 nights both checking in · 12 / 14"*).
- *Two equal option tiles under the action cards: \*\*Tonight's tap\*\* ("Opens \[time\] · in \[countdown\]") and \*\*We're arguing right now\*\* ("Talk it through", orange-red icon) → Resolve R1. Shared progress (good days together, next milestone) sits below the tiles as two thin bars*.
- **Tab bar:** **Today** (this screen) · **Calendar** (both 90-day calendars, C2 layout) · **You** (photo, settings, subscription).
- From check-in time until 04:00, the top of this screen is replaced by the **Tonight's tap** card (below).

The main card shows the first state that applies:

| State | Main card shows | Options |
| --- | --- | --- |
| Partner not joined | *"\[Partner\] hasn't joined yet. Your first check-in starts when \[Partner\] joins."* | **Resend invite** → share sheet (3.2) · **Copy link** → clipboard + toast |
| Partner joined, hasn't picked | *"\[Partner\] is picking one thing for you."* | **Nudge \[Partner\]** → push to partner; button disabled for 12 hours after |
| Reveal not yet seen | Opens the reveal (P5) full screen | **Got it** → Home |
| Before today's check-in time | *"Tonight at \[time\]: how did \[Partner\] do with \[their one thing\]?"* | None (check-in opens at the time) |
| Check-in open, not answered | *"How did \[Partner\] do today?"* | **Check in** → C1 |
| Answered | *"Done for today."* + partner status (*"\[Partner\] hasn't checked in yet"* or their answer about you) | **Change my answer** → C1 (until the window closes) |
| Pulled back / Lapsed | *"Pick up where you left off."* | **Continue** → 6.1 |

Below the main card, once both have picked:

- **Your one thing** card: what the partner picked for you.
- **\[Partner\]'s one thing** card: what you picked for the partner.
- **Calendar** card (last 7 days preview) → H2.

### C1 Nightly tap

#### C1 final (Oct 2026): overrides every earlier C1 detail

One screen, one version:

- Label "\[Name\]'s daily action" and the action in full.
- Question "Did \[Name\] keep to it today?" Buttons: **Yes, \[Name\] did** (white, Good day) · **No, \[Name\] didn't** (black, Bad day). Always the name, never he, she or they.
- Under a thin rule: YOUR OWN THING · ONLY YOU SEE THIS, the action, "Did you?" with small Yes / No (optional).
- Checkbox **We argued today** (feeds days without a fight).
- **Add a note** (collapsed; opens automatically on No). Inside the note sheet: the toggle **Something crossed the line** ("Rudeness, or attacking family").
- Line above the button: "Missing a night tells \[Name\] you're not noticing their efforts."
- Button **✓ Lock in Day \[n\]**, enabled once Yes or No is picked → the square fills, success haptic, "Day \[n\] locked in" → tonight's moment (see One moment a night, under C5).
- Colours everywhere, including the 2.1b demo: white = good, black = bad, grey = missed, accent = crossed the line. Never green or red.

**Three ways in to tonight's tap:**

1. **Home (H1):** from check-in time until 04:00, the top card is **Tonight's tap**: *"Did \[Partner\] keep to it today?"*, the action, *"Open until 04:00"*, and the **Yes** / **No** buttons right on the card. Tapping either opens C1 with that answer already selected (and the note open if No).
2. **The nightly push:** tapping it opens C1. Long-press on iOS (or expand on Android) shows **Yes, \[he/she/they\] did** and **No** as notification actions; either opens C1 with the answer selected, so they can add a note and submit.
3. **Home is also where they see their own action** (*"Your action · \[Partner\] taps for you"*, with their current run) and both partners' last 14 days, with **Both calendars** opening the full view (C2 layout).

One question, the same every night: did they keep to their action? **Yes is always a good day**, for every Do and every Don't. Five seconds.

- **Window:** opens at the user's checkin\_time, closes at 04:00 the next morning (user's time zone). Not answered by then = **Missed** for the partner's day, charged to the person who didn't tap.
- **Shows:**
  - Label *"\[Partner\]'s daily action"* and the action in full (e.g. *Don't criticise me without acknowledging what I also do well*)
  - Question: **"Did \[Partner\] keep to it today?"**
  - Two large buttons: **Yes, \[he/she/they\] did** (white, labelled *Good day*) · **No, \[he/she/they\] didn't** (black, labelled *Bad day*). Pronoun comes from the partner's profile; *they* if not set.
  - **Add a note** (collapsed): a text box, up to 200 characters, placeholder *"What happened? Keep it short and kind. \[Partner\] will see this."* It **opens automatically when No is tapped**, and stays optional.
  - Toggle: **Something crossed the line today** (helper: *"Rudeness, or attacking family"*)
  - Line above Submit: *"Missing a night tells \[Partner\] you're not noticing their efforts."*
- **Result:** Yes → Good day · No → Bad day · toggle on → Crossed the line, whatever the answer.
- **Options:** **Submit** (enabled once Yes or No is tapped) → C2 · Close → Home, nothing saved. The answer and note can be changed until the window closes.
- **Saves:** a day {date, from\_user, about\_user, kept (yes/no), result (good / bad / crossed / missed), note}. The first of the two to submit triggers the partner push *"\[Partner\] just checked in. Your turn."*
- The "Nightly question" column in the daily action table is no longer shown in the app; C1 always asks *"Did \[Partner\] keep to it today?"*

### C2 After the tap

Both people see both calendars, so each can watch the other's progress.

**Card order rule:** the two day cards follow the tap screen: a **good day card always sits on the left** (white), a bad day card on the right (black). If both days are the same, **Your day** goes on the left.

**Runs are private (no head-to-head):** each person only ever sees their own run and their own totals. The partner's calendar is visible (that's the accountability) but never with counts, runs or totals next to it. The numbers shown to both are shared ones only: good days together this month and milestones. This stops the app turning into a scoreboard between partners.

- **Shows:**
  - Headline *"Done for tonight."* and *"Day \[n\] of 90"*
  - **\[Partner\]'s day** card: Good day or Bad day as you just tapped, with your note if you wrote one
  - **Your day** card: \[Partner\]'s tap about you, their note if any, and your current run (*"5 in a row"*). If \[Partner\] hasn't tapped yet: *"Waiting for \[Partner\]. We'll let you know."*
  - **Two 90-day calendars**, \[Partner\]'s first, then yours. Each: name, the daily action* and a grid of 90 squares (15 across, 6 down). Only \*\*your own\*\* calendar shows totals ("\[n\] good · best run \[n\]"); your partner's shows the days with no totals*
  - Key: **Good** = white square · **Bad** = black square · **Missed** = grey · **Crossed the line** = orange-red · future days = faint outline · today = ink ring
  - Line: *"A grey day means the other person didn't tap. Missing a night tells your partner you're not noticing their efforts."*
- **Options:** tap any past square → sheet with that day's result and note · **Done** → Home
- **Same calendars on Home** (H2) any time, for both people.

### C3 When you both kept to it (feel-good)

Shown instead of C2 when both people have tapped and **both days are good**. The point is to make a good night feel like a shared win.

- **Shows:**
  - *"Day \[n\] of 90 · Both tapped"* · headline **"You both kept to it tonight."**
  - **Good days together this month:** a big *"\[n\] / 30"*, where a good day together = both people had a good day. A strip of 30 squares fills in white (good together), black (at least one bad), grey (missed) and outlined (still to come).
  - **Monthly target: 20 of 30 good days together.** Always 20, never editable by the couple, so nobody sets a target too ambitious to hit. Once reached: a tick and *"Target 20 · reached on day \[n\]"*. Before then: *"\[x\] more to reach 20"*.
  - *One card: your own current run ("Your run · only you see this · 9 in a row"). Your partner's run is never shown to you*.
  - One positive line, first that applies: best month so far → *"Your best month so far, and \[n\] days still to go. This is what breaking the cycle looks like."* · target just reached → *"You hit your target. That's a month of keeping your word to each other."* · otherwise → *"Another night you both showed up. That's how it changes."*
- **Options:** **Done** → Home · **Send \[Partner\] a well done** → push to the partner: *"\[Me\] says well done for today."*
- **Months** run in 30-day blocks from the start of the cycle (days 1–30, 31–60, 61–90).

### C4 After a bad day (encouragement)

Shown to the person who **got** a bad day, the next time they open the app after their partner's tap (or from the push). It's not shown to the person who gave it.

- **Shows:**
  - Headline **"\[Partner\] says today wasn't your day."**
  - &#91;Partner\]'s note, if they wrote one
  - **Before today:** a big *"\[n\] of \[n\] good days"* and the strip of their days so far
  - One line built from their record: more good than bad → *"One bad day doesn't undo \[n\] good ones."* · fewer good than bad → *"It's early. Every good day from here moves the line."* · first bad day after a run → *"That's your first bad day in \[n\]. The run was real."*
  - *"Changing a habit takes weeks, not days. Bad days are part of it. What counts is the trend."* The last sentence adds *"and yours is going the right way"* only when the last 7 days have more good days than the 7 before.
- **Options:** **Tomorrow's a clean slate** → Home
- **Never** shown as a push with the result in it; the push just says *"\[Partner\] has checked in."*

### C5 Milestones

#### One moment a night (Oct 2026): overrides the order rules below

After the tap, each person sees at most one full-screen moment per night. If several are due, the highest shows and the rest wait for the following nights, one each, shown with their real date ("Reached on day \[n\]"):

1. Day 90 (G1)
2. C4 after a bad day (encouragement always comes first after a bad day)
3. Days without a fight (3, 7, 30, 100)
4. Check-in milestones (3 good days, 7 nights, 14 nights, 30, 45, 60, 75)
5. Your own thing: "This one's yours now"
6. Intimacy then and now (intimacy route)
7. Otherwise C3 (both good) or C2

A milestone's push is sent on the night its screen is shown, not before.

Three milestones mark the early wins. Each is shown full screen to **both** people the first time it's reached in a cycle, straight after the second person taps, in place of C2 or C3.

| Milestone | Trigger | Big number and line | Body copy | Shows |
| --- | --- | --- | --- | --- |
| **3 good days together** | Both people had a good day 3 nights in a row (no bad, missed or crossed-the-line days for either) | **3** · *"Good days in a row. Both of you."* | *"Three days, no issues. You both kept your word, and you both noticed. That's the cycle starting to break."* | Both people's 3 days as white squares, tonight ringed · progress to the next milestone: *"Next · 7 nights of both checking in"* with \[n\] / 7 |
| **7 nights both checked in** | Both people tapped 7 nights in a row, **whatever the result** (good or bad days both count; a missed night by either resets it) | **7** · *"Nights in a row. You both showed up."* | *"Good days or bad, neither of you missed a night. Showing up for each other every evening is the habit everything else is built on."* | Both people's 7 days (white and black as they were), tonight ringed · *"14 of 14 check-ins · 0 missed"* |

- **Options (both):** **Keep it going** → Home · **Send \[Partner\] a well done** → push *"\[Me\] says well done for today."*
- **Push to both** when reached: *"Milestone unlocked. Open to see it together."*
- **Both on the same night:** show the 7-nights screen first, then the 3-days screen.
- **Calendar:** the day a milestone was reached gets a short bar under its square on both calendars.
- **Once per cycle each.** A new cycle (after Day 90) can earn them again.

**14 nights both checked in** (the third milestone)

- **Trigger:** both people tapped 14 nights in a row, whatever the result. A missed night by either resets it.
- **Shows:** a huge **14** · *"Two weeks. Every night, together."* · 14 ticked squares (ticks, not results, so nobody's bad days are on show) with tonight in orange-red · *"28 of 28 check-ins · 0 missed"* · *"Two weeks of noticing each other, every single night. Habits form in weeks like these. You're no longer trying it. You're doing it."* · progress to the monthly target: *"Next · 20 good days together this month · \[n\] / 20"*
- **Fallback, "Two weeks in":** if the couple reaches Day 14 of the cycle without a 14-night run, they get a softer version on Day 14 instead: **14** · *"Two weeks in."* · *"\[n\] of 28 check-ins. You're still here, still working on it. That matters."* Shown once; the full milestone can still be earned later in the cycle.
- Same options, push and calendar marker as the other milestones.

**Check-in milestones: 30, 45, 60, 75.** These count nights you **both checked in**, added up across the test. Good or bad days make no difference, missed nights never reset the count, and the screen never shows a good-day number. Each one appears once per person, straight after the tap that reaches it, plus a push to both. If a milestone isn't reached by Day 90 it's skipped. Visual: all 90 nights as a 15 × 6 grid. Checked in = outlined square (never black, because black means a bad day), missed = dashed, tonight = accent, still to come = grey. Footer: "\[n\] NIGHTS YOU BOTH CHECKED IN · DAY \[d\] OF 90" and a bar to the next milestone. Each milestone does one job:

| Nights | Headline | Copy | Primary · secondary | Why it's there |
| --- | --- | --- | --- | --- |
| 30 | A month of showing up. | "30 nights you both stopped and noticed each other, good days and bad. Showing up is the part most people skip. You haven't." | Keep going · Read \[Partner\]'s note again | Brings the sealed note back right when motivation dips. |
| 45 | Halfway. | "45 nights in. This is where habits usually wobble. One quick question for each of you, answered privately. You'll only see what you both said." | Answer one question · Later | The halfway check-in: "Is \[the action\] getting easier for \[Partner\]?" Easier · About the same · Harder. Only shown back once both answer, as plain words ("You both said it's getting easier"), never a score. If either says Harder: "That's normal at halfway. Want to talk it through?" → Resolve, or Keep going. |
| 60 | Two months in. | "You've watched \[Partner\] try for 60 nights. Tell \[Partner\] one thing you've noticed change. We'll seal it, like your first note." | Tell \[Partner\] what you've noticed · Keep going | Reuses the sealed note: chips from the action ("You put your phone down more", "You let me finish"…) and a prefilled box "\[Partner\], I've noticed…". |
| 75 | 15 to go. | "Day 90 is \[weekday date\]. You'll both see all 90 nights side by side, and decide what's next together." | Keep going · What happens on Day 90 | Sets up Day 90 two weeks early, so the ending feels planned. Monthly subscribers also see one quiet line below: "Planning another 90 days? Yearly saves you 58%." |

## Resolve — "We're arguing right now"

The same concept as CoupleIn's Resolve, in this app's UI: no typing, a guided step-by-step process where each person speaks while the other listens, and the listener says back what they heard before replying. Two additions: **AI voice recording** (each person speaks, the AI turns it into a calm summary) and **suggested solutions** the couple choose from. It works with both people in the room, or apart.

**Rules for every Resolve session**

- **One person speaks, the other listens.** Turns are 2 minutes, with a visible timer. The listener's screen shows *"Just listen. Your turn is next."*
- **Say back before you reply.** After each turn, the listener says back what they heard. The speaker confirms **That's it** or **Not quite** (then 30 seconds to clarify, and the listener tries again).
- **The AI never takes sides.** Summaries are written neutrally (*"Sarah felt…"*, never *"Mark was wrong…"*), with insults and swearing removed. It never says who is right.
- **Always show who is acting.** Every Resolve screen that belongs to one person names them and shows their initial avatar (initiator = warm sand, partner = cool slate, as in the warmth pass; photos replace them). Speaking turn: a 40 pt avatar + name + red "SPEAKING" dot at the top; the listener's row shows their avatar + "\[Name\], just listen." Say-it-back: the progress steps use the avatars, "WHAT \[NAME\] HEARD" carries the listener's avatar, and the question carries the speaker's ("\[NAME\], YOUR CALL"). Picking solutions: "\[Name\] is picking · \[OTHER NAME\] NEXT". Summary cards keep the avatar per person. On one shared phone, this is how both people know whose turn it is at a glance.
- **Recordings are private and temporary:** audio is turned into text, then deleted. Only the summaries and the agreed solution are kept.
- **Below-the-belt guard:** if a recording contains insults or attacks on family, the summary leaves them out and shows the speaker *"We left out the personal attacks. Try saying how it made you feel."*
- **Safety:** every Resolve screen has a small **I don't feel safe** link → the support screen (1E.6S).

### R0 Entry

- **Today screen:** **one of the two option tiles under the action cards: We're arguing right now (orange-red pause icon, "Talk it through"**). Always visible, any time of day.
- Also in the **You** tab and as a long-press option on the app icon (quick action).

### R1 Are you together?

- **Shows:** *"Are you and \[Partner\] together right now?"*
- **Options:**
  - **Yes, we're together** → R2T
  - **No, we're apart** → R2D
  - **Cancel** → Today

### Together (one phone, taking turns)

| Screen | What happens |
| --- | --- |
| R2T Set up | **"Who's upset?"** Sub-line: "The person who's upset speaks first, whoever is holding the phone. The other listens, then says it back." Cards: **\[Me\]** (speaks first, \[Partner\] listens) · **\[Partner\]** (speaks first, \[Me\] listens) · **Both of us** → "Who was upset first?" → that person speaks first. There is **no default to whoever opened the app**: the person who caused the issue often grabs the phone first, and letting them speak first feels unfair. Helper line: "If you were the one who caused it, let them go first. You'll get your turn." **Start · \[Name\] first** → R3T. One round only if one person is upset; after R4 the listener can still add **I have something too**. Saves: upset\_first. |
| R3T Speak | *"\[Name\], what's upsetting you? \[Other\], just listen."* Big record button, 2:00 countdown, live waveform. **Done** (or timer ends) → R4T |
| R4T Say it back | *"\[Other\], say back what you heard \[Name\] say."* Record (up to 1 minute). Then *"\[Name\], did \[Other\] get it right?"* **That's it** → swap turns (R3T for the other person) · **Not quite** → \[Name\] records a 30-second clarification → \[Other\] says it back again |
| R5 What you both said | After both turns: three AI cards. **\[Me\] said** (2–3 lines) · **\[Partner\] said** (2–3 lines) · **Where you agree** (1–2 lines). **Looks right** → R6 · **Go another round** → R3T (max 3 rounds) |
| R6 Pick a way forward | 3 AI-suggested solutions, each one line plus one line on why. Each person ticks **every** option they could live with; on one phone, they take turns and the first person's ticks are hidden from the second. Also: **Write our own** and **We need a break first** (sets a 20-minute timer, then resumes at R6) |
| R7 Agreed | Shows the solution both ticked: *"You both chose: \[solution\]"*. If several match, the one with the most shared ticks. If none match: *"No match yet. Here's the closest:"* with the option both ranked highest, and **Try new suggestions** (3 more) |

### At a distance (two phones)

| Screen | Who | What happens |
| --- | --- | --- |
| R2D Reach out | Initiator | *"We'll let \[Partner\] know you want to sort this."* Push to the partner sends straight away. Then **While you wait, say your side** → R3D |
| Push | Partner | **\[Me\] is worried. Do you want to talk?** Body: *"\[Me\] wants to sort things out with you."* Actions: **Yes, let's talk** · **Give me a bit** |
| R2D-wait | Partner | If **Give me a bit**: *"When can you talk?"* **30 minutes** · **1 hour** · **Tonight** (at check-in time). The initiator sees *"\[Partner\] will be ready in \[time\]."* Both get a push when the time comes. No option to refuse outright: *"Give me a bit"* is the way to say not now |
| R3D Your side | Each person, on their own phone | Records up to 2 minutes. The AI writes a calm summary. **They see it before it's sent:** *"Here's what \[Partner\] will see"* · **Send** · **Record again** |
| R4D Read and say back | Each person | Reads (or listens to a voice read-out of) the other's summary, then records saying it back. The other person gets a push *"\[Name\] heard you. Did they get it right?"* → **That's it** · **Not quite** (records a 30-second clarification, which goes back to the listener) |
| R5 What you both said | Both | Unlocks once both sides are said back and confirmed. Same three cards as together. |
| R6 Pick a way forward | Both, separately | Each ticks options on their own phone, blind. Push to the other: *"\[Name\] has picked. Your turn."* |
| R7 Agreed | Both | Revealed to both at once when the second person submits. Push: *"You've found a way forward."* |

- **Order at a distance:** the initiator's side goes first. Once the partner has said it back and it's confirmed, the partner records their side. Steps can be done minutes or hours apart.
- **Session expires** after 24 hours if nothing happens. Both get *"Your Resolve session closed. Start again any time."*

### After Resolve

- **R7 options:** **Done** → Today · **Save to our agreements** (a list under the You tab, each with its date).
- **Tonight's tap is unchanged:** Resolve doesn't mark anyone's day. The C1 note box shows a hint: *"You used Resolve today. Did \[Partner\] keep to their action during it?"*
- **History:** a small Resolve marker on the calendar day (both calendars), with no detail.
- **Data saved:** session {date, mode (together / distance), rounds, solution\_options, picks (per person), agreed\_solution}. Audio is never kept.

### Gap fixes (kept deliberately simple)

| Gap | Fix |
| --- | --- |
| Too heated to start, or one person walks off mid-session | **Take a break** on every Resolve screen (top right, next to close). Starts a 20-minute timer on both phones: *"Taking 20 minutes. We'll bring you both back at \[time\]."* with three short lines: leave the room, no texting about it, do something calming. Options: **We're ready now** (resumes at the same step) · **End for today**. The session is saved and can be resumed for 24 hours. |
| At a distance, the initiator can't tell if the partner has seen it | A **status card** on the initiator's screen: *Sent \[time\]* → *Seen \[time\]* → *\[Partner\] is ready at \[time\]* (or *Ready now*). While waiting: **Say your side now** (R3D) and **Cancel**. If it's not seen within 1 hour: *"\[Partner\] hasn't seen it yet. Say your side now, and it'll be ready when they open the app."* |
| Agreements are made and forgotten | For 7 days after R7, Today shows an **agreement card**: *"Your agreement · \[solution\] · day \[n\] of 7"*. On day 7 both get *"Is your agreement working?"* → **Yes, keep it** · **Sort of, tweak it** (opens R6 with the agreement pre-ticked plus 2 new suggestions) · **No, try again** (opens R6 with 3 new suggestions). Each answers separately; the result shows once both have answered. Kept agreements stay in the You tab. |
| Apart mode when the partner hasn't joined | On R1, **No, we're apart** becomes *"\[Partner\] hasn't joined yet"* with **Send your invite** (3.2). Together mode still works on one phone. |

### Notifications added by Resolve

| Trigger | To | Message | Opens |
| --- | --- | --- | --- |
| Initiator starts at a distance | Partner | \[Me\] is worried. Do you want to talk? / \[Me\] wants to sort things out with you. | R2D partner choice. After **Yes, let's talk**, the partner is asked "Do you have something to discuss too?" **Yes** (two rounds, the initiator goes first) · **No, I'll listen** (one round). |
| Chosen wait time reached | Both | Ready to talk? / \[Partner\] said now works. | Next step |
| Your side has been said back | Speaker | \[Name\] heard you. Did they get it right? | R4D confirm |
| Other person picked solutions | The one who hasn't | \[Name\] has picked. Your turn. | R6 |
| Agreed | Both | You've found a way forward. | R7 |

### H2 Calendar

- **Shows:** 90-day grid from goal\_start. Two rows per day: one for each person, showing how that person did (as answered by the other). Each day labelled in words, not colour alone: Good day (white) · Bad day (black) · Missed (grey) · Crossed the line (orange-red). Same layout as C2. Future days empty.
- **Options:** tap a past day → bottom sheet with both answers for that day · Back arrow → Home

### G1 Day 90

- **Shows:** *"90 days. You broke the cycle together."* plus good days together out of 90 and days without a fight. Each person also sees their own good days and best run, privately (never the other person's, as in C2).
- **Options:** **Keep the same things** → new 90 days starts tomorrow · **Pick new things** → both pick again (P4 screen, blind reveal again) → new 90 days starts when both have picked

### S1 You (profile and settings)

The **You** tab (third tab: Today · Calendar · You). One scrolling screen, iOS grouped-list style, no nested menus deeper than one level.

| Section | Row | What it does |
| --- | --- | --- |
| Header | Avatar + name + "With \[Partner\] · Day \[n\] of 90" + **Add a photo** | Camera badge on the avatar opens camera / photo library / remove. Square crop, shown as a circle everywhere the initial shows today (Home, Resolve, notes). No photo = initial (warm sand for initiator, cool slate for partner). |
| Profile | Name | Edit field, 1–20 characters. The partner sees the change everywhere. |
| Profile | Account | Not shown before payment. After 6.1b: "Signed in with Apple / Google" and the email they shared. Signing in on a new phone brings everything back. No email field, no password. |
| Your 90-day test | What you asked \[Partner\] for | Read-only: the action and what good looks like. |
| Your 90-day test | Change focus | Opens the Change focus sheet (below). |
| Your 90-day test | Your notes | Both sealed love notes, newest first. |
| App | Check-in time | Time picker. New time applies from tomorrow. |
| App | Notifications | On / off per type: nightly tap, milestones, Resolve requests (always on, can't turn off). Links to system settings if denied. |
| App | Plan | Monthly / Yearly + renewal date · Manage → App Store / Google Play subscriptions page. |
| Help | Restore purchase | Restores the store subscription to this device. |
| Help | I don't feel safe | Opens 1E.6S support screen. |
| Help | Delete my data | Two-step confirm. Deletes their account (revoking the Apple sign-in token, as Apple requires) and this person's answers, taps and notes; the partner is told "\[Name\] has left." and the couple's test ends. |

**Change focus sheet:** "You're on day \[n\] of 90. Changing what you asked \[Partner\] for restarts the test at Day 1 for both of you. \[Partner\] sees the new one before it starts." Options: **Pick a different thing** → the 1G.1 list (top suggestion hidden, current pick marked) → \[Partner\] gets "\[Me\] changed what they're asking for" and sees it → new Day 1 tomorrow · **Retake the questions** → Stage 1 Parts B–E with previous answers preselected → new report → pick → restart; the current test keeps running until they pick · Note: "The test works by keeping one thing for 90 days. Bad weeks are part of it, not a sign to switch." · **Keep going** (primary, closes the sheet). Limit: one change per 14 days. Saves: focus\_changed\_at, focus\_change\_reason.

## Calendar tab (replaces H2 where they differ)

#### One calendar (final, Oct 2026)

- The Calendar tab month grid is the only full calendar. It replaces H2 and its two-row grid. The two 90-day calendars in C2 become a compact 15 × 6 strip per person with the same squares, and See full calendar → Calendar tab.
- Squares: white = good · black = bad · grey = missed · accent fill = crossed the line · faint outline = still to come.
- Markers, never in the accent: tonight = ink ring · argument or Resolve day = small ink corner · milestone = short bar under the square · note = dot under the date.
- The accent means one thing on a calendar: crossed the line.

* **Toggle at the top:** Your days (how \[Partner\] marked you) · \[Partner\]'s days (how you marked them). Opens on Your days.
* **Month grid:** each day of the test is a square with its date. White outlined = good, black = bad, grey = not tapped, accent = crossed the line, ink ring = tonight, pale = still to come. A small dot under the date = there's a note.
* **Under the grid:** Good · Bad · In a row for this month, then "Tap any day to see what happened."
* **Tap any day → day sheet** (slides up, calendar stays behind): date + day number, GOOD / BAD tag, "\[Partner\] said you kept to it / didn't keep to it.", the action, **\[Partner\]'s note** in the serif with the time it was written, then a slim row with your own thing for that day (you did / you didn't / not answered; only you see it). **One button: Got it. No link into Resolve from past days, so looking back can't restart old fights.**
* On \[Partner\]'s days the sheet shows your tap and your note, with **Edit** for 24 hours after the tap, then locked.
* Solo users see only Your days; solo nights before the partner joined sit in an earlier block labelled "On your own".

## Days without a fight (peace milestones)

Couples should become proud of **not fighting**. This sits alongside the check-in milestones.

- **How a fight is counted:** a day counts as a fight if either partner ticks **We argued today** on the nightly check, or a Resolve session happens that day. Everything else is a fight-free day. The count restarts after a fight (last\_argument\_at).
- **Milestones:** 3, 7, 30 and 100 days without a fight. Same full-screen layout as the other milestones: the number, "DAYS WITHOUT A FIGHT.", a row of squares since the last argument, "A whole week of peace. That's not luck. You both did the work, every single night. Be proud of this one." (copy per milestone), a bar to the next one. **Keep the peace** · **Send \[Partner\] a well done**.
- **Home:** under the agreement card, one line: the number, "Days without a fight", and a short bar to the next milestone ("1 to go to 7"). Replaces the old good-days bar.
- **Calendar:** argument days get a small ink corner on their square (legend: ARGUMENT); the stats row shows Good · Bad · Fight-free.
- **Nightly check:** the second text link is now a small checkbox, **We argued today**. "Something crossed the line" moves inside the note sheet.

## Past arguments

From the Calendar tab, a **Past arguments** row ("2 so far · what you said and agreed") opens a list, newest first. Each card: date, time, together or apart, length, a short AI title, one calm line per person (initials), and **What you agreed** with its status (Day 6 of 7, Worked, Didn't work). The newest card is open, older ones collapsed. Read-only: no way to reopen or reply. Only the calm summaries are kept; voice recordings are deleted once the summary is made. Tapping an argument day in the calendar also shows its summary in the day sheet.

## Wording rules

Always **check** (never tap/rate/score) · **Tonight's check** · **Missed** (never "not tapped": missing is meant to sting) · **the 90-day test** (never "cycle") · the nightly button is **✓ Lock in Day \[n\]** and the after-screen says **Day \[n\] locked in.**

## Your own thing (everyone)

Every user has **two** ways to be accountable, so control never sits only in the partner's hands:

|  | **Main action** | **Your own thing** |
| --- | --- | --- |
| Who picks it | Your partner (blind) | You, from your argument type |
| Who checks it | Your partner, every night | You, every night |
| Who sees it | Both of you | Only you |
| On screen | The big card, the big Yes / No | One slim row under it, small Yes / No |
| Ends | Day 90 | When it's yours: 66 nights in total, or 10 yeses in a row → "This one's yours now" → pick a new one or stop |

**Why both:** the partner's pick covers what hurts *them*; your own thing covers what *you* bring into the fight (from your type). The main action stays the priority, your own thing never competes for space or attention. 66 nights comes from the best-known habit study (Lally et al., 2009: median 66 days to become automatic).

**Where it's picked:**

- Initiator: after 1G.1, one screen: "And your own thing? Something you'll check yourself. Only you see it." Top suggestion from their argument type (the Solo table) + 2 more · **Pick it** (required, no skip). **She starts checking it the first night after she pays, whether or not the partner has joined**, so she can set up and start right away while waiting for him.
- When the partner joins: he picks her main action freely and blind (P4), then picks his own thing (P4b). From that night each checks the other's main action, plus their own thing. Her own-thing nights carry over; nothing is reset. He never sees her own thing.

**Nightly tap (one screen, one Save):** the partner question first, big ("Did \[Partner\] keep to it today?" Yes / No). Under a thin rule, one slim row: "YOUR OWN THING · ONLY YOU SEE THIS" + the action + "Did you?" with small Yes / No pills. The button reads "✓ Lock in Day \[n\]" (never "Save" or "Submit"); on tap the day's square fills on the calendar, success haptic, then "Day \[n\] locked in." It is enabled once the main question is answered; the own-thing row is optional each night (unanswered = not counted, no penalty).

**Home:** the hero card is your main action (partner checks you). Inside the same card, a slim bottom row shows your own thing with its last 5 nights as small ticks. No extra cards.

**Rules:** your own thing never shows on the partner's phone, never feeds couple milestones, never affects the shared calendar colours. It has its own small milestone at the end ("This one's yours now").

## Solo route: your half

For someone whose partner hasn't joined, or won't. Same price (£9.99 / £49.99), same plan, same 90-day test. They work on **their own half of the cycle**: the behaviour their personality type tends to bring into arguments. Still a relationship app, not self-help. Every solo action is about how they act with their partner. The partner can join free on the same plan at any point, and the account switches to the couple version without losing anything.

### Rules

- **Never offered as an equal choice to the couple route.** Couples is the main product and solo must not eat into it.
- **Same binary rule as couples:** one fixed daily action that can be done every day, tapped yes or no each night. No levels, no "didn't come up".
- **Always relationship-scoped.** Actions name the partner: "Ask Mark instead of telling him", not "Be more patient".
- **Together is always one tap away.** Every solo screen that ends a flow (tap saved, milestones, solo Resolve) has a quiet **Invite \[Partner\]** link.

### Ways in (no one slips through)

| Trigger | What they see | Why |
| --- | --- | --- |
| Trial Day 3, partner not joined | Full-screen card on open + push at 19:00: "\[Partner\] hasn't joined yet." "You're \[n\] nights into your own thing. It works best when \[Partner\] is checking you too." Shows her own thing and nights done. **Nudge \[Partner\]** (sends the next invite message now) · **Copy invite link**. | Pushes the partner invite hard while she's already getting value from her own thing. |
| 1A.5 fork | Quiet text link under the options: "Doing this on your own?" → SO-Together → solo Stage 1 | For people who know their partner won't do it. Small, so it doesn't pull couples away. |
| Initiator taps "No, not really" at 4.0 | Exit sheet adds one line: "Not ready to do it together? Start with your half." | Catches the doubters before they leave. |
| Partner stops tapping for 7 nights in a row | Initiator: "\[Partner\]'s gone quiet. Keep going with your half?" The couple test pauses; their own action continues solo. | Stops a paying user losing value because of the partner. |

### Solo onboarding

Same Stage 1 (Parts A–E, Part C about the partner stays, because the problem is still between them). Differences:

- **SO-Report "Your side":** 9 cards instead of 13. The headline card names their argument type from Part B, e.g. **THE DIRECTOR**: "At your best: you fix things fast. Under pressure: you give orders instead of asking." Then how that lands on the partner, and the loop it creates.
- **"People like you" line:** one general tendency per type, e.g. "Directors are among the most likely to interrupt and give instructions in an argument." Always labelled **EARLY ESTIMATE · UPDATED AS COUPLES USE THE APP**. The wording comes from remote config so it can be made more accurate as data comes in, without an app update. Never a made-up percentage.
- **One thing:** picked from the solo action list (below), top suggestion from their type plus their 1D problem.
- **SO-Together (before the paywall):** "You can do this alone. It works best with \[Partner\]." Chart: **1×** On your own vs **2×** With \[Partner\], labelled "People noticing the effort, every night". That 2× is literally true: two people, two check-ins. Three lines: twice the check-ins · someone else notices your effort · \[Partner\] joins free on your plan. **Invite \[Partner\]** (primary) · **Start on my own for now**. Once real data exists, the chart's label and numbers (remote config) switch to measured results, e.g. good days solo vs together.
- Then 4.0, Stage 4 (commitment, solo wording), Stage 5, Stage 6 paywall, unchanged prices.

### Type → solo action (starter set, all daily and binary)

| Argument type (Part B) | Tends to | Solo action | Nightly question |
| --- | --- | --- | --- |
| Director (Out · Head · Planned) | Give orders, interrupt | Ask, don't tell: once a day turn an instruction into a question | "Today, did you ask \[Partner\] instead of telling them?" |
| Debater (Big picture · Head · Flexible) | Argue the point, need to be right | Once a day, say "you've got a point" and mean it | "Today, did you tell \[Partner\] they had a point?" |
| Keeper (In · Heart · Planned) | Bottle it up, then explode | Say one thing that bothered you, out loud, the same day | "Today, did you say what bothered you, the same day?" |
| Peacemaker (In · Heart · Flexible) | Go along to keep the peace | Once a day, say what you actually want | "Today, did you say what you actually wanted?" |
| Retreater (In · Head · Flexible) | Go silent, walk off | Once a day, check in first: "how was your day?" before your phone | "Today, did you check in with \[Partner\] before your phone?" |
| Firestarter (Out · Heart · Flexible) | Raise voice, say things in the heat | Once a day, say something appreciative out loud | "Today, did you say something appreciative to \[Partner\]?" |
| Fixer (Out · Facts · Flexible) | Jump to solutions, skip feelings | Once a day, ask "how did that feel?" before giving advice | "Today, did you ask how \[Partner\] felt before fixing it?" |
| Analyst (In · Facts · Planned) | Bring up the past, keep score | Once a day, let something go without comment | "Today, did you let something go without bringing it up?" |

### SO-Tap: the nightly self-check (sharper)

- The question names a specific act on a specific day: "Today, did you ask Mark instead of telling him?", never "Did you do well?"
- **Yes needs proof:** a one-line box, "What did you ask?", required to save a Yes (3–120 characters). Only they see it. Writing it down is what stops easy yeses.
- **No** saves with an optional note. Same white = good / black = bad calendar.
- **Sunday look-back:** "Looking back, how did your week really go?" shows the 7 days with their proof lines; they can flip any day. Flips are allowed and counted (honesty score kept internally, never shown).
- Line under the buttons: "Be honest. On your own, nobody checks but you."

### Solo Resolve: say it out loud first

The same "We're arguing right now" tile on Home. Solo version:

1. **Talk it out:** up to 2 minutes of recording. "Say what's upsetting you. Nobody hears this but you."
2. **Calm summary:** AI rewrites it neutrally: "Here's what you said, calmly."
3. **How to raise it with \[Partner\]:** 2–3 openers written for their type (Director: short, a question not an order, about you not them). Pick one or edit.
4. **Send it to \[Partner\]** (share sheet, with the invite link appended) · **Save it for later**. Every send is also an invite, so a solo Resolve can turn into a couple.

### When to stop waiting for the partner

We never close the door, we just stop *waiting*. The initiator is moved onto their half early (Day 3) so they get value, while the partner is nudged on a fading schedule.

| When | Initiator | Partner (invite drip, V1–V4) |
| --- | --- | --- |
| Day 0 | Invite sent | Sealed-note invite |
| Day 1–2 | Home: "Waiting for \[Partner\]" + Resend | V2 reminder ("Your note from \[Me\] is still sealed") |
| **Day 3** | **Switch to solo offer** (SO-Switch). Most should start their half here. | V3 |
| Day 5 | Trial reminder (as normal) | — |
| Day 7 | If still waiting, not solo: last nudge "Start your half, or your trial ends with nothing done." | V4 (last of the fast drip) |
| Day 7–30 | Solo. Weekly Home bar: "Invite \[Partner\] — free on your plan" | Once a week, **using her progress**: "\[Me\] is \[n\] nights into her half. Your note's still sealed." |
| Day 30 | Link expires. Initiator gets "Send \[Partner\] a fresh invite?" (one tap) | — |
| After Day 30 | Invite reappears only at milestones (45, 60, 75) and Day 90 ("Do the next 90 together") | Only if the initiator re-sends |

- **Stop nudging:** You → Settings has **Stop inviting \[Partner\]**. Ends all partner messages and the Home bar. The invite option stays in You for later.
- Partner messages never reveal the love note, the report or anything she's written. Only the count of nights she's done.

### Home while the partner is invited (your half + their spot)

The Today screen for a solo user whose invite is still open. One screen does both jobs:

- Header label "LOVETH · DAY \[n\] · YOUR HALF"; the partner's avatar is dashed and labelled INVITED.
- **Your half card:** the solo action, last 7 nights (white = yes, black = no, ink ring = tonight), "\[n\] OF \[n\] NIGHTS CHECKED".
- **\[Partner\]'s spot · kept open** (dashed card): invite status Sent → Seen → Joined, "Note still sealed", and "When \[Partner\] joins, you each check the other instead. Free on your plan, and your nights stay." Buttons: **Nudge \[Partner\]** (sends the next drip message now, max once a day) · **Copy invite link**.
- Tiles: **Tonight's check** (SO-Tap) · **We're arguing right now** (solo Resolve).
- When the partner joins, the spot card turns into "\[Partner\] joined. Pick together." and then Home switches to the couple layout. After **Stop inviting \[Partner\]**, the spot card collapses to a one-line "Invite \[Partner\] — free on your plan" bar.

### When the partner joins later

Solo progress is **never deleted**. Deleting it would punish the most committed users, and her nights are the best proof for the partner that she means it.

1. The partner joins through the sealed note as normal (P0b → P1 → his questions).
2. At P4 the partner picks her main action **freely and blind**, exactly like any partner. He is never shown her solo action, so he decides what he wants changed. Her solo action becomes **her own thing** (see Your own thing): same action, nights carried over, still checked by her, private to her.
3. Blind reveal as normal. A **new 90-day test starts that day for both**: the couple version, with each of them tapping for the other.
4. Her solo nights keep counting on her own thing. The couple milestones start from 0. Only after he has picked, the reveal can add: "\[Me\] also spent \[n\] nights working on her side before you joined."
5. Billing doesn't change: same plan, same renewal date, the partner is free on it.

### Milestones, Home, Day 90

Same check-in milestones (3, 7, 14, 30, 45, 60, 75) counting their own nights checked in. Home shows one action card instead of two, plus a slim **Invite \[Partner\] — free on your plan** bar under it. Day 90 offers: another 90 days of the same thing · a new action · **Do the next 90 together**.

### Analytics

solo\_offer\_shown (trigger), solo\_started (trigger), solo\_type, solo\_proof\_length, solo\_week\_flips, solo\_invite\_tapped, solo\_to\_couple (days into solo), solo\_trial\_to\_paid vs couple\_trial\_to\_paid.

## Free trial screens

- **Push permission (1A.0, before the first question):** bell icon · "Can we remind you?" · "We'll save your answers and remind you if life gets in the way." · three reasons: Your nightly check (one reminder at the time you pick) · Before you're ever charged (Day 5 of your trial, as promised) · When your partner joins (and when they leave you a note) · **Allow reminders** → system prompt · **Not now**. If declined, ask once more at 2.2 (after picking the check time). Push is the only channel before payment. After payment the Day-5 reminder also goes to the email shared at 6.1b.
- **Day 5 reminder push** (19:00): "2 days left of your free trial. Your plan starts \[date\]. Tap to see your first 5 days." Tapping opens the **trial reminder screen**: FREE TRIAL · DAY 5 OF 7 · big "2" · "DAYS LEFT OF YOUR FREE TRIAL." · 7-segment bar · card: YOUR PLAN STARTS \[date\] · \[price\] · "Nothing to do if you're staying. As promised, this is your reminder." · YOUR FIRST 5 DAYS: nights checked · good days · days no fight · **Keep going** → Home · **Manage or cancel subscription** → App Store / Google Play subscriptions page.
- **You tab, trial bar** (top, only during the trial): bell · FREE TRIAL · DAY \[n\] OF 7 · "\[n\] days left" · 7-segment bar · "\[Plan\] starts \[date\] · \[price\]. Manage or cancel any time." Tapping opens the trial reminder screen. Disappears once the plan starts.

## Subscription states

The couple record holds one sub\_state, and it decides what both people see. The server updates it from App Store Server Notifications and Google Play real-time developer notifications, never from the app alone.

| sub\_state | Meaning | Both have access? | Moves to |
| --- | --- | --- | --- |
| In onboarding | Initiator is in Stages 1–3 | No | Invited (invite sent at 3.2) · Trial active (bought with the invite put off, intimacy and hard week routes) |
| Invited | Invite sent, no purchase yet | No | Trial active (purchase) · Pulled back (leaves at Stage 4–6) |
| Pulled back | Initiator left before paying, or turned off renewal during the trial | Only until trial\_end, if a trial was started | Trial active (either person buys) · Lapsed (trial\_end passes, nobody pays) |
| Pending | Store payment awaiting approval | No | Trial active · Invited (declined) |
| Trial active | 7-day free trial running | Yes | Subscribed (Day 7 charge) · Pulled back (renewal turned off) · Trial extended |
| Trial extended | Partner hadn't joined by Day 7, so free time continues | Yes | Trial active / Subscribed once the partner joins (see rule 4) |
| Subscribed | Paying | Yes | Lapsed (cancelled, expired or billing failed after the store's grace period) |
| Lapsed | No active subscription | No (history kept) | Trial active / Subscribed (either person buys from 6.1) |

### Rules

1. **One subscription per couple.** Whoever buys becomes payer\_id. The other person has full access and sees *"Covered by \[Partner\]"*.
2. **Never pay twice.** While the couple is Trial active, Trial extended or Subscribed, the paywall (6.1) never shows to either person.
3. **Pulled back with a trial still running:** the partner's Home shows *"\[Partner\]'s trial ends on \[date\]. Want to keep this going?"* → P11.
4. **Partner not joined by Day 7:** on Day 6 the server checks partner\_id. Only applies if the invite was sent by Day 3 of the trial (someone who put it off is charged on Day 7 as normal). If empty, the couple moves to Trial extended and the payer isn't charged until 7 days after the partner joins. *Developer to confirm the store mechanism (App Store promotional offers, Google Play deferred billing).*
5. **A second trial is allowed.** If the initiator's trial is cancelled and the partner starts their own, that's fine.
6. **Pulled back or Lapsed:** every answer, pick and check-in stays saved. Buying again resumes the same goal, no questions repeated.
7. **One person deletes their data (You → Delete my data):** Loveth ends for both. The payer sees *"Remember to cancel in your phone's subscription settings."*

## Notifications

#### Daily limit (Oct 2026)

- At most 6 pushes per person per day. Never counted and never dropped: Resolve requests and the Day-5 trial reminder.
- Over the limit, the lowest priority waits for tomorrow or drops: 1 Resolve · 2 Day-5 reminder · 3 nightly check and its 2-hour reminder · 4 "\[Partner\] just checked in" · 5 Hard week support · 6 partner joined, picked or sealed a note · 7 milestones · 8 heads-up push · 9 onboarding drip.
- During a hard week the 17:30 heads-up isn't sent: the 18:00 support push does that job.

Every push opens the app on a specific screen. The Day-5 reminder is the one message that must never fail, so it also goes by email.

| Trigger | To | Message | Tap opens |
| --- | --- | --- | --- |
| Daily at checkin\_time (reminders on) | Each user | How did \[Partner\] do today? 10 seconds. | C1 |
| 2 hours before the window closes, not answered | Each user | Don't break the chain. How did \[Partner\] do today? | C1 |
| Other person submitted first | The one who hasn't | \[Partner\] just checked in. Your turn. | C1 |
| Partner joins | Initiator | \[Partner\] has joined. | Home |
| Partner sends nice words (P2) | Initiator | \[Partner\] said something nice about you. | Home (words shown on a card) |
| Partner picks (P4) | Initiator | \[Partner\] has picked. See what \[Partner\] picked for you. | Reveal (P5) |
| Partner not joined after 24h | Initiator | \[Partner\] hasn't joined yet. Send the invite again? | Home → Resend invite |
| Partner not joined after 72h | Initiator | Your trial's ticking. \[Partner\] still needs to join. | Home → Resend invite |
| Nudge tapped | Partner | \[Partner\] is waiting for you to pick. | P4 |
| Initiator pays while partner on P10 | Partner | You're both in. First check-in tonight. | Home |
| Pulled back | Partner (if joined) | \[Partner\]'s waiting to start with you. | P11 |
| Partner pays (takeover) | Initiator | \[Partner\]'s covered it. You're both in. | Home |
| Day 5 of trial | Payer, push **and email** | Your trial ends in 2 days. You'll be charged \[price\] on \[date\]. Cancel anytime in your phone's subscription settings. | Home |
| Day 7 charged | Payer | You're officially breaking the cycle together. | Home |
| Day 7 and Day 30 of the goal | Both | \[n\] days in. Keep going. | H2 |
| Day 90 | Both | 90 days. Come and see what you've done. | G1 |
| Left Loveth | The other person | \[Partner\] has paused Loveth. | Home |

No notification ever includes questionnaire answers, the safety answer or check-in answers in its text.

### Onboarding drop-off drip

Two aims only: **finish onboarding** and **get the partner on board**. Until both are done, the user gets two pushes a day. This product isn't for everyone: no discounts, no begging, no softening. If they leave, they leave.

**Rules**

- **Two a day:** 12:30 and 20:30, user's local time. The first one goes 2 hours after they drop off (if that's before 20:30).
- **Stops the moment the stage is done** and switches to the next stage's set. Stops entirely once the user has paid and the partner has joined.
- **No repeats** until a stage's set is used up, then it loops from the top.
- **Permission is asked at 1A.0**, so even people who drop out mid-questions can be reached. If push is off, nothing is sent before payment (there is no email yet). After payment, the same copy goes by **email, once a day** (title = subject line).
- **Personalised:** \[Partner\], \[dynamic\], \[x\] questions left, \[frequency\] and \[n\] arguments a month all come from their saved answers. A message whose data is missing is skipped.
- **Arguments a month,** from frequency: every day = 30 · a few times a week = 12 · about once a week = 4 · less than once a week = 2.
- **Tap opens** exactly where they left off.

#### Stage 1 — Dropped during the questions (aim: finish)

| # | Title | Body |
| --- | --- | --- |
| Q1 | Have you given up on you and \[Partner\]? | Your answers are saved. \[x\] minutes to go. |
| Q2 | Answering the questions is the easy part. | You're \[x\]% of the way to finding what keeps starting your fights. |
| Q3 | You said you argue \[frequency\]. | That's about \[n\] arguments a month. 3 minutes could change that. |
| Q4 | The grass is greener where you water it. | Finish your questions tonight. |
| Q5 | Same fight, different day? | You're \[x\] questions from finding out why. |
| Q6 | What's the argument you're tired of having? | We're close to naming it. Your answers are waiting. |
| Q7 | You started this for a reason. | Remember what it was. Pick up where you left off. |

#### Stage 2 — Saw the report, didn't continue (aim: feeling seen → act)

| # | Title | Body |
| --- | --- | --- |
| R1 | You two are \[dynamic\]. | We found what keeps starting your fights. Now see how to break it. |
| R2 | You made the right move. Now follow through. | \[Partner\]'s daily action is ready. |
| R3 | Knowing the pattern doesn't break it. | One small thing every day does. Yours is waiting. |
| R4 | \[dynamic\] doesn't fix itself. | Two minutes to set up your daily action. |

#### Stage 3 — Invite not sent (aim: get the partner on board)

| # | Title | Body |
| --- | --- | --- |
| I1 | \[Partner\] doesn't know yet. | One message changes that. We've written most of it for you. |
| I2 | Tell \[Partner\] one thing you love about them. | We'll turn it into an invite they'll want to open. |
| I3 | This only works with two. | Send \[Partner\] your invite tonight. |
| I4 | The hardest part is pressing send. | \[Partner\] might surprise you. |
| I5 | Picture tonight without the same argument. | It starts with \[Partner\] saying yes. |

#### Stage 4 — Invite sent, paywall not done (aim: start the trial)

| # | Title | Body |
| --- | --- | --- |
| P1 | \[Partner\] got your invite. | Don't leave them waiting. Start your 7 free days. |
| P2 | Would you rather keep £1 a week, or be happier with \[Partner\]? | 7 days free. Cancel any time. |
| P3 | Your plan is built. | Your daily actions are set. All that's left is Day 1. |
| P4 | Seven days. If it's not working, walk away. | If it is, you'll know by \[day name\]. |
| P5 | No surprises. | We remind you on Day 5, two days before you pay. |

#### Stage 5 — Paid, partner hasn't joined (to the initiator)

| # | Title | Body |
| --- | --- | --- |
| J1 | \[Partner\] hasn't opened your invite yet. | Want to send a softer version? We've written one. |
| J2 | Your Day 1 is waiting for \[Partner\]. | Resend your invite in one tap. |
| J3 | Some people need asking twice. | Here's a new message for \[Partner\]. |

Each J push opens the share sheet with the **next invite version** below (V2, then V3, then V4, then back to V1). The user can edit before sending.

#### Invite versions (CoupleIn's kind-invite format: something nice about the partner, plus a hint at fixing things)

| # | Tone | Message the user sends |
| --- | --- | --- |
| V1 | Original (3.2) | \[Me\] knows you both want this to work. Here's something nice \[Me\] said about you: "\[nice words\]". \[Me\] has found the pattern behind your arguments. Want to see if \[Me\] got you right? You'll pick one thing for \[Me\] too. \[link\] |
| V2 | Soft | I love \[nice words\]. I found something that might stop us going round in circles. Two minutes, then you pick one thing for me too. \[link\] |
| V3 | Curious | I did something about us and it says we're \[dynamic\]. Is it right? Your turn: \[link\] |
| V4 | Direct | You're not in trouble. I just want fewer arguments and more of us. Will you do this with me? \[link\] |

#### Stage 6 — Partner installed but didn't finish (to the partner)

| # | Title | Body |
| --- | --- | --- |
| M1 | \[Me\] said: "\[nice words\]" | Your turn. Two minutes. |
| M2 | \[Me\] has picked one thing for you. | Pick theirs, then you'll both see. |
| M3 | \[Me\] thinks they know your style. | Find out if they got you right. |
| M4 | \[Me\] is waiting to start with you. | Day 1 begins when you join. |

## Edge cases

| Situation | What happens |
| --- | --- |
| Both partners start their own Loveth and invite each other | Opening the other's invite asks *"Join \[Partner\]'s instead?"* **Join** → partner flow, own in-progress answers discarded · **Keep mine** → closes, invite stays unused |
| Invited person is already in Loveth with someone else | *"You're already doing Loveth with someone else."* Cannot join |
| Partner's name typed wrong at 1A.1 | Replaced by the partner's own account first name once they join |
| Partner answers Sometimes / Yes at P3 | Partner sees 1E.6S. Initiator's Home stays on *"\[Partner\] is picking one thing for you."* Nudges to that partner are silently not sent. Nothing reveals why |
| Partners in different time zones | Each person's check-in window uses their own time zone |
| Check-in time changed while today's window is open | New time applies from tomorrow |
| App deleted and reinstalled | After payment: Sign in with Apple or Google (6.1b, or Restore purchase) and everything comes back. Before payment: starts fresh, because nothing is paid for or saved to an account yet |
| Notifications off | Home banner; Day-5 reminder still sent by email |
| User hides their email at Sign in with Apple | A*pple's relay address still delivers, so the Day-5 email goes there. Nobody is ever asked for an email before payment.* |
| Account deleted | That user's Loveth data deleted; couple ends; other person told *"\[Partner\] has paused Loveth."* |
| Refund requests | Handled by the App Store / Google Play |

## Analytics events

Fire these so the funnel can be measured end to end. Exclude CoupleIn test accounts. Never log the safety question, its answer or 1E.6S views.

| Event | Properties |
| --- | --- |
| btc\_started | role |
| btc\_question\_answered | screen (any Stage 1 screen ID, P3b, P4), answer\_id |
| btc\_result\_viewed | cycle\_type |
| btc\_time\_set | hour |
| btc\_invite\_sent | method (share, copy, in\_app) |
| btc\_commit\_answered | screen (4.1–4.4), answer\_id |
| btc\_promise\_choice | sounds\_good / rather\_argue / left |
| btc\_paywall\_viewed | role, trial\_eligible |
| btc\_trial\_started | plan, role (initiator / partner takeover) |
| btc\_pulled\_back | screen |
| btc\_partner\_joined | hours\_since\_invite |
| btc\_partner\_picked | — |
| btc\_checkin\_submitted | answer, crossed\_line, day\_number |
| btc\_checkin\_missed | day\_number |
| btc\_day5\_reminder\_sent | channel (push, email) |
| btc\_converted | plan |
| btc\_lapsed | days\_subscribed |

## Open questions

- [ ] Store mechanism for Trial extended (App Store promotional offers, Google Play deferred billing). Developer to confirm.
- [ ] Deferred deep link tool for partners installing from the invite. Developer to pick.
- [ ] ~~Paywall headline~~ Decided: **"Would you rather keep £1 a week, or be happier with \[Partner\]?"** Under the button, in bold with a bell icon: "We'll remind you on \[Day 5 date\], 2 days before you pay." The Day 5 reminder must actually be sent.
