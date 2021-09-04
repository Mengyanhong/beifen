# -*- coding: utf-8 -*-
# 条件测试

import openpyxl
from adv_search.config_API import configuration_file

host = 'test'

conditionGroups = configuration_file(host).conditionGroups()
level1_num_api=len(conditionGroups)


data=openpyxl.load_workbook('条件及条件值.xlsx')
sheet_condition=data['条件']

for i in range(2,30):
    if sheet_condition['A'+str(i)].value==None:
        level1_num_request=i-2
        break

for i in range(2, 300):
    if sheet_condition['D' + str(i)].value == None:
        level2_num_request = i - 2
        break

class TestConditionGroups():
    def test_level(self):
        level2_sum = 0

        #判断一级的数量和值
        assert level1_num_api==level1_num_request
        for i in range(level1_num_api):
            assert conditionGroups[i]['name']==sheet_condition['A'+str(i+2)].value

            #判断二级的数量
            level2_num_api=len(conditionGroups[i]['conditions'])
            level2_num_request = 0
            for a in range(2,1000):
                if sheet_condition['C'+str(a+level2_sum)].value==conditionGroups[i]['name']:
                    level2_num_request+=1
                else:
                    level2_sum+=level2_num_request
                    break
            assert level2_num_api==level2_num_request

            # 判断二级的值
            for j in range(level2_num_api):
                assert conditionGroups[i]['conditions'][j]['label']==sheet_condition['D'+str(j+2+level2_sum-level2_num_api)].value




















# conditionGroups
# [{'name': '常用', 'conditions': [{'name': 'entName', 'label': '企业名称', 'isNew': False, 'description': '', 'path': ''},
# {'name': 'entStatus', 'label': '营业状态', 'isNew': False, 'description': '', 'path': ''},
# {'name': 'area', 'label': '所在地区', 'isNew': False, 'description': '', 'path': ''}, {'name': 'industry', 'label': '所属行业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'opScope', 'label': '经营范围', 'isNew': False, 'description': '', 'path': ''}, {'name': 'latest6MonthJobName', 'label': '前6个月招聘职位', 'isNew': False, 'description': '以当前时间往前计算，6个月内的招聘职位', 'path': ''}, {'name': 'hasMobile', 'label': '有无手机', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasIcp', 'label': '有无icp备案', 'isNew': False, 'description': '', 'path': ''}]}, {'name': '基本信息', 'conditions': [{'name': 'entName', 'label': '企业名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'opScope', 'label': '经营范围', 'isNew': False, 'description': '', 'path': ''}, {'name': 'baikeInfo', 'label': '企业百科', 'isNew': False, 'description': '', 'path': ''}, {'name': 'b2bProduct', 'label': '主营产品', 'isNew': False, 'description': '', 'path': ''}, {'name': 'contactAddress', 'label': '通讯地址', 'isNew': False, 'description': '', 'path': ''}, {'name': 'entStatus', 'label': '营业状态', 'isNew': False, 'description': '', 'path': ''}, {'name': 'area', 'label': '所在地区', 'isNew': False, 'description': '', 'path': ''}, {'name': 'industry', 'label': '所属行业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'regCapUnify', 'label': '注册资本', 'isNew': False, 'description': '', 'path': ''}, {'name': 'esDate', 'label': '成立年限', 'isNew': False, 'description': '', 'path': ''}, {'name': 'entTypeDetail', 'label': '企业类型', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasAnnu', 'label': '有无企业年报', 'isNew': False, 'description': '', 'path': ''}, {'name': 'employees', 'label': '参保人数', 'isNew': False, 'description': '', 'path': ''}, {'name': 'branchCount', 'label': '分支机构', 'isNew': False, 'description': '', 'path': ''}, {'name': 'latestLegalChangeDate', 'label': '最新法人/高管变更日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'latestAddressChangeDate', 'label': '最新地址变更日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasAaumChange', 'label': '有无工商变更', 'isNew': True, 'description': '', 'path': ''}, {'name': 'enterpriseAlterInfo.alterCategory', 'label': '工商变更类型', 'isNew': True, 'description': '', 'path': 'enterpriseAlterInfo'}, {'name': 'enterpriseAlterInfo.alterDate', 'label': '工商变更日期', 'isNew': True, 'description': '', 'path': 'enterpriseAlterInfo'}], 'isNew2': True}, {'name': '联系方式', 'conditions': [{'name': 'hasMobile', 'label': '有无手机', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasFixed', 'label': '有无固话', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasEmail', 'label': '有无邮箱', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasQq', 'label': '有无QQ', 'isNew': False, 'description': '', 'path': ''}, {'name': 'contactSource', 'label': '联系方式渠道', 'isNew': False, 'description': '', 'path': ''}, {'name': 'mobileSource', 'label': '手机号渠道', 'isNew': False, 'description': '', 'path': ''}, {'name': 'fixedSource', 'label': '固话渠道', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isAgency', 'label': '有无疑似代理记账号码', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasNonAgency', 'label': '有无非疑似代理记账号码', 'isNew': False, 'description': '', 'path': ''}, {'name': 'nonAgencyType', 'label': '非疑似代理记账号码类型', 'isNew': False, 'description': '', 'path': ''}], 'isNew2': False}, {'name': '企业发展', 'conditions': [{'name': 'hasCap', 'label': '有无融资历史', 'isNew': False, 'description': '', 'path': ''}, {'name': 'lastCap', 'label': '当前融资轮次', 'isNew': False, 'description': '', 'path': ''}, {'name': 'capCount', 'label': '融资次数', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isChineseTop500', 'label': '是否500强企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isUnicorn', 'label': '是否独角兽企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isGazelle', 'label': '是否瞪羚企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isListed', 'label': '是否上市企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isTopTenIndustry', 'label': '是否行业内十强企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'guild', 'label': '行业协会', 'isNew': False, 'description': '', 'path': ''}], 'isNew2': False}, {'name': '经营情况', 'conditions': [{'name': 'hasAdminLicense', 'label': '有无行政许可', 'isNew': False, 'description': '', 'path': ''}, {'name': 'licenseOffice', 'label': '许可机关', 'isNew': False, 'description': '', 'path': 'adminLicense'}, {'name': 'licenseContent', 'label': '许可内容', 'isNew': False, 'description': '', 'path': 'adminLicense'}, {'name': 'licenseCount', 'label': '行政许可数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'adminLicense.createDate', 'label': '行政许可发证日期', 'isNew': False, 'description': '', 'path': 'adminLicense'}, {'name': 'adminLicense.expireDate', 'label': '行政许可到期时间', 'isNew': False, 'description': '', 'path': 'adminLicense'}, {'name': 'hasInvestment', 'label': '有无对外投资', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasAnnualInvestment', 'label': '有无年报对外投资', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isGeneralTaxpayer', 'label': '是否为一般纳税人', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasATaxCredit', 'label': '是否为A级纳税人', 'isNew': False, 'description': '', 'path': ''}, {'name': 'ATaxAwardedYear', 'label': 'A级纳税人评价年份', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasTender', 'label': '有无招投标', 'isNew': False, 'description': '', 'path': ''}, {'name': 'tenderName', 'label': '招投标项目描述', 'isNew': False, 'description': '', 'path': 'tender'}, {'name': 'tender.pubDate', 'label': '招投标发布时间', 'isNew': False, 'description': '', 'path': 'tender'}, {'name': 'tenderType', 'label': '招投标公告类型', 'isNew': True, 'description': '', 'path': 'tender'}, {'name': 'hasImportAndExportCredit', 'label': '有无进出口信用', 'isNew': False, 'description': '', 'path': ''}, {'name': 'cusCreditLevel', 'label': '海关信用等级', 'isNew': False, 'description': '', 'path': ''}, {'name': 'cusOpCategory', 'label': '海关登记经营类别', 'isNew': False, 'description': '', 'path': ''}, {'name': 'cusIndusCategory', 'label': '海关登记行业', 'isNew': True, 'description': '', 'path': ''}, {'name': 'registSpecialty', 'label': '注册人员专业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'registCertType', 'label': '注册人员类别', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasTradeShow', 'label': '有无参展', 'isNew': False, 'description': '', 'path': ''}, {'name': 'tradeShowStartDate', 'label': '展会开始时间', 'isNew': False, 'description': '', 'path': ''}, {'name': 'b2bPopularizePlatform', 'label': 'B2B推广平台', 'isNew': False, 'description': '', 'path': ''}], 'isNew2': True}, {'name': '招聘信息', 'conditions': [{'name': 'hasRecruit', 'label': '有无招聘', 'isNew': False, 'description': '', 'path': ''}, {'name': 'jobName', 'label': '招聘职位', 'isNew': True, 'description': '', 'path': ''}, {'name': 'latest6MonthJobName', 'label': '前6个月招聘职位', 'isNew': False, 'description': '以当前时间往前计算，6个月内的招聘职位', 'path': ''}, {'name': 'latest3MonthJobName', 'label': '前3个月招聘职位', 'isNew': True, 'description': '', 'path': ''}, {'name': 'latest1MonthJobName', 'label': '前1个月招聘职位', 'isNew': True, 'description': '', 'path': ''}, {'name': 'recruitPlatform', 'label': '招聘平台', 'isNew': False, 'description': '', 'path': 'recruitment'}, {'name': 'recruitAvgSalary', 'label': '企业平均薪资', 'isNew': True, 'description': '', 'path': ''}, {'name': 'recruitment.address', 'label': '招聘详细地址', 'isNew': True, 'description': '', 'path': ''}, {'name': 'recruitment.jobDetail', 'label': '职位描述', 'isNew': False, 'description': '', 'path': 'recruitment'}, {'name': 'recruitment.entWelfare', 'label': '企业福利', 'isNew': False, 'description': '', 'path': ''}, {'name': 'jobCount', 'label': '当前招聘职位数', 'isNew': False, 'description': '', 'path': ''}, {'name': 'recruitAmountTotal', 'label': '当前招聘总人数', 'isNew': True, 'description': '', 'path': ''}, {'name': 'latest3MonthJobCount', 'label': '前3个月招聘职位数', 'isNew': False, 'description': '以当前时间往前计算，各个平台上的3个月内职位相加，去重计算', 'path': ''}, {'name': 'latest3MonthRecruitAmount', 'label': '前3个月招聘总人数', 'isNew': True, 'description': '', 'path': ''}, {'name': 'recruitAvgFrequency', 'label': '职位平均更新频率', 'isNew': True, 'description': '', 'path': ''}, {'name': 'recruitCategory', 'label': '职位类型', 'isNew': False, 'description': '', 'path': ''}, {'name': 'recruitment.releaseDate', 'label': '职位发布时间', 'isNew': False, 'description': '', 'path': 'recruitment'}], 'isNew2': True}, {'name': '网络推广', 'conditions': [{'name': 'hasSem', 'label': '有无推广', 'isNew': False, 'description': '', 'path': ''}, {'name': 'semKeyword', 'label': '推广关键词', 'isNew': False, 'description': '', 'path': 'semPromo'}, {'name': 'latest1MonthSemKeyword', 'label': '前1个月推广关键词', 'isNew': False, 'description': '以当前时间往前计算，1个月内推广的关键词', 'path': ''}, {'name': 'semTitle', 'label': '推广文案', 'isNew': False, 'description': '', 'path': ''}, {'name': 'semPlatform', 'label': '推广平台', 'isNew': False, 'description': '', 'path': 'semPromo'}, {'name': 'semDate', 'label': '最后推广时间', 'isNew': False, 'description': '', 'path': ''}, {'name': 'semKeywordCount', 'label': '推广关键词数', 'isNew': True, 'description': '', 'path': ''}, {'name': 'semUrlCount', 'label': '推广链接数', 'isNew': True, 'description': '', 'path': ''}], 'isNew2': True}, {'name': '产品信息', 'conditions': [{'name': 'hasWechat', 'label': '有无公众号', 'isNew': False, 'description': '', 'path': ''}, {'name': 'wechatName', 'label': '公众号名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'wechatCount', 'label': '公众号数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasBlog', 'label': '有无机构微博', 'isNew': False, 'description': '', 'path': ''}, {'name': 'blogName', 'label': '机构微博名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'weiboCount', 'label': '机构微博数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasApp', 'label': '有无移动应用', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appName', 'label': '移动应用名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appInfo', 'label': '移动应用描述', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appCategory', 'label': '移动应用分类', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appPlatform', 'label': '移动应用上架平台', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appCount', 'label': '移动应用数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appDownloadCount', 'label': '移动应用下载总量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appAvgScore', 'label': '移动应用平均评分', 'isNew': False, 'description': '', 'path': ''}, {'name': 'appLastReleaseDate', 'label': '移动应用最近更新时间', 'isNew': False, 'description': '', 'path': ''}, {'name': 'eShopCount', 'label': '电商店铺数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'ecomShopPlatform', 'label': '电商上架平台', 'isNew': False, 'description': '', 'path': ''}, {'name': 'eProductCategory', 'label': '电商产品分类', 'isNew': True, 'description': '', 'path': ''}, {'name': 'ecomShopName', 'label': '电商店铺名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'eMainBrand', 'label': '电商主营品牌', 'isNew': True, 'description': '', 'path': ''}, {'name': 'eShopCreateDate', 'label': '电商店铺创建时间', 'isNew': True, 'description': '', 'path': ''}, {'name': 'eShopAvgScore', 'label': '电商店铺平均分', 'isNew': True, 'description': '', 'path': ''}, {'name': 'eHasProduct', 'label': '有无商品', 'isNew': True, 'description': '', 'path': ''}, {'name': 'eProductCount', 'label': '商品数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'eProductName', 'label': '商品名称', 'isNew': True, 'description': '', 'path': ''}, {'name': 'hasBrand', 'label': '有无品牌信息', 'isNew': True, 'description': '', 'path': ''}, {'name': 'brandCount', 'label': '品牌数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'brandName', 'label': '品牌名称', 'isNew': True, 'description': '', 'path': ''}], 'isNew2': True}, {'name': '网站信息', 'conditions': [{'name': 'hasIcp', 'label': '有无icp备案', 'isNew': False, 'description': '', 'path': ''}, {'name': 'icpCount', 'label': 'icp备案数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'seoKeyword', 'label': '网站关键词', 'isNew': False, 'description': '', 'path': ''}, {'name': 'seoInfo', 'label': '网站描述', 'isNew': False, 'description': '', 'path': ''}, {'name': 'baiduRank', 'label': '百度权重PC端', 'isNew': False, 'description': '', 'path': ''}, {'name': 'qihu360Rank', 'label': '360权重PC端', 'isNew': False, 'description': '', 'path': ''}, {'name': 'sougouRank', 'label': '搜狗权重PC端', 'isNew': False, 'description': '', 'path': ''}, {'name': 'baiduCover', 'label': '百度总收录量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'qihu360Cover', 'label': '360总收录量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'sougouCover', 'label': '搜狗总收录量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'domainAge', 'label': '域名年龄', 'isNew': False, 'description': '', 'path': ''}, {'name': 'domainExpireDate', 'label': '域名到期时间', 'isNew': False, 'description': '', 'path': ''}, {'name': 'deadLinkSum', 'label': '死链数', 'isNew': False, 'description': '', 'path': ''}, {'name': 'illegalLinkSum', 'label': '非法链接数', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasSsl', 'label': '有无HTTPS证书', 'isNew': False, 'description': '', 'path': ''}, {'name': 'webSecureDesc', 'label': '网站安全性', 'isNew': False, 'description': '', 'path': ''}, {'name': 'webFeature', 'label': '网站功能', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasFlashModule', 'label': '有无flash', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasOnlineChat', 'label': '有无在线沟通工具', 'isNew': False, 'description': '', 'path': ''}, {'name': 'onlineChat', 'label': '在线沟通工具类型', 'isNew': False, 'description': '', 'path': ''}, {'name': 'templateSuppiler', 'label': '建站方', 'isNew': False, 'description': '', 'path': ''}, {'name': 'devLanguage', 'label': '网站技术语言', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isRespTech', 'label': '是否响应式技术网站', 'isNew': False, 'description': '', 'path': ''}, {'name': 'serverPhysicNode', 'label': 'IP物理位置', 'isNew': False, 'description': '', 'path': ''}, {'name': 'serviceNode', 'label': 'IP运营节点', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasMobileSite', 'label': '有无手机端网站', 'isNew': False, 'description': '', 'path': ''}, {'name': 'websiteSpeed', 'label': '平均访问速度', 'isNew': False, 'description': '', 'path': ''}, {'name': 'webLastChangeDate', 'label': '网站结构更新时间', 'isNew': False, 'description': '', 'path': ''}, {'name': 'domainRecordAge', 'label': '备案年龄', 'isNew': False, 'description': '', 'path': ''}, {'name': 'baiduPcPage', 'label': '关键词百度网页端排名', 'isNew': False, 'description': '', 'path': ''}, {'name': 'baiduH5Page', 'label': '关键词百度移动端排名', 'isNew': False, 'description': '', 'path': ''}, {'name': 'companyGroup', 'label': '网站群', 'isNew': False, 'description': '', 'path': ''}], 'isNew2': False}, {'name': '资质证书', 'conditions': [{'name': 'hasCert', 'label': '有无证书', 'isNew': False, 'description': '', 'path': ''}, {'name': 'certL2Count', 'label': '证书数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'certL2CountThisYear', 'label': '本年度获证数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'initCertDate', 'label': '初次获证日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'lastCertDate', 'label': '最近获证日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'certificate.endDate', 'label': '证书截止日期', 'isNew': False, 'description': '', 'path': 'certificate'}, {'name': 'latest3MonthCertL2Type', 'label': '未来3个月内截止证书类别', 'isNew': False, 'description': '以当前时间往后计算，3个月内截止时间的证书', 'path': ''}, {'name': 'latest6MonthCertL2Type', 'label': '未来6个月内截止证书类别', 'isNew': False, 'description': '以当前时间往后计算，6个月内截止时间的证书', 'path': ''}, {'name': 'certType', 'label': '涵盖证书类型', 'isNew': False, 'description': '', 'path': 'certificate'}, {'name': 'hasArchitCert', 'label': '有无建筑资质', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isHighTech', 'label': '是否高新企业', 'isNew': False, 'description': '', 'path': ''}, {'name': 'certL2Name', 'label': '证书名称', 'isNew': False, 'description': '', 'path': 'certificate'}, {'name': 'certificate.certOrgName', 'label': '发证机构', 'isNew': False, 'description': '', 'path': 'certificate'}], 'isNew2': False}, {'name': '知识产权', 'conditions': [{'name': 'hasPatent', 'label': '有无专利', 'isNew': False, 'description': '', 'path': ''}, {'name': 'patentCount', 'label': '专利数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'patentType', 'label': '涵盖专利类别', 'isNew': False, 'description': '', 'path': 'patent'}, {'name': 'patentName', 'label': '专利名称', 'isNew': False, 'description': '', 'path': 'patent'}, {'name': 'patentApplyDate', 'label': '专利申请日期', 'isNew': False, 'description': '', 'path': 'patent'}, {'name': 'patentApplyPubDate', 'label': '专利公开（公告）日期', 'isNew': False, 'description': '', 'path': 'patent'}, {'name': 'applyPatentCountYear', 'label': '最近一年申请专利数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'pubPatentCountYear', 'label': '最近一年公开（公告）专利数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'hasTrademark', 'label': '有无商标', 'isNew': False, 'description': '', 'path': ''}, {'name': 'trademarkName', 'label': '商标名称', 'isNew': False, 'description': '', 'path': 'trademark'}, {'name': 'trademarkType', 'label': '涵盖商标类别', 'isNew': False, 'description': '', 'path': 'trademark'}, {'name': 'tradeMarkValidCount', 'label': '有效状态商标数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'tradeMarkInvalidCount', 'label': '无效状态商标数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'trademarkApplyDate', 'label': '商标申请日期', 'isNew': False, 'description': '', 'path': 'trademark'}, {'name': 'trademarkUseRightDateEnd', 'label': '商标专用权结束日期', 'isNew': False, 'description': '', 'path': 'trademark'}, {'name': 'hasSoftware', 'label': '有无软著', 'isNew': False, 'description': '', 'path': ''}, {'name': 'softwareCount', 'label': '软著数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'softwareProductName', 'label': '软著名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasWorks', 'label': '有无作品著作权', 'isNew': False, 'description': '', 'path': ''}, {'name': 'worksCount', 'label': '作品著作权数量', 'isNew': True, 'description': '', 'path': ''}, {'name': 'worksName', 'label': '作品名称', 'isNew': False, 'description': '', 'path': ''}, {'name': 'tradeMarkInventoryCategory', 'label': '商标商品服务', 'isNew': True, 'description': '', 'path': ''}], 'isNew2': True}, {'name': '风险信息', 'conditions': [{'name': 'hasAbnormal', 'label': '有无经营异常', 'isNew': False, 'description': '', 'path': ''}, {'name': 'isAbnormal', 'label': '当前是否被列入经营异常', 'isNew': False, 'description': '', 'path': ''}, {'name': 'abnormalCount', 'label': '经营异常数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'abnormalInReason', 'label': '当前列入经营异常原因', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hisAbnormalInReason', 'label': '历史列入经营异常原因', 'isNew': False, 'description': '', 'path': ''}, {'name': 'lastAbnormalInDate', 'label': '最近经营异常列入日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'lastAbnormalOutDate', 'label': '最近经营异常移出日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasPenalty', 'label': '有无行政处罚', 'isNew': False, 'description': '', 'path': ''}, {'name': 'penaltyCount', 'label': '行政处罚数量', 'isNew': False, 'description': '', 'path': ''}, {'name': 'lastPenDate', 'label': '最近行政处罚决定日期', 'isNew': False, 'description': '', 'path': ''}, {'name': 'hasDishonest', 'label': '有无失信被执行人', 'isNew': False, 'description': '', 'path': ''}, {'name': 'taxUnusualSum', 'label': '税务异常', 'isNew': True, 'description': '', 'path': ''}], 'isNew2': True}]
# class_dict
# {'常用': ['企业名称', '营业状态', '所在地区', '所属行业', '经营范围', '前6个月招聘职位', '有无手机', '有无icp备案'], '基本信息': ['企业名称', '经营范围', '企业百科', '主营产品', '通讯地址', '营业状态', '所在地区', '所属行业', '注册资本', '成立年限', '企业类型', '有无企业年报', '参保人数', '分支机构', '有无工商变更', '工商变更类型', '工商变更日期'], '联系方式': ['有无手机', '有无固话', '有无邮箱', '有无QQ', '联系方式渠道', '手机号渠道', '固话渠道', '有无疑似代理记账号码', '有无非疑似代理记账号码', '非疑似代理记账号码类型'], '企业发展': ['有无融资历史', '当前融资轮次', '融资次数', '是否500强企业', '是否独角兽企业', '是否瞪羚企业', '是否上市企业', '是否行业内十强企业', '行业协会'], '经营情况': ['有无行政许可', '许可机关', '许可内容', '行政许可数量', '行政许可发证日期', '行政许可到期时间', '有无对外投资', '有无年报对外投资', '是否为一般纳税人', '是否为A级纳税人', 'A级纳税人评价年份', '有无招投标', '招投标项目标题', '招投标发布时间', '招投标公告类型', '有无进出口信用', '海关信用等级', '海关登记经营类别', '海关登记行业', '注册人员专业', '注册人员类别', '有无参展', '展会开始时间', 'B2B推广平台'], '招聘信息': ['有无招聘', '招聘职位', '前6个月招聘职位', '前3个月招聘职位', '前1个月招聘职位', '招聘平台', '企业平均薪资', '招聘详细地址', '职位描述', '企业福利', '当前招聘职位数', '当前招聘总人数', '前3个月招聘职位数', '前3个月招聘总人数', '职位平均更新频率', '职位类型', '职位发布时间'], '网络推广': ['有无推广', '推广关键词', '近1个月推广关键词', '推广文案', '推广平台', '最后推广时间', '推广关键词数', '推广链接数'], '产品信息': ['有无公众号', '公众号名称', '公众号数量', '有无机构微博', '机构微博名称', '机构微博数量', '有无移动应用', '移动应用名称', '移动应用描述', '移动应用分类', '移动应用上架平台', '移动应用数量', '移动应用下载总量', '移动应用平均评分', '移动应用最近更新时间', '电商店铺数量', '电商上架平台', '电商产品分类', '电商店铺名称', '电商主营品牌', '电商店铺创建时间', '电商店铺平均分', '有无商品', '商品数量', '商品名称', '有无品牌信息', '品牌数量', '品牌名称'], '网站信息': ['有无icp备案', 'icp备案数量', '网站关键词', '网站描述', '百度权重PC端', '360权重PC端', '搜狗权重PC端', '百度总收录量', '360总收录量', '搜狗总收录量', '域名年龄', '域名到期时间', '死链数', '非法链接数', '有无HTTPS证书', '网站安全性', '网站功能', '有无flash', '有无在线沟通工具', '在线沟通工具类型', '建站方', '网站技术语言', '是否响应式技术网站', 'IP物理位置', 'IP运营节点', '有无手机端网站', '平均访问速度', '网站结构更新时间', '备案年龄', '关键词百度网页端排名', '关键词百度移动端排名', '网站群'], '资质证书': ['有无证书', '证书数量', '本年度获证数量', '初次获证日期', '最近获证日期', '证书截止日期', '未来3个月内截止证书类型', '未来6个月内截止证书类型', '涵盖证书类型', '有无建筑资质', '是否高新企业', '证书名称', '发证机构'], '知识产权': ['有无专利', '专利数量', '涵盖专利类别', '专利名称', '专利申请日期', '专利公开（公告）日期', '最近一年申请专利数量', '最近一年公开（公告）专利数量', '有无商标', '商标名称', '涵盖商标类别', '有效状态商标数量', '无效状态商标数量', '商标商品服务', '商标申请日期', '商标专用权结束日期', '有无软著', '软著数量', '软著名称', '有无作品著作权', '作品著作权数量', '作品名称'], '风险信息': ['有无经营异常', '当前是否被列入经营异常', '经营异常数量', '当前列入经营异常原因', '历史列入经营异常原因', '最近经营异常列入日期', '最近经营异常移出日期', '有无行政处罚', '行政处罚数量', '最近行政处罚决定日期', '有无失信被执行人', '税务异常']}
