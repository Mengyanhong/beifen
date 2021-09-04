import yaml
import pprint
def get_yaml_data(fileDir):
    reslist = [] #存放结果[（请求1，期望响应1），（请求2，期望响应2）]
    #1- 读取文件操作---从磁盘读取到内存
    fo = open(fileDir,'r',encoding="utf-8")# file_obiect文件目录及获取方式，r表示只读，encoding表示文件编码
    #2- 使用yaml方法获取数据
    res = yaml.load(fo,Loader=yaml.FullLoader)
    fo.close() #关闭文件加载方式
    info = res[0]#自己封装基类可以使用
    del res[0] #删除yaml文档说明
    for one in res:
        reslist.append((one['company'],one['data'],one['resp']))
    return reslist,info
if __name__ == '__main__':
    res = get_yaml_data('../data/login_case.yaml')
    # res = list(res)
    # res.pop()
    print(res[-1])
    # for one in res:
    #     print(one)
    # print(res)