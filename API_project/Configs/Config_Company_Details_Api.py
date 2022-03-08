
from API_project.Configs.Configuration import User_Config
import requests


class getCompany_details(User_Config):
    # def __init__(self, test):
    #     self.user = User_Config(test)

    def getCompanyBase(self, pid):  # 请求详情页信息
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        params = {'id': f'{pid}',
                  'countSection': 1,
                  'market_source': 'advance_search_list',
                  'version': 'v3',
                  'search_result_size': 10,
                  'search_result_page': 1,
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb())
        return response

    def getEntSectionInfo(self, pid, section, label=None, page=None):  # 企业详情一级菜单
        '''
        :param pid: #企业pid
        :param section: #菜单选择，Development：企业发展,RiskInfo:风险信息, ManageInfo:经营情况
        :param label: #数据维度，TradeShow：参展
        :param page: #翻页页码
        :return:
        '''

        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        if page is not None:
            params = {'id': f'{pid}',
                      'label': label,
                      'page': page,
                      'section': section,
                      'version': 'v2'
                      }
        else:
            params = {'id': f'{pid}',
                      'section': section,
                      'version': 'v2'
                      }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getAnnualReportDetail(self, annualReportId):  # 年报详情获取
        '''
        :param annualReportId: #年报id
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getAnnualReportDetail?'
        params = {'annualReportId': annualReportId,
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_ManageInfo(self, pid, sourceName):  # 经营情况_招聘平台筛选
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'ManageInfo',
                  'label': 'RecruitmentDetail',
                  'sourceName': sourceName,
                  'version': 'v2',
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_IPR(self, pid, templateSuppiler):  # 知识产权_建站方筛选
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'IPR',
                  'label': 'WebsiteInformation',
                  'templateSuppiler': templateSuppiler,
                  'version': 'v2',
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getWebsiteInfo(self, _id):  # 知识产权_建站方_详情
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getWebsiteInfo?'
        params = {'id': f'{_id}'}
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_RiskInfo_subset(self, pid, page=1, subset='EndBookInfo'):  # 风险信息子菜单_详情
        '''

        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #风险信息下的子菜单，EndBookInfo：终本案件，Executor：被执行人
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'section': 'RiskInfo',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_InterpersonalRelations(self, pid):  # 员工人脉_详情
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'section': 'InterpersonalRelations',
                  'version': 'v2',
                  'pageSize': 20
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_InterpersonalRelations_subset(self, pid, page=1, subset='Maimai'):  # 员工人脉子菜单_详情
        '''
        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #员工人脉下的子菜单，Maimai：脉脉，LinkedinUserInfo：领英，PersonalMicroblog：微博
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'pageSize': 20,
            'section': 'InterpersonalRelations',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response
