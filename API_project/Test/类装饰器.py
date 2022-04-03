# 装饰不带参数的函数
def clothes(func):
    def wear():
        print('Buy clothes!{}'.format(func.__name__))
        return func()

    return wear


@clothes
def body():
    print('The body feels could!')

# 备注：@是语法糖
# 不用语法糖的情况下，使用下面语句也能实现装饰作用：把body再加工，再传给body
# body = clothes(body)

# 装饰带一个参数的函数


def clothes(func):
    def wear(anything):  # 实际是定义一个anything参数，对应body函数参数
        print('Buy clothes!{}'.format(func.__name__))
        return func(anything)  # 执行func函数，并传入调用传入的anything参数
        # wear = func(anything)    # 在这一步，实际上可以看出来，为啥wear必须带参数，因为它就是func(anything)

    return wear
    # 所以clothes的结果是
    # clothes = wear = func(anything)
    # 不用语法糖的情况下就是
    # body = clothes(body)('hands')
    # 进一步证明：print(body.__name__)  显示的是wear函数


@clothes
def body(part):
    print('The body feels could!{}'.format(part))


body('hands')

# 装饰带不定长参数的函数
# 通常装饰器不只装饰一个函数，每个函数参数的个数也不相同
# 这个时候使用不定长参数 * args, ** kwargs


def clothes(func):
    def wear(*args, **kwargs):
        print('Buy clothes!{}'.format(func.__name__))
        return func(*args, **kwargs)

    return wear


@clothes
def body(part):
    print('The body feels could!{}'.format(part))


@clothes
def head(head_wear, num=2):
    print('The head need buy {} {}!'.format(num, head_wear))


body('hands')
head('headdress')

# 装饰器带参数

# 把装饰器再包装，实现了seasons传递装饰器参数。


def seasons(season_type):


    def clothes(func):
        def wear(*args, **kwargs):
            if season_type == 1:
                s = 'spring'
            elif season_type == 2:
                s = 'summer'
            elif season_type == 3:
                s = 'autumn'
            elif season_type == 4:
                s = 'winter'
            else:
                print('The args is error!')
                return func(*args, **kwargs)
            print('The season is {}!{}'.format(s, func.__name__))
            return func(*args, **kwargs)

        return wear

    return clothes


@seasons(2)
def children():
    print('i am children')


children()


# 二、在类里定义装饰器，装饰本类内函数：
# 类装饰器，装饰函数和类函数调用不同的类函数
# 把装饰器写在类里
# 在类里面定义个函数，用来装饰其它函数，严格意义上说不属于类装饰器。

class Buy(object):
    def __init__(self, func):
        self.func = func

    # 在类里定义一个函数
    def clothes(func):  # 这里不能用self,因为接收的是body函数
        # 其它都和普通的函数装饰器相同
        def ware(*args, **kwargs):
            print('This is a decrator!')
            return func(*args, **kwargs)

        return ware


@Buy.clothes
def body(hh):
    print('The body feels could!{}'.format(hh))


body('hh')

# 装饰器装饰同一个类里的函数
# 背景：想要通过装饰器修改类里的self属性值。

class Buy(object):
    def __init__(self):
        self.reset = True  # 定义一个类属性，稍后在装饰器里更改
        self.func = True

        # 在类里定义一个装饰器

    def clothes(func):  # func接收body
        def ware(self, *args, **kwargs):  # self,接收body里的self,也就是类实例
            print('This is a decrator!')
            if self.reset == True:  # 判断类属性
                print('Reset is Ture, change Func..')
                self.func = False  # 修改类属性
            else:
                print('reset is False.')
            return func(self, *args, **kwargs)
        return ware
    @clothes
    def body(self):
        print('The body feels could!')


b = Buy()  # 实例化类
b.body()  # 运行body
print(b.func)  # 查看更改后的self.func值，是False，说明修改完成

# 三、类装饰器
# 定义一个类装饰器，装饰函数，默认调用__call__方法

#
class Decrator(object):
    def __init__(self, func):  # 传送的是test方法
        self.func = func

    def __call__(self, *args, **kwargs):  # 接受任意参数
        print('函数调用CALL')
        return self.func(*args, **kwargs)  # 适应test的任意参数


@Decrator  # 如果带参数，init中的func是此参数。
def test(hh):
    print('this is the test of the function !', hh)


test('hh')

# 定义一个类装饰器，装饰类中的函数，默认调用__get__方法
# 实际上把类方法变成属性了，还记得类属性装饰器吧，
# @property下面自已做一个property

class Decrator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        '''
        instance:代表实例，sum中的self
        owner：代表类本身，Test类

        '''
        print('调用的是get函数')
        return self.func(instance)  # instance就是Test类的self


class Test(object):
    def __init__(self):
        self.result = 0

    @Decrator
    def sum(self):
        print('There is the Func in the Class !')


t = Test()
print(t.sum)  # 众所周知，属性是不加括号的,sum真的变成了属性


# 做一个求和属性sum，统计所有输入的数字的和

class Decrator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        print('调用的是get函数')
        return self.func(instance)


class Test(object):
    def __init__(self, *args, **kwargs):
        self.value_list = []
        if args:
            for i in args:
                if str(i).isdigit():
                    self.value_list.append(i)
        if kwargs:
            for v in kwargs.values():
                if str(v).isdigit():
                    self.value_list.append(v)

    @Decrator
    def sum(self):
        result = 0
        print(self.value_list)
        for i in self.value_list:
            result += i

        return result


t = Test(1, 2, 3, 4, 5, 6, 7, 8, i=9, ss=10, strings='lll')

print(t.sum)