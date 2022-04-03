# -*- coding: utf-8 -*-
# author：baoshan
# 带参数的函数装饰器


def say_hello(country):
    def wrapper(func):
        def deco(*args, **kwargs):
            if country == 'china':
                print('你好！')
            elif country == 'america':
                print('hello')
            else:
                return
            func(*args, **kwargs)
        return deco
    return wrapper


@say_hello('china')
def chinese():
    print('我来自中国。')


@say_hello('america')
def america():
    print('I am from America.')


# america()
# print('-'*20)
# chinese()

from functools import wraps #引用functools下的wraps把__name__,__doc__这些全部偷梁换柱
def deco(x,y):  #为装饰器传参
    def outer(func):    #为inner传func
        @wraps(func)    #这里wraps需要传func
        def inner(*args,**kwargs):  #为函数传参数
            res = func(*args, **kwargs)
            if x+y>5:   #参数来判断return 的结果
                return res+5
            else:
                return res+100
        return inner
    return outer

@deco(2,41)
def orgin_func(name):
    '''
    打印
    :return: 123
    '''
    print(name,'is 打印')
    return 123

# res=orgin_func('john')
# print(res)
# print(orgin_func.__name__)  #伪装了__name__,使orgin_func看起来就是自己,而不再是inner
# print(orgin_func.__doc__)


# 【add\add_fun函数的定义】
# def add_fun(x, y):
#     """
#     实现两个数相加、并返回合
#     """
#     return x + y
# def add(x, y):
#     """
#     实现两个数相加、并返回合
#     """
#     return x + y

# 【通过装饰器引导调用add_fun的用户去调用add】
def deprecated(fun, new_fun_name):
    """deprecated函数会返回一个叫inner的函数、inner函数会返回
    fun调用的结果，与直接调用fun得到值不同的是inner会先打印一行提示
    表明fun已经过时
    """
    def inner(x, y):
        print("{fun.__name__} 函数已经过时 请使用{new_fun_name}".format(fun=fun, new_fun_name=new_fun_name))
        return fun(x, y)
    return inner


def add_fun(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


add_fun = deprecated(add_fun, 'add')


def add(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


if __name__ == "__main__":
    print(add_fun(1, 1))

# 【难道为装饰器增加参数就这么的简单】
# 仔细的你可能已经发现了、我们在上面的代码里并没有用装饰器的语法糖衣、而是通过函数调用的方式来包装的add_fun方法
# add_fun = deprecated(add_fun,'add')
# 机智的你应该想到了@deprecated('add') 这样去装饰add_fun应该也能成吧！于是代码如下(关键代码)

# @deprecated('add')
# def add_fun(x, y):
#     """
#     实现两个数相加、并返回合
#     """
#     return x + y
# python3 dc.py
# Traceback (most recent call last):
#   File "dc.py", line 12, in <module>
#     @deprecated('add')
# TypeError: deprecated() missing 1 required positional argument: 'new_fun_name'
# 　　事实上目前语法糖衣只解决了最简单的情况、如果你要给@写法 指定参数还要另寻它法。

# @deprecated('add')

# TypeError: deprecated()
# missing
# 1
# required
# positional
# argument: 'new_fun_name'
# 　　事实上目前语法糖衣只解决了最简单的情况、如果你要给 @ 写法
# 指定参数还要另寻它法。

# 【真理简洁而有力】
# 　　linux的世界里有句话“一切皆文件”，python的世界里也有一句话“一切皆对象”；　但是关键不是会“背”，而是“领悟”。
# 　　一个经典的糖衣格式是这样的
# @decorate
# def fun():
#     pass
# 　　请仔细看一下不难发现 @ 后面直接是对象名、由python的数据模式可知、对象名只是一个对象的标识；也就是说 @ 后面是一个对象！对象可以
# 　　是已经定义好的，也可以是调用才生成。明白这一层道理之后事情就比较好办了，我们只要在调用时生成“装饰”对象就可以了，因为要调用
# 　　所以就给了我们传递参数的机会。

# 【触摸真理一】
# 　　用调用时生成的对象用作装饰器


def deprecated(new_fun_name):
    """derepcated 装饰器把函数标记为过时
    """
    def warpper(fun):
        """
        """
        def inner(*args):
            print("{0} 函数已经过时 请使用 {1}".format(fun.__name__, new_fun_name))
            return fun(*args)
        return inner
    return warpper


decorator = deprecated('add')  # 特意把这一步单独分离出来、用于说明什么叫调用时创建的对象用作做装饰器


@decorator  # 特意把这一步单独分离出来、用于说明什么叫调用时创建的对象用作做装饰器
def add_fun(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


def add(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


if __name__ == "__main__":
    print(add_fun(1, 1))
# 【触摸真理二】
# 　　与语法糖衣结合、完成传递参数的目的


def deprecated(new_fun_name):
    """derepcated 装饰器把函数标记为过时
    """
    def warpper(fun):
        """
        """
        def inner(*args):
            print("{0} 函数已经过时 请使用 {1}".format(fun.__name__, new_fun_name))
            return fun(*args)
        return inner
    return warpper


@deprecated('add')
def add_fun(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


def add(x, y):
    """
    实现两个数相加、并返回合
    """
    return x + y


if __name__ == "__main__":
    print(add_fun(1, 1))


def get_temp(temp_out):  # temp_out外部传参===>"李想"
    def get_test(test):
        def get_current_test(temp_in):  # temp_in===>"函数传参"
            data = test()  # 调用test()函数===>print("test")
            print(temp_in)
            return data
        return get_current_test
    print(temp_out)  # temp_out外部传参===>"李想"
    return get_test
"""
    @get_temp("李想")分两步走 
    1.get_temp("李想")====>调用get_temp()函数 并返回get_test引用
    2.@加上第一步得到的get_test引用===>@get_test===>test=get_test(test) 
"""


@get_temp("李想")  # "李想"===>传送给get_temp(temp_out)
def t1est():
    print("test")
    return "函数返回值--123"


result = t1est("函数传参")

print(result)  # ====>test（）返回值 "函数返回值--123"

# 实现一个空路由表，利用装饰器将url和功能函数的对应关系自动存到这个字典中
router_dict = {}
# 定义一个装饰器
# 再给一层函数定义，用来传入一个参数,这个参数就是访问的页面地址


def set_args(url):
    def set_func(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        router_dict[url] = wrapper  # 既可以是func也可以是wrapper,单如果是func,就无法添加wrapper中的新功能
        return wrapper
    return set_func
# @set_func  # index = set_func(index)


@set_args('index.html')
def index():
    print('Index Page....')
    return 'index'


@set_args('bbs.html')
def bbs():
    print('BBS Page....')
    return 'bbs'


@set_args('login.html')
def login():
    print('Login Page....')
    return 'Login'


def run(url):  # 通过传入访问地址，获取对应的功能函数
    func = router_dict[url]
    func()



# run('bbs.html')
# run('login.html')
# run('index.html')
# print(router_dict)


class NovaApi():
    def __init__(self):
        self.ip = controller_ip
        self.port = nova_port
        self.http_protocol = http_protocol
        self.endpoint = '{}://{}:{}'.format(self.http_protocol, self.ip, self.port)
        self.token = Keystone.token
        self.admin_token = Keystone.admin_token
        self.DIR_PATH = os.path.dirname(__file__)
        self.log = Logger('../Log/Nova.log', level='info').logger

    def listVms(self):
        url = '{}/v2.1/servers'.format(self.endpoint)
        base_header["X-Auth-Token"] = self.token
        r = requests.get(url=url, headers=base_header, verify=False)
        if r.status_code == 200:
            res = json.loads(r.content)
            server_list = res.get('servers')
            return server_list

        else:
            self.log.error('list vms request failed! {}-{}'.format(r.status_code, r.content))
            return False
    @nova_new_header
    def addOneVmUseLocalDiskNet(self, name, imageRef, flavorRef, network_id,
        availability_zone="nova", diskConfig="AUTO", description=None,
        security_groups: list = [{"name": "default"}]):
        url = '{}/v2.1/servers'.format(self.endpoint)
        body = {
        "server": {
        "name": name,
        "imageRef": imageRef,
        "flavorRef": flavorRef,
        "availability_zone": availability_zone,
        "OS-DCF:diskConfig": diskConfig,
        "description": description,
        "security_groups": security_groups,
        "networks": [{
        "uuid": network_id,}]
        }}
        body = json.dumps(body)
        r = requests.post(url=url, data=body, headers=base_header, verify=False)
        if r.status_code == 202:
            res = json.loads(r.content)
            self.log.info('vm:{} create success!'.format(name))
            vm_info = res.get('server')
            return vm_info
        else:
            self.log.error('create vm failed!-{}-{}'.format(r.content,r.status_code))
            return False

# 这个类中方法都需要在请求的时候传递header，但是他们的header会有所区别，所以需要使用不同的装饰器进行解决，如上：@nova_new_header，
# 会将self.token传递给装饰器中的base_header
# 装饰器：

        # def nova_new_header(func_or_cls):
        #     def wapper(*args, **kwargs):
        #         base_header["X-Auth-Token"] = self.token
        #         base_header["X-OpenStack-Nova-API-Version"] = '2.65'
        #         res = func_or_cls(self,*args, **kwargs)
        #         return res
        #     # return wapper

# 这样就可以在装饰器中将__init__中的self.token传递给func_or_cls，并且同时定义了API的微版本号。
# 本文同步分享在 博客“phyger”(CNBlog)。
# 如有侵权，请联系 support@oschina.cn 删除。
# 本文参与“OSC源创计划”，欢迎正在阅读的你也加入，一起分享。