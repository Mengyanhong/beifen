# uploadFile: (binary)
# token: 9caa9113e321250d2ba6ea60e710c7ab
# crm_platform_type: lixiaoyun
import requests
from tools.yamlControl import get_yaml_data
from configs.config import HOST
DEV_HOST = HOST.search_fin_test()

# verify=False #关闭证书验证，若开启代理则需要在请求内加此说明，关闭证书验证
def industryTags():
    url = "https://test.lixiaoskb.com/api_skb/v1/companyDetail/staticConfig?"
    headers = {
        'Authorization': "Token token=79a2e06cac73c8ae219369cf30d4a30d",
        'crm_platform_type': "lixiaoyun"
    }
    data = {"namespace": "industryTags"}
    ret = requests.get(url,headers=headers,params=data)
    return(ret)
if __name__ == '__main__':
    print(industryTags())

# url = f'https://{DEV_HOST}/api_skb/v1/batch_search'
# headers = {
#     'Authorization': "Token token=79a2e06cac73c8ae219369cf30d4a30d",
#     'crm_platform_type': "lixiaoyun"
# }
# json = {
#     "oss_key": None
# }
# print(requests.post(url, headers=headers, json=json).json())

# url = f'https://{DEV_HOST}/api_skb/v1/upload_batch_search_file'
# headers = {
#     'Authorization': "Token token=e3b502c07cf7bf42ac29afd7d6267418",
#     'crm_platform_type': "lixiaoyun"
# }
# fl = open(r'C:\Users\admin\Desktop\CRM_线索_导入模板.xlsx','rb')
# file = {"uploadFile":("CRM_线索_导入模板.xlsx",fl,{})}
# json = {
#     "oss_key": None
# }
# print(requests.Request('POST', url, headers=headers, files=file).json())
# print(requests.post(url=url, headers=headers, files=file).json())

