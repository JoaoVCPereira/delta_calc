import requests
import json

reqUrl = "https://brasilapi.com.br/api/taxas/v1/"



response = json.loads(requests.get(reqUrl).content)
print(response)
for data in response:
    print(f"{data.get('nome')}: {data.get('valor')}")