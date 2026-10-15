import re, json, requests

H = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.misli.az",
    "Referer": "https://www.misli.az/",
    "Accept": "application/json",
}
API = "https://apivx.misli.az/api/web/"
out = []

for st in ["1", "football", "FOOTBALL", "soccer", "SOCCER"]:
    u = API + f"statistics/sport/{st}/matches/live"
    try:
        r = requests.get(u, headers=H, timeout=30)
        out.append(f"GET {u}\n{r.status_code} {r.text[:300]}\n")
    except Exception as e:
        out.append(f"GET {u}\nERR {e}\n")

for body in [{}, {"sportType": "football"}]:
    u = API + "sportsbook/events/markets"
    try:
        r = requests.post(u, headers=H, json=body, timeout=30)
        out.append(f"POST {u} {body}\n{r.status_code} {r.text[:300]}\n")
    except Exception as e:
        out.append(f"POST {u}\nERR {e}\n")

base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
for s in re.findall(r'src="([^"]+\.js[^"]*)"', html):
    if "_nuxt" not in s:
        continue
    u = s if s.startswith("http") else base + s
    js = requests.get(u, headers=H, timeout=30).text
    for k, n_max, w in [("events/markets", 2, 350), ("sportType:", 4, 150), ("ootball", 4, 150)]:
        n = 0
        for m in re.finditer(re.escape(k), js):
            out.append(f"## {k}\n" + js[max(0, m.start() - w): m.end() + w] + "\n")
            n += 1
            if n >= n_max:
                break

text = "\n".join(out)
text = re.sub(r"(.{45})", r"\1\n", text.replace("\r", ""))
open("probe2.txt", "w", encoding="utf-8").write(text)
print(len(text))
