import requests

url = "https://test.lixiaoskb.com/api_skb/v1/companyDetail/getCompanyBaseInfo?"
headers = {
    "Authorization": "Token token=c226f5c5b96665b6aae7ec832e997408",
    "crm_platform_type": "lixiaoyun"
}
params = ({"id": "3805fb5556b7dc860a8ef21ee0709d86",
        "countSection": 1,
        # "market_company": "%E6%B9%96%E5%B7%9E%E6%B9%96%E7%91%9E%E7%94%9F%E6%80%81%E5%86%9C%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
        # "market_source": "advanced_search_list",
        "version": "v3"})
response = requests.get(url, headers=headers, params=params)
print(response.json())
