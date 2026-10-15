import re, requests

H = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.misli.az",
    "Referer": "https://www.misli.az/",
    "Accept": "application/json",
}
out = []
for u in [
    "https://apivx.misli.az/api/web/sportsbook/events?ids=1",
    "https://apivx.misli.az/api/web/sportsbook/favorite-markets",
    "https://socket-service.misli.az/socket.io/?EIO=4&transport=polling",
]:
    try:
        r = requests.get(u, headers=H, timeout=30)
        out.append(f"GET {u}\n{r.status_code} {r.text[:250]}\n")
    except Exception as e:
        out.append(f"GET {u}\nERR {e}\n")

base = "https://www.misli.az"
html = requests.get(base, headers=H, timeout=30).text
for s in re.findall(r'src="([^"]+\.js[^"]*)"', html):
    if "_nuxt" not in s:
        continue
    u = s if s.startswith("http") else base + s
    js = requests.get(u, headers=H, timeout=30).text
    for k, n_max, w in [("baseURL", 5, 250), ("publicAxios", 4, 250), ("eventSpace", 3, 300), ("scoreSpace", 2, 300)]:
        n = 0
        for m in re.finditer(re.escape(k), js):
            out.append(f"## {k}\n" + js[max(0, m.start() - w): m.end() + w] + "\n")
            n += 1
            if n >= n_max:
                break

text = "\n".join(out)
text = re.sub(r"(.{45})", r"\1\n", text.replace("\r", ""))
open("probe3.txt", "w", encoding="utf-8").write(text)
print(len(text))
