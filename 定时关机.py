from os import*
from time import*
print("\n嗨,这个程序可以让您快速设置电脑定时关机哦!\n")
t=eval(input("您想多少分钟后关机呢:"))
print("\n即将为您执行!")
system("shutdown -s -t {}".format(t*60))
print("\n已成功执行!")
a=input("\n如果需要取消的话,请输入0,不需要的话回车即可退出:")
if a=="0":
    system("shutdown -a")
    b=input("\n已取消!任意键退出!")
