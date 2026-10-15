import requests

H = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.misli.az",
    "Referer": "https://www.misli.az/",
    "Accept": "application/json",
}
base = "https://apivx.misli.az/api/web"
urls = [
    base + "/",
    base + "/event",
    base + "/matches/live",
    base + "/sportsbook/events/markets",
    "https://virtual-game-aggregator.misli.az/api/web/",
]
out = []
for u in urls:
    try:
        r = requests.get(u, headers=H, timeout=30)
        out.append(f"=== {u}\nSTATUS {r.status_code} TYPE {r.headers.get('content-type')} LEN {len(r.text)}\n{r.text[:700]}\n")
    except Exception as e:
        out.append(f"=== {u}\nERR {e}\n")
text = "\n".join(out)
open("probe.txt", "w", encoding="utf-8").write(text)
print(text)
