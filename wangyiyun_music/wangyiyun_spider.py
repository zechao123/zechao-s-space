import os,sys
import time,requests
from lxml import etree
from urllib.request import urlretrieve
from tkinter import *
from tkinter import filedialog
import threading

root = Tk()
root.title("网易云爬取歌手页面音乐！")
#窗口大小
width ,height= 400, 300
#窗口居中显示
root.geometry('%dx%d+%d+%d' % (width,height,(root.winfo_screenwidth() - width ) / 2, (root.winfo_screenheight() - height) / 2))
#窗口最大值
root.maxsize(400,300)
#窗口最小值
root.minsize(400,300)
label = Label(root, text="请输入要爬取的网址：")
label.pack()
entry = Entry(root,width="40")
entry.pack()
label = Label(root, text="下载进度显示：")
label.pack()
TEXT=Text(width=45,height=12)
TEXT.pack()
# TEXT.insert(INSERT,"你好\n")
# TEXT.insert(INSERT,"你好ma")
#下载进度显示
def cbk(a, b, c):
    '''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
        sys.stdout.write('\r')
        sys.stdout.write('当前已经下载了%.2f%%' % per)


    else:
        sys.stdout.write('\r')
        sys.stdout.write('当前已经下载了%.2f%%' % per)



def thread_it(func, *args):
        # 创建线程
    t = threading.Thread(target=func, args=args)
        # 守护线程
    t.setDaemon(True)
        # 启动
    t.start()


def run():
    Folderpath = filedialog.askdirectory()
    url0=entry.get()
    url = "https://y.music.163.com/m/" + url0[24:]
    result=requests.get(url).text
    response=etree.HTML(result)
    music=response.xpath('//ul[@class="f-hide"]/li/a')

    text=Folderpath.replace('/','\\')
    for elem in music:
        addr=",".join(elem.xpath('@href'))
        add_song="https://link.hhtjim.com/163/"+addr[9:]+".mp3"
        dir = os.path.abspath('.')

        work_path = os.path.join(dir, '%s'%text+'\%s.mp3'%elem.text)
        TEXT.insert(INSERT,"正在下载"+elem.text+"...\n")
        urlretrieve(add_song, work_path, cbk)
        TEXT.insert(INSERT, elem.text+"下载完成！\n\n")
        print("\n")
        TEXT.see(END)
    TEXT.insert(INSERT, "共")
    TEXT.insert(INSERT,len(music))
    TEXT.insert(END,"首歌曲下载完成！")
button = Button(root, text="选择文件夹并爬取", command=lambda:thread_it(run))
button.pack()
root.mainloop()