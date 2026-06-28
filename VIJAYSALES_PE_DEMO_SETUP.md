# Vijay Sales — CleverTap Product Experience (PE) Demo

This guide explains the **4 Product Experience (Remote Config Variables)** use cases built into
`vijaysales.html`, the **dashboard setup** for each, the **manual changes** already made in code,
and a **stage-ready demo script**.

> **API facts below are verified against CleverTap Web SDK v2.7.2 source** (the build served by
> the CloudFront CDN this page loads). The earlier object-variable approach was scrapped because
> object variables reject nested arrays; we now use **flat primitive variables (string/boolean)**,
> which are simpler to create on the dashboard and bulletproof.

> **Why Product Experience and not Web Pop-ups / Native Display / Visual Editor?** These 4 use
> cases change the page's *structure/behaviour* (re-ranking the nav & category rail, re-skinning
> via one accent token, swapping localized copy per geo-segment, gating layout on loyalty tier) —
> things overlays and one-off visual edits can't do. That's where PE Variables are the right tool.

---

## 0. Prerequisites

| Item | Value |
|---|---|
| Web SDK version | **v1.7.0+** (the CDN serves the latest, currently **v2.7.2** — fully supported). Confirm with `clevertap.getSDKVersion()`. |
| Account ID (in code) | `449-RRZ-7W7Z` — in `vijaysales.html` `<head>` `clevertap.account.push({id})` |
| **Region** | **REQUIRED** — routes requests to the right data centre. Set `region` (top-level) in the init: one of `in1 / sg1 / us1 / aps3 / mec1 / eu1`. |
| **Account Token (Passcode)** | Required for **`syncVariables()` only** (the one-time dashboard registration). Find at **Dashboard → Settings → Passcode**. Set `token` (top-level) in the init. *Not* needed for runtime `fetchVariables()`/`getVariables()`. |
| Test profile | Mark your profile as a **Test Profile** (needed only to sync/preview). |
| `useIP` | Set to `true` in code (done) so CleverTap derives **City** from IP for UC4 geo-segments. |

> The Account Token (Passcode) is only checked inside `syncVariables` — **anonymous/logged-out
> visitors receive segment-targeted values with just the account ID + region** (CleverTap targets
> them via their anonymous `GCOOKIE`). So production visitors do not need the token.

---

## 1. Create the 11 variables on the dashboard

Variables are registered in code via `clevertap.defineVariable(name, default)` inside `wzrk.onload`
(the pre-load `clevertap.variables.push()` queue is **not** processed for variables). To make them
appear on the dashboard so you can override them, **sync once** (Section 1a), or create them
manually with these exact names/types/defaults:

| # | Variable name | Type | Default |
|---|---|---|---|
| UC1 | `vs_boosted_category` | String | *(empty)* — values: `Air Conditioners` / `TV & Entertainment` / `Microwave` |
| UC2 | `vs_festival_active` | Boolean | `false` |
| UC2 | `vs_festival_ribbon_text` | String | `🪔 Diwali Dhamaka Sale — Up to 60% OFF + No Cost EMI` |
| UC2 | `vs_festival_accent_color` | String | `#d35400` |
| UC3 | `vs_loyalty_tier_label` | String | *(empty)* — e.g. `Gold` |
| UC3 | `vs_loyalty_greeting` | String | *(empty)* — e.g. `Welcome back, Gold member 👑` |
| UC3 | `vs_loyalty_perks` | String | *(empty)* — comma-separated, e.g. `Free installation,Priority delivery,Extended warranty` |
| UC3 | `vs_loyalty_accent_color` | String | `#b8860b` |
| UC4 | `vs_city_greeting` | String | `नमस्कार मुंबई! 🙏` |
| UC4 | `vs_city_subtext` | String | `मुंबईत जलद डिलिव्हरी आणि जवळचे स्टोअर` |
| UC4 | `vs_city_store_callout` | String | `Nearest store: Vijay Sales, Andheri West — 2.3 km` |

> **Value types:** only flat **String / Boolean / Number**. Lists (loyalty perks) are a
> comma-separated **string** that the page splits in JS — this avoids the SDK's nested-array
> restriction on object variables.

### 1a. Sync the definitions to the dashboard (one-time)

Set `region` + `token` in the `<head>`, mark your profile as **Test**, then open the page as that
profile with the built-in sync flag:

```
vijaysales.html?ctsync=1
```

The page runs `clevertap.setLogLevel(4)` (DEBUG) + `clevertap.syncVariables()` and logs the result.
You should see `[VS_PE] Defined variables: [...]` then `[VS_PE] ✅ Synced…`. Refresh
**Dashboard → Product Experiences → Variables** — all 11 appear. Remove `?ctsync=1` afterwards.

**If sync fails**, check (all must be true): SDK v1.7.0+, **token + region set**, **profile marked
Test** (else 401 "not a test profile"), and **no existing draft** (else 400 — discard it under
Product Experiences → Variables → Discard Draft). You only re-sync when you add/rename a variable.

---

## 2. Per-use-case: segments + Product Experiences

For each use case: **(a)** an event/property puts the user in a **Segment** → **(b)** a
**Product Experience** sets the variable value(s) for that segment → **(c)** the SDK fetches the
value (auto on first page view of a session, or via `fetchVariables()`) and the page re-renders.

**Dashboard flow to override a value:** Product Experiences → Variables → **+ Create Experience** →
pick the variable → set Control (default) + Variant value → **add a segment** → **Publish**.

### UC1 — Category Affinity Re-ranking
*A user who keeps browsing ACs sees ACs surfaced (nav, category rail, "For You" hero) next visit.*
- **Event the page fires:** `Category Viewed` with property `Category` (from nav + category-rail clicks).
- **Segments:** e.g. *did `Category Viewed` where `Category = Air Conditioners` ≥1× in 7 days* (repeat for `TV & Entertainment`, `Microwave`).
- **Experience:** set **`vs_boosted_category`** = `Air Conditioners` (resp. `TV & Entertainment` / `Microwave`) for each segment.

### UC2 — Festival / Sale Theme Switch
*Marketing flips the whole site into a sale skin, instantly, no deploy.*
- **Segment:** All Users (or a VIP segment for early access).
- **Experience:** set **`vs_festival_active`** = `true`, **`vs_festival_ribbon_text`**, **`vs_festival_accent_color`**. Setting active back to `false` (or ending it) reverts.

### UC3 — Login + Loyalty-Tier Personalization
*Guests get a sign-in nudge; members get tier-specific greeting, accent, perks.*
- **Profile property:** `Loyalty Tier` (Silver/Gold/Platinum), set at login (the page pushes it via `onUserLogin`).
- **Segments:** one per tier on `Loyalty Tier`.
- **Experience per tier:** set **`vs_loyalty_tier_label`**, **`vs_loyalty_greeting`**, **`vs_loyalty_perks`** (comma-separated), **`vs_loyalty_accent_color`**.
- The page calls `fetchVariables()` right after login so the tier values apply in-session. Guests (no values) see the default nudge.

### UC4 — City / Language Localization
*Mumbai → Marathi, Delhi → Hindi, Bengaluru → Kannada + nearest-store callout.*
- **Property:** `City` (auto from IP, since `useIP:true`).
- **Segments:** one per city.
- **Experience per city:** set **`vs_city_greeting`**, **`vs_city_subtext`**, **`vs_city_store_callout`**.

---

## 3. What changed in `vijaysales.html` (already done)

1. **`region` + `token`** added as top-level properties on the `clevertap` object.
2. **`useIP` `false → true`** for UC4 City geo-segments.
3. **11 flat variables** registered via `clevertap.defineVariable(name, value)` in `wzrk.onload`, from the `window.VS_PE_VARS` map (String/Boolean only — no nested arrays).
4. Hardcoded brand red `#c0392b` replaced with the **`--vs-accent`** CSS variable so UC2 can re-skin.
5. New HTML: festival ribbon, city strip, loyalty strip, "Recommended" hero.
6. A **`VS_PE` engine `<script>`** that reads values with the **synchronous** `clevertap.getVariables()`, applies all 4 use cases, re-applies on `addVariablesChangedCallback`, and renders a **Demo Controls** panel.

**You must fill in** the real **`region`** + **`token`** in the `<head>` before syncing. Optionally
change the account ID or the `CATEGORY_META` image URLs/copy.

---

## 4. How values resolve at runtime (so the two screens line up)

Precedence in code: **demo-control override (localStorage) → live PE value (`getVariables()`) → `<head>` default.**

- The **Demo Controls** panel (bottom-left) forces states for a reliable stage demo.
- To show the **real dashboard value** driving the site, click **Reset demo** first (clears the
  local override), reload, and watch the console log `[VS_PE] Live PE variables: {...}`.
- Easiest to show genuinely live end-to-end: **UC2 (festival)** and **UC4 (city)** — no login needed.

## 5. Demo script (stage)

1. **Localization** — show Marathi (Mumbai); click **Delhi** → Hindi + Nehru Place store.
2. **Festival** — **Diwali ON** → ribbon + whole-site recolor; **OFF** reverts.
3. **Loyalty** — guest nudge → **Gold** → member greeting + perks → **Platinum**.
4. **Category affinity** — **AC** → AC jumps to front of nav + rail + a "For You" hero; **TV** to generalize.
5. **Reset demo** clears forced states.

## 6. Production cleanup

Remove the presenter aid so the UI runs purely on PE: delete the **DEMO-CONTROL layer** in the
`VS_PE` script (the `SIM` map, the `demoState()` reads in the `*Cfg()` resolvers, and the
`buildDemoPanel()` call). Keep the `Category Viewed` / `onUserLogin` event wiring — that feeds your segments.
