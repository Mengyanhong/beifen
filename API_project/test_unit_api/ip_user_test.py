#  ip识别企业接口
import requests, pytest, os
from pprint import pprint
from API_project.Configs.Config_Info import Config_info
from API_project.tools.Excelread import Excel_Files
test_search_api = Config_info(host="lxcrm")


class Test_ips:
    def skb_ip_user(self, IP, orgName=None):  # 查询联系方式
        payload = {"ip": IP}
        if orgName is not None:
            payload.update({"orgName": orgName})
        url = f'https://{Config_info(host="lxcrm").telephone_url_Host()}/api_utility/v2/ip_user/street'
        response = requests.get(url=url, params=payload, headers=Config_info(host="lxcrm").headers_telephone())
        return response

    def skb_ips_user(self, IP):  # 查询联系方式
        payload = {"ips": IP}
        url = f'https://{test_search_api.telephone_url_Host()}/api_utility/v2/ips_user/street'
        response = requests.get(url=url, params=payload, headers=test_search_api.headers_telephone())
        return response

    @pytest.mark.parametrize('IP', ["1.1.8.11", "1.1.8.19", "36.33.24.179", "117.184.79.238"])
    def test_skb_ip_user(self, IP, orgName=None):  # 查询联系方式
        payload = {"ip": IP}
        if orgName is not None:
            payload.update({"orgName": orgName})
        url = f'https://{Config_info(host="lxcrm").telephone_url_Host()}/api_utility/v2/ip_user/street'
        response = requests.get(url=url, params=payload, headers=Config_info(host="lxcrm").headers_telephone())
        print(response.json())
        return response

    @pytest.mark.parametrize('IP',
                             [Excel_Files(file_name="IPData.xlsx", sheel="IPData").open_file_rows("ip")[500:701:1]])
    # @pytest.mark.parametrize("host", ["test"])
    def test_ips_user_case_lang(self, IP):
        ips_user_seaceh_value = self.skb_ips_user(IP=IP)
        # print(ips_user_seaceh_value.url)
        # print(ips_user_seaceh_value.request.headers)
        # print(ips_user_seaceh_value.request.method)
        # print(len(IP))
        # print(IP)
        ips_user_seaceh_value = ips_user_seaceh_value.json()
        assert len(IP) > 200
        print(ips_user_seaceh_value)
        assert ips_user_seaceh_value["code"] == 7003
        assert ips_user_seaceh_value["message"] == "参数长度超限"

    # @pytest.mark.parametrize('IP', [["1.1.8.11", "1.1.8.19", "36.33.24.179", "117.184.79.238"], ["117.184.79.238"]])
    @pytest.mark.parametrize('IP', [Excel_Files(file_name="IPData.xlsx", sheel="IPData").open_file_rows("ip")[500:800:2]])
    def test_ips_user_case(self, IP):
        ips_user_seaceh_value = self.skb_ips_user(IP=IP)
        # print(ips_user_seaceh_value.url)
        # print(ips_user_seaceh_value.request.headers)
        # print(ips_user_seaceh_value.request.method)
        # print(len(IP))
        # print(IP)
        ips_user_seaceh_value = ips_user_seaceh_value.json()
        assert IP != 0
        print(ips_user_seaceh_value)
        assert ips_user_seaceh_value["code"] == 0
        assert len(ips_user_seaceh_value["data"]) == len(IP)
        for ips_responses_value in ips_user_seaceh_value["data"]:
            ip_user_seaceh_value = self.skb_ip_user(IP=ips_responses_value["ip"]).json()
            assert ip_user_seaceh_value["code"] == 0
            assert ips_responses_value == ip_user_seaceh_value["data"]
            print(ips_responses_value == ip_user_seaceh_value["data"])
        pprint(ips_user_seaceh_value["data"])
        return ips_user_seaceh_value["data"]

    @pytest.mark.parametrize('IP', [["1.1.8.11", "1.1.8.19", "36.33.24.179", "117.184.79.238"]])
    def test_skb_ips_user_Authorization(self, IP):  # 查询联系方式
        payload = {"ips": IP}
        telephone_headers = {"appid": "1000000",
                             "orgid": "6929",
                             "appkey": "BC3E6D63C4C4462F8952F785ADE8CB8"
                             }
        url = f'https://{test_search_api.telephone_url_Host()}/api_utility/v2/ips_user/street'
        respons = requests.get(url=url, params=payload, headers=telephone_headers)
        assert respons.status_code == 200
        response = respons.json()
        assert response["code"] == 1119
        assert response["message"] == "用户鉴权失败"

    @pytest.mark.parametrize('IP',
                             ["1.1.8.19,36；33.24.179", ["1.1.8.19", "36.33.24,179"], ["1.1.8.a19,36.33.24.179"], " ",
                              "\t", ["1.1.8.19", "36.33.\n.179"], "ABC", "上海", ";", "{}", "x", "\\n"])
    def test_skb_ips_user_payload(self, IP):  # 查询联系方式
        payload = {"ips": IP}
        url = f'https://{test_search_api.telephone_url_Host()}/api_utility/v2/ips_user/street'
        respons = requests.get(url=url, params=payload, headers=test_search_api.headers_telephone())
        assert respons.status_code == 200
        print(respons.request.url)
        response = respons.json()
        print(response)
        assert response["code"] == 1001
        assert response["message"] == "服务器错误"


if __name__ == '__main__':
    # pytest.main(
    #     ["ip_user_test.py::Test_ips::test_ips_user_case", "-s", "--alluredir", "../report/tmp"])  # -s 打印输出,-sq简化打印
    # # os.system("allure serve ../report/temp")
    # os.system("allure generate ../report/tmp -o ../report/temp --clean")
    # ip_value = Test_ips().skb_ip_user(IP="117.184.79.238", orgName="沧州师范学院")
    ips_value = Test_ips().skb_ips_user(
        IP=Excel_Files(file_name="IPData.xlsx", sheel="IPData").open_file_rows("ip")[200:500])
    pprint(ips_value.status_code)
    pprint(ips_value.json())
# """f   用例失败
#    E   ERROR
#    。  成功的
# """
