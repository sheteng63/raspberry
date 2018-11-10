import time
import json
import hashlib
import base64
from urllib import request, parse


# 讯飞语音识别
def ifktts(filename):
    f = open(filename, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = '47bbcb78dae53f475dedbc19356a3be5'
    param = {"engine_type": "sms16k", "aue": "raw"}
    x_appid = '5be543f2'
    x_param = base64.b64encode(bytes(json.dumps(param).replace(' ', ''), encoding="utf8"))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(bytes(api_key + str(x_time) + str(x_param, encoding="utf8"), encoding="utf8")).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': str(x_time),
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    data = bytes(parse.urlencode([("audio", base64_audio)]), encoding="utf8")
    # http = apihttp.apicommonhttp(url).addBody("audio", base64_audio).addHeaders(x_header).post()
    # data = json.loads(http.text,encoding="utf8")
    req = request.Request(url, headers=x_header)
    resp = request.urlopen(req, data=data)
    res = resp.read().decode()
    print(res)

    return json.loads(res)["data"]


# 讯飞语音合成
def ifkspeech(ts, filename):
    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    AUE = "raw"
    APPID = "5be543f2"
    API_KEY = "0fe0a727d9e9747e8a760c10acdce6d6"
    x_time = int(int(round(time.time() * 1000)) / 1000)
    # param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
    param = {
        "auf": "audio/L16;rate=16000",
        "aue": "raw",
        "voice_name": "xiaoyan",
        "engine_type": "intp65",
    }
    paramBase64 = base64.b64encode(bytes(json.dumps(param).replace(' ', ''), encoding="utf8"))

    checkSum = hashlib.md5(
        bytes(API_KEY + str(x_time) + str(paramBase64, encoding="utf8"), encoding="utf8")).hexdigest()
    header = {
        'X-CurTime': x_time,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    req = request.Request(URL, headers=header)
    resp = request.urlopen(req, data=bytes(parse.urlencode([("text", ts)]), encoding="utf8"))
    contentType = resp.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = resp.headers['sid']
        if AUE == "raw":
            writeFile(filename, resp.read())
        else:
            writeFile(filename, resp.content)
        print("success, sid = " + sid)
    else:
        print(resp.read().decode())


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()


# 交互
def ifkaiui(filepath):
    URL = "https://openapi.xfyun.cn/v2/aiui"
    APPID = "5be543f2"
    API_KEY = "61f3e3bd596b48d7b6b1cca2a1c961b4"
    curTime = str(int(time.time()))
    param = "{\"result_level\":\"complete\",\"aue\":\"raw\",\"auth_id\":\"2049a1b2fdedae553bd03ce6f4820ac4\",\"data_type\":\"audio\",\"sample_rate\":\"16000\",\"scene\":\"main\",\"lat\":\"39.26\",\"lng\":\"115.14\"}"
    paramBase64 = base64.b64encode(bytes(param, encoding="utf8"))

    checkSum = hashlib.md5(
        bytes(API_KEY + curTime + str(paramBase64, encoding="utf8"), encoding="utf8")).hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    binfile = open(filepath, 'rb')
    data = binfile.read()

    # http = apihttp.apicommonhttp(url).addBody("audio", base64_audio).addHeaders(x_header).post()
    # data = json.loads(http.text,encoding="utf8")
    req = request.Request(URL, headers=header)
    resp = request.urlopen(req, data=data)
    res = json.loads(resp.read().decode())
    print(res)
    ansres = ""
    ansres2 = ""
    if res['code'] == '0':
        lists = res["data"]
        for ans in lists:
            if ans["sub"] == "nlp":
                intent = ans["intent"]
                print(intent)
                if intent != {}:
                    answer = intent.get("answer")
                    if answer != None:
                        ansres += answer.get("text")
            elif ans["sub"] == "iat":
                pass
        if ansres == "":
            pass
    if ansres == "":
        ansres = "我没有听懂你说的啥"
    #
    return ansres
