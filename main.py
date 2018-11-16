import record
import tts
import os
import threading
import queue
import time
FILNAME = "recordTem.mp3"
FILE_SPEECH_IFK_TMP = "file_speech_ifk_tmp.wav"
isTtsLoop = True #对话循环
isClose = False #主循环


# socket 通信



# Tts线程
def run():
    while isTtsLoop:
        # 录音
        if not record.recording(FILNAME,isTtsLoop) == None:
            # 交互
            res = tts.ifkaiui(FILNAME)
            # 合成
            tts.ifkspeech(res, FILE_SPEECH_IFK_TMP)
            # 播放
            record.playing(FILE_SPEECH_IFK_TMP, isTtsLoop)
            q.put("recordStop")


# 主循环
q = queue.Queue()

# 唤醒线程
def wake():
    print('thread %s ended.\n' % threading.current_thread().name)
    time.sleep(5)
    q.put("wake")
#
awake = threading.Thread(target=wake, name='LoopThread')
awake.start()

print("loop start")
while not isClose:
    if not q.empty():
        msg = q.get()
        print(msg)
        if msg == "wake":
            run = threading.Thread(target=run, name='LoopThread')
            run.start()

