# uploadFile: (binary)
# token: 9caa9113e321250d2ba6ea60e710c7ab
# crm_platform_type: lixiaoyun
import requests
from tools.yamlControl import get_yaml_data
from configs.config import HOST
DEV_HOST = HOST.search_fin_test()
class upload_batch_search_file():
    def __init__(self,inData,HOST):
        self.HOST = HOST
        self.token = inData['current_user_token']
        self.lixiaoyun = inData['lixiaoyun']
        # self.oss_key = oss_key
        # self.file = file
    def search_files(self,files):
        url = f'https://{self.HOST}/api_skb/v1/batch_search/upload_file'
        headers = {
            'Authorization': f'{self.token}',
            'crm_platform_type': f'{self.lixiaoyun}'
        }
        fl = open(f'C:\\Users\\admin\\Desktop\\上传数据\\{files}', 'rb')
        file = {"uploadFile": (f'{files}', fl, {})}
        return requests.post(url=url, headers=headers, files=file,verify=True).json()
    def search_fin(self,oss_key):
        oss_key = oss_key
        if oss_key == "None":
            oss_key = None
        url = f'https://{self.HOST}/api_skb/v1/batch_search'
        headers = {
            'Authorization': f'{self.token}',
            'crm_platform_type': f'{self.lixiaoyun}'
        }
        json = {
            'oss_key': oss_key
        }
        # print(requests.post(url, headers=headers, json=json).json())
        return requests.post(url, headers=headers, json=json).json()
# verify=False #关闭证书验证，若开启代理则需要在请求内加此说明，关闭证书验证
if __name__ == '__main__':
    fin = get_yaml_data('../Data/search_fin.yaml')
    file = get_yaml_data('../Data/search_files.yaml')
    # print(fin[8])
    print(len(file))
    # print(len(file))
    host = HOST.search_fin_test()
    from pprint import pprint
    # res = upload_batch_search_file(fin[j][0], host).search_fin(fin[j][0]["oss_key"])
    # res_1 = upload_batch_search_file(file[i][0], host).search_files(file[i][0]["file_name"])
    for i in file:
        res_1 = upload_batch_search_file(i[0], host).search_files(i[0]["file_name"])
        # pprint(res_1)
        print(res_1)
    # for j in fin:
    #     res = upload_batch_search_file(j[0], host).search_fin(j[0]["oss_key"])
    #     print(res)

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

