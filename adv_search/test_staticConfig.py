# -*- coding: utf-8 -*-
import openpyxl
from ..adv_search.config_API import staticConfig
import urllib3
urllib3.disable_warnings()

staticConfig=staticConfig()['tradeMarkInventoryCategory']
level1_num_api=len(staticConfig)

data=openpyxl.load_workbook('二级选项.xlsx')
sheet_last=data['商标商品服务']

for i in range(2,1000):
    if sheet_last['G'+str(i)].value==None:
        level1_num_request=i-2
        break
for i in range(2, 1000):
    if sheet_last['J'+str(i)].value==None:
        level2_num_request=i-2
        break


class TestTradeMarkInventoryCategory:
    def test_level(self):
        level2_sum = 0
        print(staticConfig)

        #判断一级的数量和值
        assert level1_num_api==level1_num_request
        for i in range(level1_num_api):
            print(i)
            assert staticConfig[i]['value']==sheet_last['G'+str(i+2)].value

            #判断二级的数量
            level2_num_api=len(staticConfig[i]['sub'])
            level2_num_request = 0
            for a in range(2,1000):
                if sheet_last['I'+str(a+level2_sum)].value==staticConfig[i]['value']:
                    level2_num_request+=1
                else:
                    level2_sum+=level2_num_request
                    break
            assert level2_num_api==level2_num_request

            # 判断二级的值
            for j in range(level2_num_api):
                assert staticConfig[i]['sub'][j]['value'].rstrip()==sheet_last['J'+str(j+2+level2_sum-level2_num_api)].value
                print(i,j)

