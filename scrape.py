import requests

r = requests.get(
    "https://misli.az",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)
with open("odds.csv", "w", encoding="utf-8") as f:
    f.write(f"status,{r.status_code}\nlength,{len(r.text)}\n")
print(r.status_code, len(r.text))
