from API_project.Configs.Config_Info import user
import requests
from pprint import pprint

host = "test"
user_config = user(host)


def ip():
    url = f"https://{user_config.skb_Host()}/api_skb/v1/ip_pcd"
    header = user_config.headers()
    # header.pop('content-type')
    # header.pop('crm_platform_type')
    print(header)
    response = requests.get(url=url, headers=header).json()
    return response


if __name__ == '__main__':
    pprint(ip())
