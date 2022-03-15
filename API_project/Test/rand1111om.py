import random


# 1.使用python random模块的choice方法随机选择某个元素
# from random import choice
foo = ['a', 'b', 'c', 'd', 'e']
print(random.choice(foo))
print(random.choice(['a', 'b', 'c', 'd', 'e']))
# print(random.choices(foo))

#
# # 2.使用python random模块的sample函数从列表中随机选择一组元素
list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 设置种子使得每次抽样结果相同
random.seed(10)
slice = random.sample(list, 5)  # 从list中随机获取5个元素，作为一个片断返回
print(slice)
print(list)  # 原有序列并没有改变。