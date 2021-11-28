import yaml
import pprint
def get_yaml_data(fileDir):
    reslist = [] #存放结果[（请求1，期望响应1），（请求2，期望响应2）]
    #1- 读取文件操作---从磁盘读取到内存
    fo = open(fileDir,'r',encoding="utf-8")# file_obiect
    #2- 使用yaml方法获取数据
    res = yaml.load(fo,Loader=yaml.FullLoader)
    fo.close()
    # info = res[0]#自己封装基类可以使用
    del res[0]
    for one in res:
        reslist.append((one['data'],one['resp']))
    return reslist
if __name__ == '__main__':
    res = get_yaml_data('../Data/staging_se_files.yaml')
    print(res[0][0]["file_name"])
    # for one in res:
    #     print(one)
    # print(res)

