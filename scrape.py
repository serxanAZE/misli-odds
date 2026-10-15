import re, requests

H = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.misli.az",
    "Referer": "https://www.misli.az/",
}
base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
pairs = set()
for s in re.findall(r'src="([^"]+\.js[^"]*)"', html):
    if "_nuxt" not in s:
        continue
    u = s if s.startswith("http") else base + s
    js = requests.get(u, headers=H, timeout=30).text
    for k, v in re.findall(r'([A-Z][A-Z0-9_]*(?:URL|HOST|API)[A-Z0-9_]*)\s*:\s*"(https?://[^"]+)"', js):
        pairs.add((k, v))

out = []
for k, v in sorted(pairs):
    try:
        r = requests.get(v, headers=H, timeout=20)
        out.append(f"{k}\n{v}\nstatus {r.status_code}\n")
    except Exception as e:
        out.append(f"{k}\n{v}\nERR {e}\n")

text = "\n".join(out)
open("config.txt", "w", encoding="utf-8").write(text)
print(text)
