import record
import tts
import os
import threading
import queue

FILNAME = "recordTem.mp3"
FILE_SPEECH_IFK_TMP = "file_speech_ifk_tmp.wav"
isTtsLoop = True

# socket 通信


# 主循环
q = queue.Queue()

while not q.empty():
    msg = q.get()



# Tts线程
def run():
    while isTtsLoop:
        # 录音
        record.recording(FILNAME)
        # 交互
        res = tts.ifkaiui(FILNAME)
        #
        # 合成
        tts.ifkspeech(res, FILE_SPEECH_IFK_TMP)
        # 播放
        record.playing(FILE_SPEECH_IFK_TMP)



# 唤醒线程
def wake():
    print("wake")


#
awake = threading.Thread(target=wake(), name='LoopThread')
awake.start()

# 计时线程
def timing(long):
    pass


