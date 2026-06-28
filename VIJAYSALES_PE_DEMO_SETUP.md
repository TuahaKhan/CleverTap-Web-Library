# Vijay Sales — CleverTap Product Experience (PE) Demo

**Model: user-property driven.** The website pushes a **user property** on each trigger; on the
dashboard you write **if/else on that property** and set a PE **variable = a small JSON object**
holding the content (text / subtitle / image / colour). The site fetches the variable and renders
those fields. **All content lives on the dashboard — nothing is hardcoded in the page.**

Scope now: **UC1 Category**, **UC3 Loyalty**, **UC4 City**. Festival is deferred until these work.

> API verified against CleverTap Web SDK **v2.7.2** (the CDN build this page loads).

---

## 1. The 3 variables and their user properties

| Use case | Variable (object) | User property the page pushes | Object fields |
|---|---|---|---|
| UC1 | `vs_reco` | `Last Category Clicked` | `category`, `mainText`, `subText`, `image` |
| UC3 | `vs_loyalty` | `Loyalty Tier` | `tierLabel`, `greeting`, `perks` (comma-separated), `accentColor` |
| UC4 | `vs_city` | `Selected City` | `greeting`, `subText`, `storeCallout` |

The page registers these (empty defaults) via `clevertap.defineVariable(name, obj)` in `wzrk.onload`,
and reads them with the synchronous `clevertap.getVariables()`. **The variable can be either an
Object/map type OR a String type holding the JSON text — the page handles both** (it `JSON.parse`s
the value when CleverTap returns it as a string, which is what String-type variables do). No nested
arrays — `perks` is a comma-separated string the page splits.

---

## 2. One-time setup

### 2a. Init (`<head>`)
Set your **`region`** and **`token`** (Dashboard → Settings → Passcode) in the `clevertap` object,
and confirm the account ID. (Token is only needed for the sync step below; anonymous visitors get
targeted values with just account ID + region.)

### 2b. Register the variables on the dashboard
Open the page as a **Test Profile** with the sync flag: **`vijaysales.html?ctsync=1`**.
The console logs `[VS_PE] Defined variables…` then `[VS_PE] ✅ Synced…`, and the 3 variables appear
under **Product Experiences → Variables** as object/map variables. Remove the flag afterward.
(If sync fails: token+region set? profile marked Test? discard any open draft, then retry.)

---

## 3. Create the Experiences (the if/else lives here)

One Experience per variable, with branches on the user property. **+ Create Experience → pick the
variable → add a segment/condition on the user property → set the object value → Publish.**

### UC1 — `vs_reco`, branch on `Last Category Clicked`
| If `Last Category Clicked` = | Set `vs_reco` to |
|---|---|
| `Air Conditioners` | `{"category":"Air Conditioners","mainText":"Beat the Heat — Top ACs picked for you","subText":"Inverter Split ACs from ₹26,990 · No Cost EMI · Free Installation","image":"https://s7ap1.scene7.com/is/image/vsproddmfinal/Ac_Fest?dpr=on,2&bfc=on"}` |
| `TV & Entertainment` | `{"category":"TV & Entertainment","mainText":"Big-screen entertainment, just for you","subText":"4K QLED & Mini-LED Smart TVs · Up to 32% OFF","image":"<TV banner image url>"}` |
| `Microwave` | `{"category":"Microwave","mainText":"Cook smarter — Microwaves & Ovens for you","subText":"Convection, Solo & Grill · Starting ₹6,499","image":"https://s7ap1.scene7.com/is/image/vsproddmfinal/Microwave_desktop?dpr=on,2&bfc=on"}` |

> `category` must be exactly `Air Conditioners` / `TV & Entertainment` / `Microwave` — the page uses
> it to also move that nav link + category tile to the front. `mainText`, `subText`, `image` are
> shown in the hero. If a visitor matches no branch, `mainText` is empty → the hero stays hidden.

### UC3 — `vs_loyalty`, branch on `Loyalty Tier`
| If `Loyalty Tier` = | Set `vs_loyalty` to |
|---|---|
| `Silver` | `{"tierLabel":"Silver","greeting":"Welcome back! You're a Silver member","perks":"Free delivery,Extended 1-yr warranty,Member prices","accentColor":"#94a3b8"}` |
| `Gold` | `{"tierLabel":"Gold","greeting":"Welcome back, Gold member 👑","perks":"Free installation,Priority delivery,Extended warranty,Exclusive Gold prices","accentColor":"#b8860b"}` |
| `Platinum` | `{"tierLabel":"Platinum","greeting":"Welcome back, Platinum member 💎","perks":"Dedicated concierge,Same-day delivery,3-yr warranty,Early sale access","accentColor":"#111827"}` |

> No match (e.g. logged out) → empty greeting → the page shows the **guest sign-in nudge**.
> `perks` is a single comma-separated string; the page splits it into chips.

### UC4 — `vs_city`, branch on `Selected City`
| If `Selected City` = | Set `vs_city` to |
|---|---|
| `Mumbai` | `{"greeting":"नमस्कार मुंबई! 🙏","subText":"मुंबईत जलद डिलिव्हरी आणि जवळचे स्टोअर","storeCallout":"Nearest store: Vijay Sales, Andheri West — 2.3 km"}` |
| `Delhi` | `{"greeting":"नमस्ते दिल्ली! 🙏","subText":"दिल्ली में तेज़ डिलीवरी और नज़दीकी स्टोर","storeCallout":"Nearest store: Vijay Sales, Nehru Place — 1.8 km"}` |
| `Bengaluru` | `{"greeting":"ನಮಸ್ಕಾರ ಬೆಂಗಳೂರು! 🙏","subText":"ಬೆಂಗಳೂರಿನಲ್ಲಿ ವೇಗದ ಡೆಲಿವರಿ ಮತ್ತು ಹತ್ತಿರದ ಸ್ಟೋರ್","storeCallout":"Nearest store: Vijay Sales, Koramangala — 2.1 km"}` |

> No match → empty greeting → the city strip stays hidden.

---

## 4. The runtime flow (what happens on each trigger)

1. **Trigger** — the page calls `clevertap.profile.push({ "Site": { "<property>": "<value>" } })`:
   - Click a category (top nav or category rail) → `Last Category Clicked`
   - Pick a tier (Sign In / Triggers panel) → `Loyalty Tier`
   - Pick a city (Triggers panel) → `Selected City`
2. **Re-evaluate** — the page calls `clevertap.fetchVariables()`; CleverTap evaluates your if/else
   for the updated property and returns the matching object.
3. **Render** — the page reads `clevertap.getVariables()` and shows the hero / loyalty strip / city strip.
   It also re-renders on `addVariablesChangedCallback` and on the auto-fetch at first page view.

Because targeting is on a **user property** (not slow segment membership), the new value comes back
on the very next `fetchVariables()` — which the page calls immediately after the push.

## 5. Demo / testing
- The **"CleverTap PE — Triggers"** panel (bottom-left) fires the same user-property pushes, so you
  can switch states without hunting for the on-page control. The values shown always come from your
  dashboard rules.
- Real on-page **category clicks** (nav + rail) also push `Last Category Clicked`.
- Watch the console: `[VS_PE] PE values: {...}` shows exactly what came back from CleverTap.
- Before you've configured an Experience, triggers push the property but the hero/strips stay
  empty/guest (nothing to show yet) — that's expected.

## 6. Notes
- Variable **names** (`vs_reco`, `vs_loyalty`, `vs_city`) and **field keys** must match exactly.
- Account **token** is only for `syncVariables()`; production/anonymous visitors don't need it.
- Festival theme will be added the same way (its own variable + trigger) once these 3 are confirmed.
