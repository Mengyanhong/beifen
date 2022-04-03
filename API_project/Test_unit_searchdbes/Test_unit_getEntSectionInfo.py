from API_project.Configs.Config_Api import Get_Company_Info
from API_project.Configs.Config_Database import ES_All
from API_project.tools.Excelread import Excel_Files
from API_project.tools.get_yaml_set import get_yaml_data
import time, pytest

get_company_api = Get_Company_Info(host="test")
get_company_prod_api = Get_Company_Info(host="lxcrm")


def get_pid_details(host, pid, label, V_doing, major_key, section="IPR"):
    '''
    请求测试维度的数据
    :param section:
    :param host: 环境
    :param pid: 企业pid
    :param label: 测试tab
    :param V_doing: 返回值内的key
    :param major_key: 定义返回字典时的key
    :return:
    '''

    time.sleep(1)
    responses = Get_Company_Info(host=host).getEntSectionInfo(pid, section=section, label=label,
                                                              page=1).json()["data"]
    total = responses[V_doing]["total"]
    items = responses[V_doing]["items"]
    responses_items_dict = {}
    for res_value in items:
        responses_items_dict.update({res_value[major_key]: res_value})
    if 10 < total:
        total_num = round(total // 10)
        total_nums = round(total / 10, 2)
        if total_nums > total_num:
            total_num += 1
        for page in range(2, total_num + 1):
            time.sleep(1)
            responses_ = Get_Company_Info(host=host).getEntSectionInfo(pid, section=section,
                                                                       label=label,
                                                                       page=page).json()["data"]
            items.extend(responses_[V_doing]["items"])
            for res_value_ in responses_[V_doing]["items"]:
                responses_items_dict.update({res_value_[major_key]: res_value_})
    if len(responses_items_dict.items()) != total:
        print("{}responses_items_dict数量计算错误".format(host))
    return {'total': total, 'items': items, 'responses_items_dict': responses_items_dict}


def case_es_compare(pid, ES_search_value, has_list=None, number_list=None, list_list=None):
    """
    列表内参数定义，dict,参数{"detail"：详情数据结果，"fieldName"：ES字段名称}
    :param pid: 测试企业pid
    :param ES_search_value: ES搜索结果
    :param has_list: 有无判断字段列表
    :param number_list: 数字判单字段列表
    :param list_list: 字符判断字段列表
    :return:
    """
    if has_list is not None:
        """开始执行有无字段判断"""
        for has_value in has_list:
            if has_value["detail"]:
                if has_value["fieldName"] not in ES_search_value.keys() or ES_search_value[has_value["fieldName"]] \
                        is not True:
                    print(pid, "{}字段有无搜索错误".format(has_value["fieldName"]))
                    print("detail字段值{}".format(has_value["detail"]))
            else:
                if has_value["fieldName"] in ES_search_value.keys() and ES_search_value[has_value["fieldName"]] is True:
                    print(pid, "{}字段有无搜索错误".format(has_value["fieldName"]))
                    print("detail字段值{},ES字段值{}".format(has_value["detail"], ES_search_value[has_value["fieldName"]]))
                # assert "hasSoftware" not in ES_value.keys() or ES_value["hasSoftware"] is False

        """执行有无字段判断结束"""
    else:
        """没有有无字段，不执行有无搜索判断"""
    if number_list is not None:
        """开始执行数量字段判断"""
        for number_value in number_list:
            if number_value["detail"] != 0:
                if ES_search_value[number_value["fieldName"]] != number_value["detail"] or number_value["fieldName"] \
                        not in ES_search_value.keys() or ES_search_value[number_value["fieldName"]] is None:
                    print(pid, "{}字段数量搜索错误".format(number_value["fieldName"]))
                    print("detail字段值{}".format(number_value["detail"]))
            else:
                if number_value["fieldName"] in ES_search_value.keys() \
                        and ES_search_value[number_value["fieldName"]] is not None \
                        and ES_search_value[number_value["fieldName"]] > 0:
                    print(pid, "{}字段数量搜索错误".format(number_value["fieldName"]))
                    print("detail字段值{},ES字段值{}".format(number_value["detail"],
                                                       ES_search_value[number_value["fieldName"]]))
                # assert ES_value["softwareCount"] is None or "softwareCount" not in ES_value.keys() or \
                #        ES_value["softwareCount"] == 0
        """执行数量字段判断结束"""
    else:
        """没有数量字段，不执行数量搜索判断"""
    if list_list is not None:
        """开始执行字符字段判断"""
        for list_value in list_list:
            if list_value["detail"]:
                if set(list_value["detail"]).intersection(set(ES_search_value[list_value["fieldName"]])) is False \
                        or set(ES_search_value[list_value["fieldName"]]).intersection(
                    set(list_value["detail"])) is False:
                    print(pid, "{}字段内容搜索错误".format(list_value["fieldName"]))
                    print("detail数据量{}ES数据量{}".format(len(set(list_value["detail"])),
                                                      len(ES_search_value[list_value["fieldName"]])))
                    print("detail有数据但是ES没有的数据，\n{}".format(
                        set(list_value["detail"]).difference(set(ES_search_value[list_value["fieldName"]]))))
                    print("ES有数据但是detail没有的数据，\n{}".format(
                        set(ES_search_value[list_value["fieldName"]]).difference(set(list_value["detail"]))))
                    print("ES字段值{}".format(ES_search_value[list_value["fieldName"]]))
                    print("detail字段值{}".format(list_value["detail"]))
            else:
                if list_value["fieldName"] in ES_search_value.keys() and ES_search_value[list_value["fieldName"]] != []:
                    print(pid, "{}字段内容搜索错误".format(list_value["fieldName"]))
                    print("detail字段值{},\nES字段值{}".format(list_value["detail"],
                                                         ES_search_value[list_value["fieldName"]]))
                # assert "softwareProductName" not in ES_value.keys() or ES_value["softwareProductName"] == []
        """执行字符字段判断结束"""
    else:
        """没有字符字段，不执行字符搜索判断"""


def case_search_es(label, V_doing, major_key, ES_host, searchName, has_fieldName, number_fieldName, list_fieldName,
                   page, pagesize, search_host="test", cv=None, pid=None):
    ES = ES_All(environment=ES_host).ES()
    pid_list = []
    if cv is not None:
        time.sleep(2.2)
        pid_responst = Get_Company_Info(host=search_host).advanced_search(cv=cv, page=page, pagesize=pagesize).json()
        if pid_responst['data']['items']:
            for pid in pid_responst['data']['items']:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print("搜索结果为空")
    else:
        pid_list.append(pid)
    for pid_value in pid_list:
        if cv is not None:
            pid = pid_value["pid"]
        else:
            pid = pid_value
        ES_responses = ES.get(index="company_info_prod", id=pid)["_source"]
        prod_detail = get_pid_details(host="lxcrm", pid=pid, label=label, V_doing=V_doing, major_key=major_key)
        if search_host != "lxcrm":
            test_detail = get_pid_details(host=search_host, pid=pid, label=label, V_doing=V_doing, major_key=major_key)
            if test_detail['responses_items_dict'] != prod_detail['responses_items_dict']:
                print(pid_value, "该企业生产数据和{}不一致".format(search_host))
                print("企业生产数据\n{}".format(prod_detail['responses_items_dict']))
                print("企业{}数据\n{}".format(search_host, test_detail['responses_items_dict']))
                print("生产多出的数据",
                      prod_detail['responses_items_dict'].items() - test_detail['responses_items_dict'].items())
                print("测试多出的数据",
                      test_detail['responses_items_dict'].items() - prod_detail['responses_items_dict'].items())
                list_fieldName_list = []
                for detailName in test_detail['items']:
                    list_fieldName_list.append(detailName[searchName])
                case_es_compare(pid=pid_value, ES_search_value=ES_responses,
                                has_list=[{"detail": test_detail['items'], "fieldName": has_fieldName}],
                                number_list=[{"detail": test_detail['total'], "fieldName": number_fieldName}],
                                list_list=[{"detail": list_fieldName_list, "fieldName": list_fieldName}]
                                )
        else:
            list_fieldName_list = []
            for detailName in prod_detail['items']:
                list_fieldName_list.append(detailName[searchName])
            case_es_compare(pid=pid_value, ES_search_value=ES_responses,
                            has_list=[{"detail": prod_detail['items'], "fieldName": has_fieldName}],
                            number_list=[{"detail": prod_detail['total'], "fieldName": number_fieldName}],
                            list_list=[{"detail": list_fieldName_list, "fieldName": list_fieldName}]
                            )
    ES.close()


class Test_IPR:
    @pytest.mark.parametrize('search_host', ["test"])
    @pytest.mark.parametrize('ES_host', ["lxcrm"])
    @pytest.mark.parametrize('cv', [[
        {
            "cn": "hasSoftware",
            "cr": "IS",
            "cv": False
        },
        {
            "cn": "softwareCount",
            "cr": "BETWEEN",
            "cv": [
                "'',1"
            ]
        }
    ]])
    @pytest.mark.parametrize("InDate",
                             [get_yaml_data('../data/yaml/IPR.yaml')['getCompanyBaseInfo']['softWareCopyright']])
    def test_SoftwareCopyright_search(self, search_host, cv, InDate, ES_host):
        case_search_es(label=InDate['label'], V_doing=InDate['V_doing'], major_key=InDate['major_key'],
                       searchName=InDate['searchName'],has_fieldName=InDate['has_fieldName'],
                       number_fieldName=InDate['number_fieldName'], list_fieldName=InDate['list_fieldName'],
                       ES_host=ES_host, search_host=search_host, cv=cv, pid=None, page=1, pagesize=10)


    @pytest.mark.parametrize('search_host', ["lxcrm"])
    @pytest.mark.parametrize('ES_host', ["lxcrm"])
    @pytest.mark.parametrize('pid',
                             Excel_Files(file_name="软件著作写正式es 300个.xlsx",
                                         sheel="软件著作写正式es 300个").open_file_rows("pid")[:10])
    @pytest.mark.parametrize("InDate",
                             [get_yaml_data('../data/yaml/IPR.yaml')['getCompanyBaseInfo']['softWareCopyright']])
    def test_SoftwareCopyright_pid(self, search_host, InDate, ES_host, pid):
        case_search_es(label=InDate['label'], V_doing=InDate['V_doing'], major_key=InDate['major_key'],
                       searchName=InDate['searchName'], has_fieldName=InDate['has_fieldName'],
                       number_fieldName=InDate['number_fieldName'], list_fieldName=InDate['list_fieldName'],
                       ES_host=ES_host, search_host=search_host, cv=None, pid=pid, page=1, pagesize=10)


    @pytest.mark.parametrize('search_host', ["test"])
    @pytest.mark.parametrize('ES_host', ["lxcrm"])
    @pytest.mark.parametrize('cv', [[
                                 {
                                     "cn": "hasWorks",
                                     "cr": "IS",
                                     "cv": False
                                 },
                                 {
                                     "cn": "worksCount",
                                     "cr": "BETWEEN",
                                     "cv": [
                                         "'',1"
                                     ]
                                 }
                             ]])
    @pytest.mark.parametrize("InDate",
                             [get_yaml_data('../data/yaml/IPR.yaml')['getCompanyBaseInfo']['opusCopyright']])
    def test_WorksCopyrightHive_search(self, search_host, cv, InDate, ES_host):
        case_search_es(label=InDate['label'], V_doing=InDate['V_doing'], major_key=InDate['major_key'],
                       searchName=InDate['searchName'],has_fieldName=InDate['has_fieldName'],
                       number_fieldName=InDate['number_fieldName'], list_fieldName=InDate['list_fieldName'],
                       ES_host=ES_host, search_host=search_host, cv=cv, pid=None, page=1, pagesize=10)


    @pytest.mark.parametrize('search_host', ["test"])
    @pytest.mark.parametrize('ES_host', ["lxcrm"])
    @pytest.mark.parametrize('pid',
                             Excel_Files(file_name="作品.xlsx", sheel="Sheet1").open_file_rows("pid"))
    @pytest.mark.parametrize("InDate",
                             [get_yaml_data('../data/yaml/IPR.yaml')['getCompanyBaseInfo']['opusCopyright']])
    def test_WorksCopyrightHive_pid(self, search_host, InDate, ES_host, pid):
        case_search_es(label=InDate['label'], V_doing=InDate['V_doing'], major_key=InDate['major_key'],
                       searchName=InDate['searchName'], has_fieldName=InDate['has_fieldName'],
                       number_fieldName=InDate['number_fieldName'], list_fieldName=InDate['list_fieldName'],
                       ES_host=ES_host, search_host=search_host, cv=None, pid=pid, page=1, pagesize=10)

    @pytest.mark.parametrize('cv',
                             [[
                                 {
                                     "cn": "b2bInfo",
                                     "cr": "IN",
                                     "cv": [
                                         "测试"
                                     ],
                                 },
                                 {
                                     "cn": "baikeInfo",
                                     "cr": "IN",
                                     "cv": [
                                         "测试"
                                     ]
                                 }
                             ]])
    def test_getCompanyBase_bk_b2b(self, cv, ES):
        pid_list = []
        time.sleep(2.2)
        pid_responst = get_company_api.advanced_search(cv=cv, page=6, pagesize=5).json()['data'][
            'items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        for pid_value in pid_list:
            time.sleep(2.2)
            testvalue = get_company_api.getCompanyBase(pid_value["pid"]).json()
            testBaikeInfo = testvalue["data"]["baseSectionInfo"]["BaikeInfo"]
            testEntInfo = testvalue["data"]["baseSectionInfo"]["EntInfo"]
            pordvalue = get_company_prod_api.getCompanyBase(pid_value["pid"]).json()
            pordBaikeInfo = pordvalue["data"]["baseSectionInfo"]["BaikeInfo"]
            pordEntInfo = pordvalue["data"]["baseSectionInfo"]["EntInfo"]
            ES_value = ES.get(index="company_info_prod", id=pid_value["pid"])["_source"]
            if testBaikeInfo != pordBaikeInfo:
                print(pid_value, "该企业生产百科数据和测试不一致")
            # if testvalue["data"]["baseSectionInfo"]["BaikeInfo"]["total"] != 0:
            #     if testBaikeInfo != ES_value["baikeInfo"]:
            #         print("百科ES和详情不一致", pid_value)
            # else:
            #     if "baikeInfo" in ES_value.keys() and ES_value["baikeInfo"] != [] and ES_value["baikeInfo"] is not None:
            #         print("百科ES和详情不一致", pid_value)
            # assert ES_value["baikeInfo"] == [] or "baikeInfo" not in ES_value.keys()
            if testEntInfo != pordEntInfo:
                print(pid_value, "该企业生产简介数据和测试不一致")
            # if testvalue["data"]["baseSectionInfo"]["EntInfo"]["total"] != 0:
            #     if testBaikeInfo != ES_value["b2bInfo"]:
            #         print("企业简介ES和详情不一致", pid_value)
            # else:
            #     if "EntInfo" in ES_value.keys() and ES_value["EntInfo"] != [] and ES_value["EntInfo"] is not None:
            #         print(pid_value, "该企业生产简介数据和测试不一致")
            # assert ES_value["baikeInfo"] == [] or "baikeInfo" not in ES_value.keys()

    # @pytest.mark.parametrize('cv',
    #                          [[
    #                              {
    #                                  "cn": "hasSoftware",
    #                                  "cr": "IS",
    #                                  "cv": False
    #                              },
    #                              {
    #                                  "cn": "softwareCount",
    #                                  "cr": "BETWEEN",
    #                                  "cv": [
    #                                      "'',1"
    #                                  ]
    #                              }
    #                          ]])
    # def test_SoftwareCopyright(self, cv):
    #     pid_list = []
    #     time.sleep(2.2)
    #     pid_responst = get_company_api.advanced_search(cv=cv, page=1, pagesize=100).json()['data'][
    #         'items']
    #     if pid_responst:
    #         for pid in pid_responst:
    #             pid_list.append({'pid': pid['id'], 'entName': pid['name']})
    #     for pid_value in pid_list:
    #         testvalue = get_company_api.getEntSectionInfo(pid_value["pid"], section="IPR", label="softWareCopyright",
    #                                                       page=1).json()
    #         testvaluetotal = testvalue["data"]["softWareCopyright"]["total"]
    #         testvalue_list = testvalue["data"]["softWareCopyright"]["items"]
    #         if 10 < testvaluetotal:
    #             testvaluetotal_num = round(testvaluetotal // 10)
    #             testvaluetotal_nums = round(testvaluetotal / 10, 2)
    #             if testvaluetotal_nums > testvaluetotal_num:
    #                 testvaluetotal_num = testvaluetotal_num + 2
    #             else:
    #                 testvaluetotal_num = testvaluetotal_num + 1
    #             for testvaluetotal_page in range(2, testvaluetotal_num):
    #                 time.sleep(1.2)
    #                 fortestvalue = get_company_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                                  label="softWareCopyright",
    #                                                                  page=testvaluetotal_page).json()
    #                 testvalue_list.extend(fortestvalue["data"]["softWareCopyright"]["items"])
    #         pordvalue = get_company_prod_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                            label="softWareCopyright", page=1).json()
    #         pordvaluetotal = pordvalue["data"]["softWareCopyright"]["total"]
    #         pordvalue_list = pordvalue["data"]["softWareCopyright"]["items"]
    #         if 10 < pordvaluetotal:
    #             pordvaluetotal_num = round(pordvaluetotal // 10)
    #             pordvaluetotal_nums = round(pordvaluetotal / 10, 2)
    #             if pordvaluetotal_nums > pordvaluetotal_num:
    #                 pordvaluetotal_num = pordvaluetotal_num + 2
    #             else:
    #                 pordvaluetotal_num = pordvaluetotal_num + 1
    #             for pordvaluetotal_page in range(2, pordvaluetotal_num):
    #                 time.sleep(1.2)
    #                 forpoedvalue = get_company_prod_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                                       label="softWareCopyright",
    #                                                                       page=pordvaluetotal_page).json()
    #                 pordvalue_list.extend(forpoedvalue["data"]["softWareCopyright"]["items"])
    #         if pordvalue_list != testvalue_list:
    #             print(pid_value, "该企业生产数据和测试不一致")
    #
    # @pytest.mark.parametrize('pid',
    #                          Excel_Files(file_name="软件著作写正式es 300个.xlsx",
    #                                      sheel="软件著作写正式es 300个").open_file_rows("pid"))
    # def test_SoftwareCopyright_ES(self, pid, ES):
    #     ES_value = ES.get(index="company_info_prod", id=pid)["_source"]
    #     time.sleep(1)
    #     testvalue = get_company_api.getEntSectionInfo(pid, section="IPR",
    #                                                   label="softWareCopyright",
    #                                                   page=1).json()
    #     testvaluetotal = testvalue["data"]["softWareCopyright"]["total"]
    #     testvalue_list = testvalue["data"]["softWareCopyright"]["items"]
    #     testvalue_list_dict = {}
    #     for testvalue_list_dict_softname in testvalue_list:
    #         testvalue_list_dict.update({testvalue_list_dict_softname["registNo"]: testvalue_list_dict_softname})
    #     if 10 < testvaluetotal:
    #         testvaluetotal_num = round(testvaluetotal // 10)
    #         testvaluetotal_nums = round(testvaluetotal / 10, 2)
    #         if testvaluetotal_nums > testvaluetotal_num:
    #             testvaluetotal_num = testvaluetotal_num + 2
    #         else:
    #             testvaluetotal_num = testvaluetotal_num + 1
    #         for testvaluetotal_page in range(2, testvaluetotal_num):
    #             time.sleep(1.2)
    #             fortestvalue = get_company_api.getEntSectionInfo(pid, section="IPR",
    #                                                              label="softWareCopyright",
    #                                                              page=testvaluetotal_page).json()
    #             # testvalue_list.extend(fortestvalue["data"]["softWareCopyright"]["items"])
    #             for fortestvalue_dict_softname in fortestvalue["data"]["softWareCopyright"]["items"]:
    #                 testvalue_list_dict.update({fortestvalue_dict_softname["registNo"]: fortestvalue_dict_softname})
    #     if len(testvalue_list_dict.items()) != testvaluetotal:
    #         print("testvalue_list_dict数量计算错误")
    #     time.sleep(1)
    #     pordvalue = get_company_prod_api.getEntSectionInfo(pid, section="IPR",
    #                                                        label="softWareCopyright", page=1).json()
    #     pordvaluetotal = pordvalue["data"]["softWareCopyright"]["total"]
    #     pordvalue_list = pordvalue["data"]["softWareCopyright"]["items"]
    #     pordvalue_list_dict = {}
    #     for pordvalue_list_dict_softname in pordvalue_list:
    #         pordvalue_list_dict.update({pordvalue_list_dict_softname["registNo"]: pordvalue_list_dict_softname})
    #     if 10 < pordvaluetotal:
    #         pordvaluetotal_num = round(pordvaluetotal // 10)
    #         pordvaluetotal_nums = round(pordvaluetotal / 10, 2)
    #         if pordvaluetotal_nums > pordvaluetotal_num:
    #             pordvaluetotal_num = pordvaluetotal_num + 2
    #         else:
    #             pordvaluetotal_num = pordvaluetotal_num + 1
    #         for pordvaluetotal_page in range(2, pordvaluetotal_num):
    #             time.sleep(1.2)
    #             forpoedvalue = get_company_prod_api.getEntSectionInfo(pid, section="IPR",
    #                                                                   label="softWareCopyright",
    #                                                                   page=pordvaluetotal_page).json()
    #             # pordvalue_list.extend(forpoedvalue["data"]["softWareCopyright"]["items"])
    #             for forpoedvalue_list_dict_softname in forpoedvalue["data"]["softWareCopyright"]["items"]:
    #                 pordvalue_list_dict.update(
    #                     {forpoedvalue_list_dict_softname["registNo"]: forpoedvalue_list_dict_softname})
    #     if len(pordvalue_list_dict.items()) != pordvaluetotal:
    #         print("pordvalue_list_dict数量计算错误")
    #     if pordvalue_list_dict != testvalue_list_dict:
    #         print(pid, "该企业生产数据和测试不一致")
    #         print(pordvalue_list_dict)
    #         print(testvalue_list_dict)
    #         print(set(testvalue_list_dict).difference(set(pordvalue_list_dict)))
    #     softwareName_list = []
    #     for softwareName in pordvalue_list:
    #         softwareName_list.append(softwareName["softwareName"])
    #     if pordvalue_list:
    #         if ES_value["hasSoftware"] is not True:
    #             print(pid, "有无错误")
    #             print(ES_value["hasSoftware"])
    #         # assert ES_value["hasWorks"] is True
    #         if ES_value["softwareCount"] != testvaluetotal:
    #             print(pid, "数量错误")
    #             print(ES_value["softwareCount"], testvaluetotal)
    #         # assert ES_value["worksCount"] == testvaluetotal
    #         if set(softwareName_list).intersection(set(ES_value["softwareProductName"])) is False or set(
    #                 ES_value["softwareProductName"]).intersection(set(softwareName_list)) is False:
    #             print(pid, "名称错误")
    #             print(softwareName_list, '\n', ES_value["softwareProductName"])
    #             print(len(softwareName_list), len(ES_value["softwareProductName"]))
    #         # assert ES_value["hasSoftware"] is True
    #         # assert ES_value["softwareCount"] == testvaluetotal
    #         # assert softwareName_list == ES_value["softwareProductName"]
    #     else:
    #         assert "hasSoftware" not in ES_value.keys() or ES_value["hasSoftware"] is False
    #         assert ES_value["softwareCount"] is None or "softwareCount" not in ES_value.keys() or \
    #                ES_value["softwareCount"] == 0
    #         assert "softwareProductName" not in ES_value.keys() or ES_value["softwareProductName"] == []
    #
    # @pytest.mark.parametrize('cv',
    #                          [[
    #                              {
    #                                  "cn": "hasWorks",
    #                                  "cr": "IS",
    #                                  "cv": False
    #                              },
    #                              {
    #                                  "cn": "worksCount",
    #                                  "cr": "BETWEEN",
    #                                  "cv": [
    #                                      "'',1"
    #                                  ]
    #                              }
    #                          ]])
    # def test_WorksCopyrightHive(self, cv):
    #     pid_list = []
    #     time.sleep(2.2)
    #     pid_responst = get_company_api.advanced_search(cv=cv, page=1, pagesize=100).json()['data'][
    #         'items']
    #     if pid_responst:
    #         for pid in pid_responst:
    #             pid_list.append({'pid': pid['id'], 'entName': pid['name']})
    #     for pid_value in pid_list:
    #         testvalue = get_company_api.getEntSectionInfo(pid_value["pid"], section="IPR", label="opusCopyright",
    #                                                       page=1).json()
    #         testvaluetotal = testvalue["data"]["opusCopyright"]["total"]
    #         testvalue_list = testvalue["data"]["opusCopyright"]["items"]
    #         if 10 < testvaluetotal:
    #             testvaluetotal_num = round(testvaluetotal // 10)
    #             testvaluetotal_nums = round(testvaluetotal / 10, 2)
    #             if testvaluetotal_nums > testvaluetotal_num:
    #                 testvaluetotal_num = testvaluetotal_num + 2
    #             else:
    #                 testvaluetotal_num = testvaluetotal_num + 1
    #             for testvaluetotal_page in range(2, testvaluetotal_num):
    #                 time.sleep(1.2)
    #                 fortestvalue = get_company_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                                  label="opusCopyright",
    #                                                                  page=testvaluetotal_page).json()
    #                 testvalue_list.extend(fortestvalue["data"]["opusCopyright"]["items"])
    #         pordvalue = get_company_prod_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                            label="opusCopyright", page=1).json()
    #         pordvaluetotal = pordvalue["data"]["opusCopyright"]["total"]
    #         pordvalue_list = pordvalue["data"]["opusCopyright"]["items"]
    #         if 10 < pordvaluetotal:
    #             pordvaluetotal_num = round(pordvaluetotal // 10)
    #             pordvaluetotal_nums = round(pordvaluetotal / 10, 2)
    #             if pordvaluetotal_nums > pordvaluetotal_num:
    #                 pordvaluetotal_num = pordvaluetotal_num + 2
    #             else:
    #                 pordvaluetotal_num = pordvaluetotal_num + 1
    #             for pordvaluetotal_page in range(2, pordvaluetotal_num):
    #                 time.sleep(1.2)
    #                 forpoedvalue = get_company_prod_api.getEntSectionInfo(pid_value["pid"], section="IPR",
    #                                                                       label="opusCopyright",
    #                                                                       page=pordvaluetotal_page).json()
    #                 pordvalue_list.extend(forpoedvalue["data"]["opusCopyright"]["items"])
    #         if pordvalue_list != testvalue_list:
    #             print(pid_value, "该企业生产数据和测试不一致")
    #
    # @pytest.mark.parametrize('pid',
    #                          Excel_Files(file_name="作品.xlsx", sheel="Sheet1").open_file_rows("pid"))
    # # @pytest.mark.parametrize('pid',
    # #                          ["366c561d4ac0a57fefa1f56bce277ce7"])
    # def test_WorksCopyrightHive_ES(self, pid, ES):
    #     ES_value = ES.get(index="company_info_prod", id=pid)["_source"]
    #     time.sleep(1)
    #     testvalue = get_company_api.getEntSectionInfo(pid, section="IPR", label="opusCopyright",
    #                                                   page=1).json()
    #     testvaluetotal = testvalue["data"]["opusCopyright"]["total"]
    #     testvalue_list = testvalue["data"]["opusCopyright"]["items"]
    #     testvalue_list_dict = {}
    #     for testvalue_list_dict_softname in testvalue_list:
    #         testvalue_list_dict.update({testvalue_list_dict_softname["registNo"]: testvalue_list_dict_softname})
    #     if 10 < testvaluetotal:
    #         testvaluetotal_num = round(testvaluetotal // 10)
    #         testvaluetotal_nums = round(testvaluetotal / 10, 2)
    #         if testvaluetotal_nums > testvaluetotal_num:
    #             testvaluetotal_num = testvaluetotal_num + 2
    #         else:
    #             testvaluetotal_num = testvaluetotal_num + 1
    #         for testvaluetotal_page in range(2, testvaluetotal_num):
    #             time.sleep(1.2)
    #             fortestvalue = get_company_api.getEntSectionInfo(pid, section="IPR",
    #                                                              label="opusCopyright",
    #                                                              page=testvaluetotal_page).json()
    #             # testvalue_list.extend(fortestvalue["data"]["opusCopyright"]["items"])
    #             for fortestvalue_dict_softname in fortestvalue["data"]["opusCopyright"]["items"]:
    #                 testvalue_list_dict.update({fortestvalue_dict_softname["registNo"]: fortestvalue_dict_softname})
    #     if len(testvalue_list_dict.items()) != testvaluetotal:
    #         print("testvalue_list_dict数量计算错误")
    #     time.sleep(1)
    #     pordvalue = get_company_prod_api.getEntSectionInfo(pid, section="IPR",
    #                                                        label="opusCopyright", page=1).json()
    #     pordvaluetotal = pordvalue["data"]["opusCopyright"]["total"]
    #     pordvalue_list = pordvalue["data"]["opusCopyright"]["items"]
    #     pordvalue_list_dict = {}
    #     for pordvalue_list_dict_softname in pordvalue_list:
    #         pordvalue_list_dict.update({pordvalue_list_dict_softname["registNo"]: pordvalue_list_dict_softname})
    #     if 10 < pordvaluetotal:
    #         pordvaluetotal_num = round(pordvaluetotal // 10)
    #         pordvaluetotal_nums = round(pordvaluetotal / 10, 2)
    #         if pordvaluetotal_nums > pordvaluetotal_num:
    #             pordvaluetotal_num = pordvaluetotal_num + 2
    #         else:
    #             pordvaluetotal_num = pordvaluetotal_num + 1
    #         for pordvaluetotal_page in range(2, pordvaluetotal_num):
    #             time.sleep(1.2)
    #             forpoedvalue = get_company_prod_api.getEntSectionInfo(pid, section="IPR",
    #                                                                   label="opusCopyright",
    #                                                                   page=pordvaluetotal_page).json()
    #             # pordvalue_list.extend(forpoedvalue["data"]["opusCopyright"]["items"])
    #             for forpoedvalue_list_dict_softname in forpoedvalue["data"]["opusCopyright"]["items"]:
    #                 pordvalue_list_dict.update(
    #                     {forpoedvalue_list_dict_softname["registNo"]: forpoedvalue_list_dict_softname})
    #     if len(pordvalue_list_dict.items()) != pordvaluetotal:
    #         print("pordvalue_list_dict数量计算错误")
    #     if pordvalue_list_dict != testvalue_list_dict:
    #         print(pid, "该企业生产数据和测试不一致")
    #         print(pordvalue_list_dict)
    #         print(testvalue_list_dict)
    #         print(set(testvalue_list_dict).difference(set(pordvalue_list_dict)))
    #     worksName_set = set()
    #     for worksName in testvalue_list:
    #         worksName_set.add(worksName["worksName"])
    #     worksName_list = list(worksName_set)
    #     # print(worksName_list)
    #     if testvalue_list:
    #         if ES_value["hasWorks"] is not True:
    #             print(pid, "有无错误")
    #             print(ES_value["hasWorks"])
    #         # assert ES_value["hasWorks"] is True
    #         if ES_value["worksCount"] != testvaluetotal:
    #             print(pid, "数量错误")
    #             print(ES_value["worksName"], '\n', len(ES_value["worksName"]))
    #             print(ES_value["worksCount"], testvaluetotal)
    #         # assert ES_value["worksCount"] == testvaluetotal
    #         if set(worksName_list).intersection(set(ES_value["worksName"])) is False or set(
    #                 ES_value["worksName"]).intersection(set(worksName_list)) is False:
    #             print(pid, "名称错误")
    #             print(worksName_list, '\n', ES_value["worksName"])
    #             print(len(worksName_list), len(ES_value["worksName"]))
    #         # assert worksName_list == ES_value["worksName"]
    #     else:
    #         assert "hasWorks" not in ES_value.keys() or ES_value["hasWorks"] is False
    #         assert ES_value["worksCount"] is None or "worksCount" not in ES_value.keys() or \
    #                ES_value["worksCount"] == 0
    #         assert "worksName" not in ES_value.keys() or ES_value["worksName"] == []



