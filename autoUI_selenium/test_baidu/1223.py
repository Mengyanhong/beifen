# a=0
# for i in range(1,101):
#     a+=i
#     print(a)
# print(a)
# import pprint
from pprint import pprint

LIST = {"condition": {"cn": "composite", "cr": "MUST",
                      "cv": [{"cn": "hasMobile", "cr": "IS", "cv": True, "id": "de3b6010-500a-4a19-abb0-85f910b8a032"},
                             {"id": "03962766-4765-4b28-b381-4d0fd033925d", "cn": "entStatus", "cr": "IN", "cv": ["1"]},
                             {"id": "a2e70b14-6d6c-4f43-8856-000c63e9b93f", "cn": "baikeInfo", "cr": "NOT_IN",
                              "cv": ["京东", "1688", "天猫", "淘宝"]},
                             {"id": "28e7fedb-8517-473c-a901-7f1111491582", "cn": "semKeyword", "cr": "NOT_IN",
                              "cv": ["诚信通", "京东"]},
                             {"id": "35133511-1be1-413e-b329-350d6d3d8f93", "cn": "seoKeyword", "cr": "NOT_IN",
                              "cv": ["京东", "淘宝", "诚信通"]},
                             {"id": "53b50bab-3d32-47f7-a436-0a4d9f61fed8", "cn": "ecomShopPlatform", "cr": "IN",
                              "cv": ["4", "5", "1", "2", "3"]}]}, "hasSyncClue": 0, "hasSyncRobot": 0, "hasUnfolded": 0,
        "sortBy": 0}
list = {"cn": "composite", "cr": "MUST",
        "cv": [{"cn": "hasMobile", "cr": "IS", "cv": True, "id": "de3b6010-500a-4a19-abb0-85f910b8a032"},
               {"id": "03962766-4765-4b28-b381-4d0fd033925d", "cn": "entStatus", "cr": "IN", "cv": ["1"]},
               {"id": "a2e70b14-6d6c-4f43-8856-000c63e9b93f", "cn": "baikeInfo", "cr": "NOT_IN",
                "cv": ["京东", "1688", "天猫", "淘宝"]},
               {"id": "28e7fedb-8517-473c-a901-7f1111491582", "cn": "semKeyword", "cr": "NOT_IN", "cv": ["诚信通", "京东"]},
               {"id": "35133511-1be1-413e-b329-350d6d3d8f93", "cn": "seoKeyword", "cr": "NOT_IN",
                "cv": ["京东", "淘宝", "诚信通"]},
               {"id": "53b50bab-3d32-47f7-a436-0a4d9f61fed8", "cn": "ecomShopPlatform", "cr": "IN",
                "cv": ["4", "5", "1", "2", "3"]}], "hasSyncClue": 0, "hasSyncRobot": 0, "hasUnfolded": 0, "sortBy": 0}
if list == LIST:
    print("测试通过")
    pprint(list)
    pprint(LIST)
