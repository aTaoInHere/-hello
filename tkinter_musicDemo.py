import threading
import pygame
import tkinter
from tkinter import filedialog
import os
import time

# pygame.mixer.init()
#1 界面
root = tkinter.Tk() #创建界面
root.title("music")
root.geometry('400x600+500+100') #大小+位置
root.resizable(False, False) #是否可变大小

#函数式编程
folder = ''
res = []
num = 0
now_music = ''

def buttonChooseClick():
    '''
    添加文件
    :return:
    '''
    global folder
    global res
    if not folder:
        #打开文件、保存文件、选择目录等关于文件的操作
        folder = tkinter.filedialog.askdirectory()
        musics = [folder + '\\' + music for music in os.listdir(folder)]
                  # if music.endswith('.mp3', '.wav', '.ogg')]
        ret = []
        for i in musics:
            ret.append(i.split('\\')[1:])
            res.append(i.replace('\\', '/'))
        var2 = tkinter.StringVar()
        var2.set(ret)
        lb = tkinter.Listbox(root, listvariable=var2) #列表框
        lb.place(x=50, y=100, width=260, height=300)

    if not folder:
        return

    global playing
    playing = True
    buttonNext['state'] = 'normal'
    buttonPrev['state'] = 'normal'
    buttonPlay['state'] = 'normal'




def play():
    '''
    播放音乐
    :return:
    '''
    if len(res):

        pygame.mixer.init() #播放音乐
        global num
        while playing:
            if not pygame.mixer.music.get_busy():#检查当前是否正在播放音乐
                '''
                pygame.mixer.music.load()  ——  载入一个音乐文件用于播放
                pygame.mixer.music.play()  ——  开始播放音乐流
                pygame.mixer.music.rewind()  ——  重新开始播放音乐
                pygame.mixer.music.stop()  ——  结束音乐播放
                pygame.mixer.music.pause()  ——  暂停音乐播放
                pygame.mixer.music.unpause()  ——  恢复音乐播放
                pygame.mixer.music.fadeout()  ——  淡出的效果结束音乐播放
                pygame.mixer.music.set_volume()  ——  设置音量
                pygame.mixer.music.get_volume()  ——  获取音量
                pygame.mixer.music.get_busy()  ——  检查是否正在播放音乐
                pygame.mixer.music.set_pos()  ——  设置播放的位置
                pygame.mixer.music.get_pos()  ——  获取播放的位置
                pygame.mixer.music.queue()  ——  将一个音乐文件放入队列中，并排在当前播放的音乐之后
                pygame.mixer.music.set_endevent()  ——  当播放结束时发出一个事件
                pygame.mixer.music.get_endevent()  ——  获取播放结束时发送的事件
                Pygame 中播放音乐的模块和 pygame.mixer 模块是密切联系的。使用音乐模块去控制在调音器上的音乐播放。
                '''
                nextMusic = res[num]
                print(nextMusic)
                pygame.mixer.music.load(nextMusic.encode())
                pygame.mixer.music.play(1)
                # if len(res) - 1 == num:
                #     num = 0
                # else:
                #     num += 1
                nextMusic = nextMusic.split('/')[-1][:-4]
                musicName.set('playing....' + ''.join(nextMusic))
            else:
                time.sleep(0.1)



def buttonPlay():
    '''
    点击播放
    :return:
    '''

    if pause_resume.get() == '播放':
        pause_resume.set('暂停')
        # global folder
        # if not folder:
        #     folder = tkinter.filedialog.askdirectory()
        #
        # if not folder:
        #     return
        global playing
        playing = True
        t = threading.Thread(target=play)
        t.start()
    elif pause_resume.get() == '暂停':
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        # pygame.mixer.music.pause()
        pause_resume.set('继续')
    elif pause_resume.get() == '继续':
        pygame.mixer.music.unpause()
        pause_resume.set('暂停')


def buttonStop():
    '''
    停止播放
    :return:
    '''
    global playing
    playing = False
    pygame.mixer.music.stop()

def buttonNext():
    '''
    点击下一首
    :return:
    '''
    global playing
    playing = False
    global num
    if len(res) == num:
        num = 0
    num += 1
    playing = True
    #创建线程
    t = threading.Thread(target=play)
    t.start()


def close():
    '''
    关闭窗口
    :return:
    '''
    global playing
    playing = False
    time.sleep(0.3)
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    root.destroy()

def control_voice(value=0.5):
    '''
    声音控制
    :param value:0.0-1.0
    :return:
    '''
    pygame.mixer.music.set_volume(float(value))

def buttonPrev():
    '''
    上一首
    :return:
    '''
    global playing
    playing = False
    global num
    if num == 0:
        num = len(res) - 1
    else:
        num -= 1

    playing = True
    # 创建线程
    t = threading.Thread(target=play)
    t.start()


#关闭
root.protocol('WM_DELETE_WINDOW', close)

#按钮
buttonChoose = tkinter.Button(root, text='添加', command=buttonChooseClick)
#设置位置
buttonChoose.place(x=50, y=10, width=50, height=20)

#显示框
pause_resume = tkinter.StringVar(root, value='播放')
#可变名称按钮
buttonPlay = tkinter.Button(root, textvariable=pause_resume, command=buttonPlay)
buttonPlay.place(x=190, y=10, width=50, height=20)
buttonPlay['state'] = 'disabled'

#停止播放
buttonStop = tkinter.Button(root, text='停止', command=buttonStop)
buttonStop.place(x=120, y=10, width=50, height=20)
buttonStop['state'] = 'disabled'

#下一首
buttonNext = tkinter.Button(root, text='下一首', command=buttonNext)
buttonNext.place(x=260, y=10, width=50, height=20)
buttonNext['state'] = 'disabled'

#上一首
buttonPrev = tkinter.Button(root, text='上一首', command=buttonPrev)
buttonPrev.place(x=330, y=10, width=50, height=20)
buttonPrev['state'] = 'disabled'

#
musicName = tkinter.StringVar(root, value='暂时没有播放音乐...')
labelName = tkinter.Label(root, textvariable=musicName)
labelName.place(x=10, y=30, width=260, height=20)

#滑块
#horizontal水平放置，默认为vertical
s = tkinter.Scale(root, label='音量', from_=0, to=1,orient=tkinter.HORIZONTAL,
                  length=240, showvalue=0, tickinterval=2, resolution=0.01,
                  command=control_voice)
s.place(x=50, y=50, width=200)

#消息循环
root.mainloop()

