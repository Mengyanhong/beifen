a = int(input("请输入数据位数:"))
for i in range(9):
    for j in range(1,10):
        i = i+1
        if i <=9:
            if i != 9:
                print(f"{j}*{i}={i * j:<3d}", end="")
            else:
                print(f"{j}*{i}={i * j:<3d}", end="\n")


