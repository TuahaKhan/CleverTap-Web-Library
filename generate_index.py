import os

EXCLUDE = {"index.html"}

def get_tag(filename):
    f = filename.lower()
    if "push" in f:     return "Push"
    if "inbox" in f:    return "Inbox"
    if "visual" in f:   return "Builder"
    if "display" in f:  return "Display"
    if "rudder" in f:   return "Integration"
    if "axis" in f:     return "PE · Axis"
    if "pe" in f:       return "Web SDK"
    if "sample" in f:   return "Demo"
    return "Demo"

def get_title(filename):
    name = filename.replace(".html", "").replace("_", " ").replace("-", " ")
    return " ".join(word.capitalize() for word in name.split())

def get_desc(filename):
    f = filename.lower()
    if "push" in f:         return "Web push notification setup and integration demo."
    if "inbox" in f:        return "Web inbox messaging feature demo and implementation."
    if "visual" in f:       return "Visual builder for creating web campaigns and layouts."
    if "display2" in f:     return "Banner &amp; carousel display demo with CleverTap event tracking."
    if "display" in f:      return "Core web native display component showcase."
    if "rudder" in f:       return "Sample integration connecting RudderStack with CleverTap."
    if "axis" in f:         return "Product Experiences demo tailored for the Axis use case."
    if "pe" in f:           return "Product Experiences demo via the CleverTap Web SDK."
    if "sample" in f:       return "Sample demo page with CleverTap integration."
    return "Demo page hosted on GitHub Pages."

html_files = sorted([
    f for f in os.listdir(".")
    if f.endswith(".html") and f not in EXCLUDE
])

cards = ""
for i, f in enumerate(html_files, 1):
    delay = 0.3 + (i - 1) * 0.08
    cards += f"""
      <a class="card" href="{f}" style="animation-delay: {delay:.2f}s">
        <span class="card-number">{str(i).zfill(2)}</span>
        <span class="card-tag">{get_tag(f)}</span>
        <div class="card-title">{get_title(f)}</div>
        <div class="card-desc">{get_desc(f)}</div>
        <div class="card-arrow">Open demo</div>
      </a>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rashmi's Demo Websites</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
  <style>
    :root {{
      --bg: #f5f0eb;
      --surface: #ede6dd;
      --accent: #c0392b;
      --text: #1a1412;
      --muted: #8a7f78;
      --border: rgba(180, 140, 120, 0.25);
    }}

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Mono', monospace;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    .glow-orb {{
      position: fixed;
      border-radius: 50%;
      filter: blur(120px);
      pointer-events: none;
      z-index: 0;
    }}
    .glow-orb-1 {{ width: 500px; height: 500px; background: rgba(192,57,43,0.07); top: -100px; right: -100px; }}
    .glow-orb-2 {{ width: 400px; height: 400px; background: rgba(124,58,237,0.05); bottom: 100px; left: -100px; }}

    .container {{
      position: relative;
      z-index: 1;
      max-width: 860px;
      margin: 0 auto;
      padding: 80px 32px 100px;
    }}

    header {{ margin-bottom: 72px; }}

    .eyebrow {{
      font-size: 11px;
      letter-spacing: 0.25em;
      color: var(--accent);
      text-transform: uppercase;
      margin-bottom: 16px;
      opacity: 0;
      animation: fadeUp 0.6s ease forwards;
    }}

    h1 {{
      font-family: 'Playfair Display', serif;
      font-size: clamp(38px, 7vw, 68px);
      font-weight: 700;
      line-height: 1.1;
      letter-spacing: -0.02em;
      color: var(--text);
      opacity: 0;
      animation: fadeUp 0.6s ease 0.1s forwards;
    }}

    .subtitle {{
      margin-top: 16px;
      font-size: 13px;
      color: var(--muted);
      letter-spacing: 0.05em;
      opacity: 0;
      animation: fadeUp 0.6s ease 0.2s forwards;
    }}

    .divider {{
      width: 60px;
      height: 1px;
      background: var(--border);
      margin: 32px 0;
      opacity: 0;
      animation: fadeUp 0.6s ease 0.25s forwards;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 16px;
    }}

    .card {{
      position: relative;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 28px 28px 24px;
      text-decoration: none;
      color: var(--text);
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
      overflow: hidden;
      opacity: 0;
      animation: fadeUp 0.5s ease forwards;
    }}

    .card::after {{
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, rgba(192,57,43,0.04) 0%, transparent 60%);
      opacity: 0;
      transition: opacity 0.3s;
    }}

    .card:hover {{
      border-color: rgba(192,57,43,0.35);
      transform: translateY(-3px);
      box-shadow: 0 16px 40px rgba(0,0,0,0.1), 0 0 0 1px rgba(192,57,43,0.1);
    }}

    .card:hover::after {{ opacity: 1; }}

    .card-tag {{
      font-size: 10px;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 500;
    }}

    .card-title {{
      font-family: 'Playfair Display', serif;
      font-size: 20px;
      font-weight: 700;
      line-height: 1.25;
      color: var(--text);
    }}

    .card-desc {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.6;
      flex: 1;
    }}

    .card-arrow {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      letter-spacing: 0.1em;
      color: var(--accent);
      text-transform: uppercase;
      margin-top: 6px;
      transition: gap 0.2s;
    }}

    .card:hover .card-arrow {{ gap: 10px; }}
    .card-arrow::after {{ content: '→'; }}

    .card-number {{
      position: absolute;
      top: 20px;
      right: 24px;
      font-size: 11px;
      color: rgba(107,104,128,0.4);
      letter-spacing: 0.1em;
    }}

    footer {{
      margin-top: 80px;
      padding-top: 32px;
      border-top: 1px solid var(--border);
      font-size: 11px;
      color: var(--muted);
      letter-spacing: 0.1em;
      opacity: 0;
      animation: fadeUp 0.6s ease 1s forwards;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }}

    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(16px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>
  <div class="glow-orb glow-orb-1"></div>
  <div class="glow-orb glow-orb-2"></div>

  <div class="container">
    <header>
      <p class="eyebrow">Rashmi-9514 · GitHub Pages</p>
      <h1>Demo<br>Websites</h1>
      <p class="subtitle">// Click any card to open the demo</p>
      <div class="divider"></div>
    </header>

    <div class="grid">
{cards}
    </div>

    <footer>
      <span>Rashmi · Demo Collection</span>
      <span>{len(html_files)} demos</span>
    </footer>
  </div>
</body>
</html>"""

with open("index.html", "w") as f:
    f.write(html)

print(f"✅ index.html generated with {len(html_files)} demos!")
