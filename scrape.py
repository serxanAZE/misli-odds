import re, requests

H = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.misli.az",
    "Referer": "https://www.misli.az/",
    "Accept": "application/json",
}
base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
cfg = {}
jss = []
for s in re.findall(r'src="([^"]+\.js[^"]*)"', html):
    if "_nuxt" not in s:
        continue
    u = s if s.startswith("http") else base + s
    js = requests.get(u, headers=H, timeout=30).text
    jss.append(js)
    for k, v in re.findall(r'([A-Z][A-Z0-9_]*(?:URL|HOST)[A-Z0-9_]*)\s*:\s*"(https?://[^"]+)"', js):
        cfg[k] = v

W = cfg.get("WAGER_STATS_AGGREGATOR_API_URL", "")
out = [f"W={W}"]

def get(u):
    try:
        r = requests.get(u, headers=H, timeout=30)
        out.append(f"GET {u}\n{r.status_code} {r.text[:500]}\n")
    except Exception as e:
        out.append(f"GET {u}\nERR {e}\n")

get(W)
for st in ["1", "2", "soccer", "SOCCER", "football", "FOOTBALL"]:
    get(W + f"statistics/sport/{st}/matches/live")

for js in jss:
    for k, n_max, w in [("SOCCER", 3, 200), ("soccer", 3, 200), ("sportTypes", 3, 200), ("matches/live", 2, 200)]:
        n = 0
        for m in re.finditer(re.escape(k), js):
            out.append(f"## {k}\n" + js[max(0, m.start() - w): m.end() + w] + "\n")
            n += 1
            if n >= n_max:
                break

text = "\n".join(out)
text = re.sub(r"(.{45})", r"\1\n", text.replace("\r", ""))
open("probe4.txt", "w", encoding="utf-8").write(text)
print(len(text))
