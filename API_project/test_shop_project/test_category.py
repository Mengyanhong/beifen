# -*- coding: utf-8 -*-# @Time : 2021/7/14 10:55# @Author : 孟艳红# @File : test_category.py 店铺分类import pytest,timefrom API_project.Configs.shop_API import shopfrom API_project.Configs.config_API import configuration_fileHOST = 'staging' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境shop = shop(HOST) #实例化店铺搜索shopCategory = configuration_file(HOST).shopCategory() #实例化店铺分类并返回配置信息category_list=[]category2_list=[]for i in range(len(shopCategory['shopCategory'])):    category_list.append((shopCategory['shopCategory'][i]['name'],shopCategory['shopCategory'][i]['value']))    for j in range(len(shopCategory['shopCategory'][i]['sub'])):        category2_list.append((shopCategory['shopCategory'][i]['sub'][j]['name'],shopCategory['shopCategory'][i]['sub'][j]['value']))class Test_category:    @pytest.mark.parametrize('categoryL1,categoryL1Name',category_list)    def test_CategoryL1(self,categoryL1,categoryL1Name,ES):        es_client = ES        shopdata = shop.categoryL1(categoryL1)        time.sleep(2.5)        if shopdata['error_code'] != 0:            assert shopdata['error_code'] == 0        if shopdata['data']['total'] != 0:            for i in range(len(shopdata['data']['items'])):                response_shop_id = shopdata['data']['items'][i]['id']                response_shop_name = shopdata['data']['items'][i]['name']                response_categoryL1 = shopdata['data']['items'][i]['categoryL1']                print(response_shop_name,'shop_id',response_shop_id)                assert response_categoryL1 == categoryL1Name #断言该店铺的搜索分类和详情页分类是否一致                try:                    es_result = es_client.get(index="shop_info_prod", id=response_shop_id)['_source']  # 获取es搜索数据内容                    print(es_result['categoryL1'])                except:                    pass                else:                    assert int(categoryL1) == es_result['categoryL1'] #断言该店铺搜索分类和es上该店铺的分类是否一致        else:            print('\n搜索结果',shopdata)            assert shopdata['data']['total'] != 0    @pytest.mark.parametrize('categoryL2,categoryL2Name', category2_list)    def test_CategoryL2(self, categoryL2, categoryL2Name, ES):        es_client = ES        shopdata = shop.categoryL2(categoryL2)        time.sleep(2.5)        if shopdata['error_code'] != 0:            assert shopdata['error_code'] == 0        if shopdata['data']['total'] != 0:            for i in range(len(shopdata['data']['items'])):                response_shop_id = shopdata['data']['items'][i]['id']                response_shop_name = shopdata['data']['items'][i]['id']                response_categoryL2 = shopdata['data']['items'][i]['categoryL2']                print(response_shop_name, 'shop_id', response_shop_id)                assert response_categoryL2 == categoryL2Name                try:                    es_result = es_client.get(index="shop_info_prod", id=response_shop_id)['_source']  # 获取es搜索数据内容                    print(es_result['categoryL2'])                except:                    pass                else:                    assert int(categoryL2) == es_result['categoryL2'] #断言该店铺搜索分类和es上该店铺的分类是否一致        else:            print('\n搜索结果',shopdata)            assert shopdata['data']['total'] != 0