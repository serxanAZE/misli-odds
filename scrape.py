import re, requests

H = {"User-Agent": "Mozilla/5.0"}
base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
srcs = re.findall(r'src="([^"]+\.js[^"]*)"', html)

keys = [
    "sportsbook/events/markets",
    "api/web/",
    "matches/live",
    "coupon/game/",
    "api/web/event",
]
out = []
for s in srcs:
    if "_nuxt" not in s:
        continue
    u = s if s.startswith("http") else base + s
    js = requests.get(u, headers=H, timeout=30).text
    for k in keys:
        n = 0
        for m in re.finditer(re.escape(k), js):
            a = max(0, m.start() - 160)
            b = min(len(js), m.end() + 160)
            out.append(f"## {k} @ {u[-14:]}\n{js[a:b]}\n")
            n += 1
            if n >= 3:
                break

text = "\n".join(out)
text = re.sub(r"(.{55})", r"\1\n", text.replace("\r", ""))
open("ctx.txt", "w", encoding="utf-8").write(text)
print(len(text))
