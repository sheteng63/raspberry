import pyaudio
import numpy as np
import time
from scipy import fftpack
import wave


# 录音 超时进入等待唤醒 打断机制
# 录音必须安装portaudio模块，否则会报错
# http://portaudio.com/docs/v19-doxydocs/compile_linux.html
def recording(filename,isTtsLoop, time=0, threshold=1500):
    """
    :param filename: 文件名
    :param time: 录音时间,如果指定时间，按时间来录音，默认为自动识别是否结束录音
    :param threshold: 判断录音结束的阈值
    :return:
    """
    CHUNK = 1024  # 块大小
    FORMAT = pyaudio.paInt16  # 每次采集的位数
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率：每秒采集数据的次数
    RECORD_SECONDS = time  # 录音时间
    WAVE_OUTPUT_FILENAME = filename  # 文件存放位置
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("record start")
    frames = []
    if time > 0:
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
    else:
        stopflag = 0
        stopflag2 = 0
        startflag = 0
        startstate = False
        while True:
            data = stream.read(CHUNK)
            rt_data = np.frombuffer(data, np.dtype('<i2'))
            # print(rt_data*10)
            # 傅里叶变换
            fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
            fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]

            # 测试阈值，输出值用来判断阈值
            print(sum(fft_data) // len(fft_data))

            # 判断麦克风是否停止，判断说话是否结束，# 麦克风阈值，默认7000
            if sum(fft_data) // len(fft_data) > threshold:
                stopflag += 1
                startflag += 1
            else:
                stopflag2 += 1

            # print("startflag 1 ", startflag)
            oneSecond = int(RATE / CHUNK)
            # print("stopflag2 == %s stopflag == %s", stopflag2, stopflag)
            if stopflag2 + stopflag > oneSecond:
                if stopflag2 > oneSecond // 3 * 2:
                    if startstate:
                        startflag = 0
                        break
                    else:
                        stopflag2 = 0
                        stopflag = 0
                else:
                    stopflag2 = 0
                    stopflag = 0
            print(startflag)
            if startflag > 4:
                startstate = True
            if startstate:
                frames.append(data)
            if not isTtsLoop:
                stream.stop_stream()
                stream.close()
                p.terminate()
                return None

    print("record over")
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


# 播放
def playing(filepath,isTtsLoop):
    CHUNK = 1024
    wf = wave.open(filepath, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
        if not isTtsLoop:
            stream.stop_stream()
            stream.close()
            p.terminate()
            return None
    stream.stop_stream()
    stream.close()
    p.terminate()
    time.sleep(2)
    return
