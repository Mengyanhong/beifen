from API_project.Configs.Config_Info import Api_Config_File
from API_project.tools.Excelread import Excel_Files
from pprint import pprint

HOST = 'test'  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
shopCategory = Api_Config_File(HOST).shopCategory()  # 实例化店铺分类并返回配置信息
category_list = []
for i in shopCategory['shopCategory']:
    for j in i["sub"]:
        category_list.append({"categoryL1_value": i["value"], "categoryL2_value": j["value"]})
excel_file = Excel_Files(file_name="店铺数据准备.xlsx", sheel="店铺分类")
file = excel_file.open_case4(request_name="一级分类", response_name="二级分类")
# print(file)
if len(category_list) != len(file):
    print(f"配置数量不相等Excel配置数为{len(file)},应用配置数为{len(category_list)}")
    if len(category_list) < len(file):
        for file_value in file:
            if file_value not in category_list:
                print(f"应用内缺少筛选项{file_value}")
    elif len(category_list) > len(file):
        for categ_value in category_list:
            if categ_value not in file:
                print(f"应用内多出筛选项{categ_value}")
sum_case_ = None
for sum_case in range(len(category_list)):
    if category_list[sum_case] != file[sum_case]:
        sum_case_ = False
        print("配置顺序不相等Excel配置", file[sum_case], "\n应用配置", category_list[sum_case])
if sum_case_ is False:
    print("Excel配置", file)
    print("应用  配置", category_list)
