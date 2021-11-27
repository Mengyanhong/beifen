import requests
from UC_wwj_skb_test.tools.yamlControl import get_yaml_data
from UC_wwj_skb_test.Configs.config import HOST
class industry_labels():
    def __init__(self,inData,HOST):
        self.HOST = HOST
        self.token = inData['current_user_token']
        self.lixiaoyun = inData['lixiaoyun']
        # self.oss_key = oss_key
        # self.file = file
    def industry_tags(self):
        url = f'https://{self.HOST}/api_skb/v1/search/industry_tags'
        headers = {
            'app_token': 'f6620ff6729345c8b6101174e695d0ab',
            'Authorization': f'{self.token}',
            'crm_platform_type': f'{self.lixiaoyun}'
        }
        json = {"scope":"industryTags","pagesize":10,"page":1,"filter":{"industryTags":["0101010f00"],"filterSync":0,"filterSyncRobot":0,"filterUnfold":0,"sortBy":0}}

        return requests.post(url=url, headers=headers, json=json).json()
if __name__ == '__main__':
    file = get_yaml_data('../Data/test_se_fin.yaml')
    print(file[2][0])
    host = HOST.search_fin_test()
    for i in file:
        fi = industry_labels(i[0],host).industry_tags()
        print(fi)