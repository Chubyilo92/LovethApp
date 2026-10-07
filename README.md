# Loveth — Stop having the same fight

Loveth is a standalone iOS and Android app for couples who argue a lot. It is separate from CoupleIn and only reuses CoupleIn's partner-invite idea. It has **one job: stop couples fighting**.

This repo holds everything needed to build it:

| File | What it is |
|---|---|
| [build-spec.md](docs/build-spec.md) | The full build spec, exported from the live doc on 7 Oct 2026. This is the source of truth for the build. |
| [screens/nightly-check-flow.png](docs/screens/nightly-check-flow.png) | The approved Today screen and nightly check, in four steps: daytime → 21:30 reminder → Today at 21:30 → the check |
| [screens/today-normal-vs-hard-week.png](docs/screens/today-normal-vs-hard-week.png) | Today on a normal day vs. with Hard week switched on |

Live, editable version of the spec: https://claude.ai/code/artifact/593f3f01-2770-4491-b38e-2bf9b8ba9333 (if the two ever differ, the live doc wins; re-export it here).


## How the app works, in one minute

1. **Why are you here?** The first screen picks one of three routes: *Break the cycle of fighting*, *Improve intimacy*, or *The hard week* (PMS or PMDD).
2. **Are you serious?** Every route has more than 15 questions, so the app says how many, and asks "I'm serious / I'm just curious". Curious people get a quiet "We'll see you when you're ready". Serious people answer the route's questions (about 36–42).
3. **The report.** The app names their pattern and the exact behaviour behind the fights.
4. **One daily action each.** Each partner picks one fixed Do or Don't for the other, blind. It stays the same for the 90-day test.
5. **The nightly check.** Every night each partner taps whether the other kept to it. Good day / bad day / missed. That is the whole mechanism.
6. **Help in the moment.** "We're arguing right now" opens Resolve, a guided turn-taking talk with AI summaries.

## Key decisions (Oct 2026)

**Accounts and payment**
- No sign-in, email or requests of any kind before payment. The app uses an anonymous account on the device.
- A real account is created in one tap (Sign in with Apple or Google, both offered on both platforms) right after payment: screen **6.1b**. The partner gets the same one-tap card once the couple has paid.
- The Day-5 trial reminder goes by push and to the email Apple/Google shares at sign-in.
- Payments: RevenueCat (App Store + Google Play). Prices £9.99/month, £49.99/year, 7-day free trial.

**Routes**
- *Intimacy:* works for whoever wants more, less, or "we've both drifted". No action ever obliges sex. "Kiss me for 30 seconds every day" is always in the top three suggestions. A private pressure question with a support screen.
- *The hard week:* names PMS/PMDD on the first screen, health-data consent, separate answer lists for who has the hard weeks. PMDD gets its own report line, longer support and a permanent support row.
- *Hard week switch:* each person has their own switch. Whoever turns it on, support starts for both. Nobody is ever told who pressed it. Each person then gets 3 pushes a day (08:00, 13:00, 18:00), 21 different lines over 7 days, all using the other person's name, all lock-screen safe (never mention a period, PMS or PMDD).
- On the intimacy and hard week routes the initiator can pay first and send the invite later.

**The Today screen (approved layout)**
- Daytime: "Hi, [Me]", then **Day [n] of 90** with a reward line and a 90-segment progress bar, then the hero card: *"[Partner] asked you:"* and their words quoted in the serif. Then *We're arguing right now*, the Hard week row (collapsed when off), and *"Tonight at 21:30 · You asked [Partner]:"* with a bell hint.
- At check-in time it's the **same screen**: only the top card changes into *Tonight's check* with Yes / No right on the card. The app tells them with a push, a "1" badge on the app icon, and a dot on the Today tab.
- The check: the quote, "Did [Partner] keep to it today?", Yes / No, their own private thing, *We argued today*, an optional note, and **✓ Lock in Day [n]**.

**Rules that keep it calm**
- One full-screen moment a night (milestones queue up; encouragement after a bad day always comes first).
- At most 6 pushes per person per day (Resolve requests and the Day-5 reminder are never blocked).
- One calendar design; the orange accent only ever means "crossed the line".
- Nobody sees a head-to-head count of the other's days.

## Path check

Every answer on every route was traced by script to a valid daily action (binary, checkable every day, visible to the person checking, fixed for 90 days): 97 paths on the fighting route (7 problems found and fixed), 29 on intimacy, 16 on the hard week, 15 own-thing suggestions. Details are in the *Path check* section of the spec.

## Before launch

- Legal sign-off on health-data consent wording and outcome claims.
- Verify helpline numbers (Rape Crisis, National Domestic Abuse Helpline, Samaritans, Men's Advice Line, Galop).
- Confirm the store mechanism for *Trial extended* (App Store promotional offers / Google Play deferred billing).
- Pick the deferred deep link tool for partner installs.
