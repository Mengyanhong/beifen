import requests
from API_project.Configs.Config_Info import Config_info


class ip(Config_info):
    def skb_ip_user(self, IP, orgName=None):  # 查询联系方式
        payload = {'ip': IP}
        if orgName is not None:
            payload.update({"orgName": orgName})
        # headers = {"appid": "f6620ff6729345c8b6101174e695d0ab",
        #            "orgid": "wwjSpqgS3jEVix65myNL",
        #            "appkey": "fdc7cd52a1808e344b490b9457bb70e3"}
        url = f'https://{self.biz_url_Host()}/api_utility/v2/ip_user/street'
        response = requests.get(url=url, params=payload, headers=self.headers_skb())
        return response


if __name__ == '__main__':
    ip_value = ip("test").skb_ip_user(IP="131", orgName=None)
    print(ip_value.json())
