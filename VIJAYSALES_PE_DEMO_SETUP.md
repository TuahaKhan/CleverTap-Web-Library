# Vijay Sales — CleverTap Product Experience (PE) Demo

This guide explains the **4 Product Experience (Remote Config Variables)** use cases built
into `vijaysales.html`, the **dashboard setup** required for each, the **manual changes**
already made in code, and a **stage-ready demo script**.

> **Why Product Experience (Variables) for these — and not Web Pop-ups / Native Display / Visual Editor?**
> PE Variables let the **website's own rendering logic** consume server-controlled values.
> These 4 use cases all change *structure/behaviour* (re-ordering the nav & category rail,
> re-skinning the whole site via one accent token, switching localized copy keyed to a geo
> segment, gating layout on loyalty tier). Pop-ups/Native Display can only *overlay* content,
> and the Visual Editor only does static one-off element tweaks — none of them can re-rank a
> category list or theme the site from a single segment-targeted value without a code deploy.
> That's exactly the gap PE fills, so the demo stays honest about where PE is the right tool.

---

## 0. Prerequisites

| Item | Value |
|---|---|
| Web SDK version | **1.7.0 or higher** (Remote Config requires this) |
| Account ID (in code) | `WW6-988-RW7Z` — change in `vijaysales.html` `<head>` if you use a different demo account |
| Test profile | Mark your own profile as a **Test Profile** in the dashboard (needed to sync & preview variables) |
| `useIP` | Set to **`true`** in code (already done) so CleverTap derives **City** from IP for UC4 geo-segments |

---

## 1. Register the 4 variables on the dashboard

The variables are already **defined in code** (`vijaysales.html` `<head>`, in the
`clevertap.variables.push({...})` block). You now need them to exist on the dashboard so you
can override their values per segment.

**Option A — Sync from the SDK (recommended, one-time):** temporarily add this in the browser
console (or a throwaway script) while logged in as your **test profile**, in DEBUG mode:

```js
clevertap.syncVariables(
  () => console.log('Sync successful — check Product Experiences > Variables'),
  () => console.log('Sync failed — publish/dismiss any existing draft first')
);
```

**Option B — Create them manually** under **Product Experiences → Variables → Create**, using
the exact names, types and defaults below.

| # | Variable name | Type | Default value (JSON) |
|---|---|---|---|
| UC1 | `vs_category_priority` | JSON (string) | `{"boostedCategory":"","headline":"Recommended for You"}` |
| UC2 | `vs_festival_theme` | JSON (string) | `{"active":false,"name":"Diwali Dhamaka","ribbonText":"🪔 Diwali Dhamaka Sale — Up to 60% OFF + No Cost EMI","accentColor":"#d35400","headerBg":"#2a0a3a","countdownText":"Ends in 2 days"}` |
| UC3 | `vs_loyalty_config` | JSON (string) | `{"tier":"Guest","greeting":"Sign in for member prices, faster checkout & order tracking","accentColor":"#c0392b","perks":["Member-only prices","Faster checkout"],"showPerksStrip":false}` |
| UC4 | `vs_city_config` | JSON (string) | `{"city":"Mumbai","language":"Marathi","greeting":"नमस्कार मुंबई! 🙏","subText":"मुंबईत जलद डिलिव्हरी आणि जवळचे स्टोअर","storeCallout":"Nearest store: Vijay Sales, Andheri West — 2.3 km","show":true}` |

> **Note on value type:** the demo stores each config as a **JSON string** and parses it
> client-side (the convention already used in `sample_pe_demo.html`). If you prefer, CleverTap
> also supports native string/number/boolean variables — but JSON keeps each use case in one
> editable value, which is easier to manage from the dashboard.

---

## 2. Use-case-by-use-case dashboard setup

For **every** use case the pattern is the same:
**(a)** an event/property makes the user fall into a **Segment** → **(b)** a **Product Experience
campaign** overrides the variable's value **for that segment** → **(c)** the SDK fetches the
value (on load, or after `fetchVariables()`), and the page re-renders.

### UC1 — Category Affinity Re-ranking
*Goal: a user who keeps browsing ACs sees ACs surfaced (nav, category rail, "For You" hero) on their next visit.*

- **Event captured by the page:** `Category Viewed` with property `Category` (fired from the top
  nav and the "Shop by Category" rail — see `wireAffinityEvents()` in code).
- **Segment to create:** *"Users who raised `Category Viewed` with `Category = Air Conditioners`
  at least 2 times in the last 7 days"* (repeat for `TV & Entertainment`, `Microwave`).
- **PE campaign:** override `vs_category_priority` → set
  `{"boostedCategory":"Air Conditioners","headline":"Recommended for You"}` for the AC segment
  (and the matching value for the TV / Microwave segments).
- **Result:** on next load the page reads the value, **moves the matching nav link & category
  tile to the front + highlights them**, and shows a personalized **"Recommended for you" hero**.
- Accepted `boostedCategory` values (mapped in code's `CATEGORY_META`): `Air Conditioners`,
  `TV & Entertainment`, `Microwave`.

### UC2 — Festival / Sale Theme Switch
*Goal: marketing flips the whole site into a sale skin, instantly, with no developer/deploy.*

- **Segment:** usually **All Users** (or a segment, e.g. only "high-value" users see the sale early).
- **PE campaign:** override `vs_festival_theme` → set `active: true` and edit `ribbonText`,
  `accentColor`, `countdownText` to taste. Setting `active:false` (or ending the campaign) reverts.
- **Result:** a top **sale ribbon** appears and the site **accent colour** (`--vs-accent`,
  applied to "Add to Cart" buttons, discount badges, the Loyalty Hub link, etc.) re-skins live.
- No events needed — this is a pure marketing-controlled toggle.

### UC3 — Login + Loyalty-Tier Personalization
*Goal: guests get a sign-in nudge; members get tier-specific greeting, accent and perks.*

- **Profile property:** `Loyalty Tier` (`Silver` / `Gold` / `Platinum`) — set at login via
  `onUserLogin` (the code pushes it; in production it comes from your auth/CRM).
- **Segments:** one per tier on the `Loyalty Tier` property.
- **PE campaigns:** override `vs_loyalty_config` per tier segment, e.g. for Gold:
  `{"tier":"Gold","greeting":"Welcome back, Gold member 👑","accentColor":"#b8860b","perks":["Free installation","Priority delivery","Extended warranty","Exclusive Gold prices"],"showPerksStrip":true}`.
- **Important (Web):** because login changes the profile/segment, the page calls
  **`clevertap.fetchVariables()` right after `onUserLogin`** so the tier value applies in-session
  (already wired in `simulateLogin()`). Guests keep the default (sign-in nudge).

### UC4 — City / Language Localization
*Goal: Mumbai sees Marathi, Delhi sees Hindi, Bengaluru sees Kannada + nearest-store callout.*

- **Property:** `City` — auto-derived by CleverTap from IP (because `useIP:true`), or set explicitly.
- **Segments:** one per city on the `City` property.
- **PE campaigns:** override `vs_city_config` per city segment with localized
  `greeting` / `subText` / `storeCallout`, e.g. Delhi:
  `{"city":"Delhi","language":"Hindi","greeting":"नमस्ते दिल्ली! 🙏","subText":"दिल्ली में तेज़ डिलीवरी और नज़दीकी स्टोर","storeCallout":"Nearest store: Vijay Sales, Nehru Place — 1.8 km","show":true}`.
- **Result:** a localized greeting strip + store callout under the header; the header city label updates too.

---

## 3. Manual changes already made in `vijaysales.html`

Everything below is **done** — listed so you know what changed and what to revisit for production:

1. **`variables: []`** added to the `clevertap` queue object (required to define variables pre-load).
2. **`useIP` changed `false → true`** to enable City geo-segments for UC4.
3. **4 `clevertap.variables.push({...})`** definitions added (the variables table above).
4. Hardcoded brand red `#c0392b` replaced with the **`--vs-accent`** CSS variable so UC2 can re-skin.
5. New HTML containers added: festival ribbon, city strip, loyalty strip, "Recommended" hero.
6. A single **`VS_PE` engine `<script>`** that fetches the variables and applies all 4 use cases,
   plus a **floating "Demo Controls" panel**.

**The only thing you may want to change manually:** the **account ID** in the `<head>` if you
demo on a different account, and (optionally) the `CATEGORY_META` image URLs / copy in the script.

---

## 4. Demo script (how to present on stage)

The floating **"CleverTap PE — Demo Controls"** panel (bottom-left) lets you force each state
instantly so the demo never depends on live network/segment timing:

1. **Open with localization** — point out the **Marathi** greeting (Mumbai). Click **Delhi** →
   it flips to **Hindi** + Nehru Place store. *"This copy is one variable, targeted per city
   segment — zero code change."*
2. **Festival** — click **Diwali ON** → ribbon drops in and the **whole site recolors**.
   *"Marketing flips this the morning of the sale; no deploy, no dev ticket."* Click **OFF** to revert.
3. **Loyalty** — start as guest (sign-in nudge), click **Gold** → member greeting + perks; click
   **Platinum** → richer perks. *"The page re-fetches PE right after login, so the tier
   experience applies in the same session."*
4. **Category affinity** — click **AC** → AC jumps to the front of the nav + category rail and a
   personalized hero appears. *"After a few AC views, CleverTap segments the user and a PE
   campaign boosts that category on their next visit."* Click **TV** to show it generalizes.
5. **Reset demo** clears the forced states.

> The page **also** reads real values from `clevertap.getVariables()`, so once your dashboard
> campaigns are live you can demo the genuine end-to-end flow too. The demo panel just guarantees
> a clean stage experience.

---

## 5. Going to production

When this graduates from a demo, remove the presenter aid so the UI is driven **purely** by PE:

- Delete the **DEMO-CONTROL layer** in the `VS_PE` script: the `SIM` map, `demoState()`/`setDemo()`
  reads inside the `*Cfg()` resolvers, and the `buildDemoPanel()` call.
- The appliers (`applyFestival`, `applyCity`, `applyLoyalty`, `applyCategory`) then run only on
  values returned by `clevertap.getVariables()` + their in-code defaults.
- Keep the `Category Viewed` / `onUserLogin` event wiring — that's what feeds your segments.
