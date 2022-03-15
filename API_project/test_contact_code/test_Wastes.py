# 联系方式相关case

import pytest
import time
from API_project.tools.Excelread import Excel_Files
from API_project.Configs.search_Api import search
from API_project.tools.install_Excel import install_Excel
file_name = time.strftime("%Y年%m月%d日%H时%M分")  # 实例化测试报告工作表名称
HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
# 渠道，抽测
@pytest.mark.parametrize('entName', Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置") .open_file_rows("entName"))  # 号码
@pytest.mark.parametrize('pid', Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置") .open_file_rows("pid"))  # 号码
def test_ES_prod_a(self, pid, entName, ES):  # 联系方式维度测试
    op_name = Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置") .open_file_rows("name")
    op_vlue = Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置") .open_file_rows("value")
    install_files = install_Excel(file_name="联系方式渠道抽测", file_title_name=file_name)  # 实例化测试报告文件
    row_sum = install_files.read_sum() + 1
    if row_sum == 2 and install_files.read_one_value() is None:
        install_files.install(row=1, column=1, value='keyword')  # 写入表头
        install_files.install(row=1, column=2, value='pid')  # 写入表头
        install_files.install(row=1, column=3, value='entname')  # 写入表头
        install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        install_files.install(row=1, column=5, value='code')  # 写入表头
    es_result = ES.get(index="company_info_prod", id=pid)['_source']
    details_response = search(HOST).skb_contacts_num(id=pid, module='advance_search_detail')
    details_response_contacts = details_response.json()['data']['contacts']
    details_response_contactNum = details_response.json()['data']['contactNum']
    details_response.close()
    mobilePhone_list = []
    mobilePhonelist = []
    mobilePhonelist = set(mobilePhonelist)
    fixedPhone_list = []
    fixedPhonelist = []
    fixedPhonelist = set(fixedPhonelist)
    email_list = []
    contactSource = []
    contactSource = set(contactSource)
    if details_response_contacts:
        details_response_contacts_value = details_response_contacts
    elif details_response_contacts == [] and details_response_contactNum != 0:
        detail_response = search(HOST).skb_contacts(id=pid, entName=entName,
                                                    module='advance_search_detail')
        detail_response_contacts = detail_response.json()['data']['contacts']
        detail_response.close()
        details_response_contacts_value = detail_response_contacts
    else:
        details_response_contacts_value = []
    if details_response_contacts_value:
        for details_response_value in details_response_contacts_value:
            if details_response_value['type'] == 1:
                mobilePhone_list.append(details_response_value['content'])
                for sourceName in details_response_value['sources']:
                    if sourceName["sourceName"] == "仪表仪器交易网":
                        sourceName_value = "仪表仪器交易"
                    else:
                        sourceName_value = sourceName["sourceName"]
                    try:
                        ind = op_name[op_vlue.index(sourceName_value)]
                    except:
                        ind = None
                    if ind is not None:
                        mobilePhonelist.add(int(ind))
                        contactSource.add(int(ind))
            elif details_response_value['type'] == 2:
                fixedPhone_list.append(details_response_value['content'])
                for sourceName in details_response_value['sources']:
                    if sourceName["sourceName"] == "仪表仪器交易网":
                        sourceName_value = "仪表仪器交易"
                    else:
                        sourceName_value = sourceName["sourceName"]
                    try:
                        ind = op_name[op_vlue.index(sourceName_value)]
                    except:
                        ind = None
                    if ind is not None:
                        fixedPhonelist.add(int(ind))
                        contactSource.add(int(ind))
            elif details_response_value['type'] == 4:
                email_list.append(details_response_value['content'])
                for sourceName in details_response_value['sources']:
                    if sourceName["sourceName"] == "仪表仪器交易网":
                        sourceName_value = "仪表仪器交易"
                    else:
                        sourceName_value = sourceName["sourceName"]
                    try:
                        ind = op_name[op_vlue.index(sourceName_value)]
                    except:
                        ind = None
                    if ind is not None:
                        contactSource.add(int(ind))
            else:
                for sourceName in details_response_value['sources']:
                    if sourceName["sourceName"] == "仪表仪器交易网":
                        sourceName_value = "仪表仪器交易"
                    else:
                        sourceName_value = sourceName["sourceName"]
                    try:
                        ind = op_name[op_vlue.index(sourceName_value)]
                    except:
                        ind = None
                    if ind is not None:
                        contactSource.add(int(ind))
        eSn_list = set(mobilePhone_list).difference(set(es_result["mobilePhone"]))
        eSnf_list = set(fixedPhone_list).difference(set(es_result["fixedPhone"]))
        ESn_list = set(email_list).difference(set(es_result["email"]))
        ESm_list = set(es_result["mobilePhone"]).difference(set(mobilePhone_list))
        ESf_list = set(es_result["fixedPhone"]).difference(set(fixedPhone_list))
        ESe_list = set(es_result["email"]).difference(set(email_list))
        mobilePhonelist_re = set(mobilePhonelist).difference(set(es_result["mobileSource"]))
        fixedPhonelist_re = set(fixedPhonelist).difference(set(es_result["fixedSource"]))
        contactSource_re = set(contactSource).difference(set(es_result["contactSource"]))
        if len(list(eSn_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES没有详情页有，手机')  #
            install_files.install(row=row_sum, column=5, value=str(eSn_list))  # 写入表头
            row_sum = row_sum + 1
        if len(list(eSnf_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES没有详情页有，固话')  #
            install_files.install(row=row_sum, column=5, value=str(eSnf_list))  # 写入表头
            row_sum = row_sum + 1
        if len(list(ESn_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES没有详情页有，邮箱')  #
            install_files.install(row=row_sum, column=5, value=str(ESn_list))  # 写入表头
            row_sum = row_sum + 1
        if len(list(ESm_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES有详情页没有，手机')  #
            install_files.install(row=row_sum, column=5, value=str(ESm_list))  # 写入表头
            row_sum = row_sum + 1
        if len(list(ESf_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES有详情页没有，固话')  #
            install_files.install(row=row_sum, column=5, value=str(ESf_list))  # 写入表头
            row_sum = row_sum + 1
        if len(list(ESe_list)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES有详情页没有，邮箱')  #
            install_files.install(row=row_sum, column=5, value=str(ESe_list))  # 写入表头
        if len(list(mobilePhonelist_re)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='ES详情页有，手机号渠道')  #
            install_files.install(row=row_sum, column=5, value=str(mobilePhonelist_re))  # 写入表头
        if len(list(fixedPhonelist_re)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='详情页有，固话渠道')  #
            install_files.install(row=row_sum, column=5, value=str(fixedPhonelist_re))  # 写入表头
        if len(list(contactSource_re)) != 0:
            install_files.install(row=row_sum, column=2, value=pid)  # 写入表头
            install_files.install(row=row_sum, column=3, value=entName)  # 写入表头
            install_files.install(row=row_sum, column=4, value='详情页有,联系方式渠道')  #
            install_files.install(row=row_sum, column=5, value=str(contactSource_re))  # 写入表头
        assert len(list(ESe_list)) == 0 and len(list(ESf_list)) == 0 and len(list(ESm_list)) == 0 and len(
            list(ESn_list)) == 0 and len(list(eSnf_list)) == 0 and len(list(eSn_list)) == 0 and len(
            list(mobilePhonelist_re)) == 0 and len(list(fixedPhonelist_re)) == 0 and len(list(contactSource_re)) == 0