import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
hf_token = os.getenv('HF_TOKEN')
if hf_token:
    print(f"HF_TOKEN exists and begins {hf_token[:2]}")
else:
    print("HF_TOKEN not set (and this is optional)")

MODEL1='black-forest-labs/FLUX.1-schnell'

response = requests.post(
    f"https://router.huggingface.co/hf-inference/models/{MODEL1}",
    headers={
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
        "Content-Type": "application/json"
    },
    json={
        "inputs":"A plane flying over vast ocean as seen from top"
    },
    timeout=180
)

print(response.status_code)

if response.status_code == 200:
    with open("flux2.png","wb") as f:
        f.write(response.content)

    print("Saved flux.png")
else:
    print(response.text)