import re, requests

H = {"User-Agent": "Mozilla/5.0"}
base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
srcs = re.findall(r'src="([^"]+\.js[^"]*)"', html)

out = []
found = set()
for s in srcs:
    if s.startswith("http"):
        u = s
    else:
        u = base + ("" if s.startswith("/") else "/") + s
    try:
        js = requests.get(u, headers=H, timeout=30).text
    except Exception as e:
        out.append(f"ERR {u} {e}")
        continue
    out.append(f"JS {u} {len(js)}")
    for m in re.findall(r'https?://[a-zA-Z0-9.\-]*misli\.az[^\s"\'`\\)]*', js):
        found.add(m)
    for m in re.findall(r'["\'`](/[a-zA-Z0-9_\-/]*(?:odds|event|match|sport|coef|game|live)[a-zA-Z0-9_\-/]*)["\'`]', js, re.I):
        found.add("PATH " + m)

text = "\n".join(out) + "\n\nFOUND\n" + "\n".join(sorted(found))
open("discovery.txt", "w", encoding="utf-8").write(text)
print(text[:3000])
