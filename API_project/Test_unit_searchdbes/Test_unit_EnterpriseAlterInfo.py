from API_project.Configs.Config_Database import DataBase_All, ES_All
from API_project.Configs.Config_Api import Skb_Search_Api
# DataBase = DataBase_All().to_pymongo()
# db = DataBase()

search = Skb_Search_Api(host="xlcrm")

class Test_EnterpriseAlterInfo:
    def test01(self, ES_new, connect_db):
        db = connect_db
        datav = db.enterprise.CourtAnnouncementNew.find({})
        db.close()
        datalist = db.enterprise.EnterpriseAlterInfo.find({}).limit(2).skip(0)
        datalist_value = {}
        pid_list = []
        for data_value in datalist:
            datalist_value.update({f"{data_value['PID']}": data_value})
            pid_list.append(data_value['PID'])
            print(data_value)
        print(datav.count())
        for i in datav[:11:]:
            print(i)
        # print(DataBase("close"))
        # print(pid_list)
        # es = ES_new()
        # print(es)
        # print(es.get(index="company_info_prod", id=pid_list[0]))
        # es.close()
if __name__ == "__main__":
    Test_EnterpriseAlterInfo().test01()