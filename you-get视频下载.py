import os
import time

def you_get_download(url):
    root_cmd = 'you-get -o D:/you-get-download '
    url = url.replace('&seid=', '%3D')
    cmd = root_cmd + url
    os.system(cmd)

def main():
    print('\n' + '*'*30 + 'You-Get-Download' + '*'*30 + '\n')
    print('【说明】')
    print('1.这个小程序封装了you-get库，可以用来下载您所喜欢的视频、图片或者音乐！')
    print('2.此程序中资源会默认以最高品质下载，请见谅哦！')
    print('3.部分网站的资源是不能下载的哦，请见谅！')
    print('4.我只是一名搬运工，有时间多去官网支持它们的作者哦！')
    print('5.官网:https://github.com/soimort/you-get\n')
    print('我们开始吧!\n')

    url = input('请输入您需要下载的资源链接:')
    n = 0
    while url != '0':
        n += 1
        print('\n' + '*' * 30 + '请稍后' + '*' * 30 + '\n')
        you_get_download(url)
        print('\n' + '*'*30 + '第%s个文件处理结束'%n + '*'*30 + '\n')
        url = input("需要继续下载吗？需要的话请再次输入网址哦，不需要的话输入‘0’就可以退出啦:")
    else:
        print('\n已成功结束下载！\n')
        print('文件下载的位置默认是：D:\you-get-download，如有更多的磁盘麻烦自己转移哦！\n')
        print('另外，里面会有一个.xml文件是视频的字幕或者弹幕文件，放心删除!\n')
        print('三秒后程序帮您打开文件所在位置......\n')
        time.sleep(3)
        os.system('start explorer D:\you-get-download')
        print('程序即将自动关闭......')
        time.sleep(3)

if __name__ == '__main__':
    main()