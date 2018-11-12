import record
import tts
import os

FILNAME = "recordTem.mp3"
FILE_SPEECH_IFK_TMP = "file_speech_ifk_tmp.wav"


class launch:
    def __init__(self):
        pass

    def run(self):
        isreturn = True
        while isreturn:
            print("开始录音")
            # 录音
            record.recording(FILNAME)
            # 交互
            # res = tts.ifkaiui(FILNAME)

            #

            # 合成
            # tts.ifkspeech(res, FILE_SPEECH_IFK_TMP)
            # 播放
            # record.playing(FILE_SPEECH_IFK_TMP)

            # os.remove(FILNAME)
            # os.remove(FILE_SPEECH_IFK_TMP)
            print("结束录音")
            isreturn = False


launch().run()
