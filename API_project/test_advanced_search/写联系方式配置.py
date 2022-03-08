# 联系方式相关case
# from collections import Counter  # 导入表格统计模块
from API_project.Configs.Configuration import configuration_file
from API_project.tools.install_Excel import install_Excel
HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_list = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_list + staticConfig_value['sub']
print(staticConfig_list)
install_files = install_Excel(file_name="联系方式渠道配置test", file_title_name="联系方式渠道配置")  # 实例化测试报告文件
if install_files.read_sum() == 1 and install_files.read_one_value() is None:
    install_files.install(row=1, column=1, value='name')
    install_files.install(row=1, column=2, value='value')
    install_files.install(row=1, column=3, value='dbName')
for i in staticConfig_list:
    row_sum = install_files.read_sum() + 1
    install_files.install(row=row_sum, column=1, value=i['name'])
    install_files.install(row=row_sum, column=2, value=i['value'])
    install_files.install(row=row_sum, column=3, value=i['dbName'])
