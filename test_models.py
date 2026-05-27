import requests

base_url = "https://dairy-trio-railway-rebate.trycloudflare.com/v1"
api_key = "lm-studio"
headers = {"Authorization": f"Bearer {api_key}"}
resp = requests.get(f"{base_url}/models", headers=headers)
models = [m['id'] for m in resp.json().get('data', [])]

for m in models:
    if "embed" in m.lower():
        continue
    print(f"Testing {m}...")
    payload = {
        "model": m,
        "messages": [{"role": "user", "content": "1"}],
        "max_tokens": 1
    }
    try:
        r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=3)
        if r.status_code == 200:
            print(f"✅ {m} is loaded!")
        else:
            print(f"❌ {m} returned {r.status_code}: {r.text}")
    except Exception as e:
        print(f"❌ {m} timed out or failed: {e}")
