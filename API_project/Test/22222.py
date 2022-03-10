# for i in range(10):
#     if i <10:
#         print(i)
# else:
#     print(2222222)
#
# if False or True:
#     print(1)

a = [1,2,345,22]
b = [1,2,345]
print(set(a).difference(set(b)))
if set(a).issubset(set(b)) is True:
    print(1)
