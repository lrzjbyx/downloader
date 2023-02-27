import os
import sys
from copy import copy
import requests, time, hashlib, urllib.request, re, json
from PyQt5.QtGui import QImage, QPixmap
from imageio.core import urlopen
from lxml import etree
from urllib.parse import urljoin, urlparse
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import uuid
import ffmpeg
from progress import bar
from progressbar import progressbar
import platform

'''
        支持如下视频格式  https://github.com/leiurayer/downkyi
        # - [x] av号：av170001，https://www.bilibili.com/video/av170001
        # - [x] BV号：BV17x411w7KC，https://www.bilibili.com/video/BV17x411w7KC, https://b23.tv/BV17x411w7KC


        思路
        # - [x] 获取视频信息的链接
            #   https://api.bilibili.com/x/web-interface/view?bvid=BV18B4y1x7Rs
            #   https://api.bilibili.com/x/web-interface/view?aid=170001


        # - [x] 获取分级视频的链接
            # 在获取视频链接时会返回JSON，数据中包含pages字段和bvid键值
                {
                    "cid": 11111111,
                    "page": 1,
                    "from": "vupload",
                    "part": "1. xxxx-1",
                    "duration": 615,
                    "vid": "",
                    "weblink": "",
                    "dimension": { "width": 1280, "height": 720, "rotate": 0 },
                    "first_frame": "http://i0.hdslbxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            # 拼接分集视频的链接
                https://api.bilibili.com/x/player/playurl?cid={0}&qn=125&fourk=1&fnver=0&fnval=4048&bvid={1}
                cid     11111111
                bvid    BV18B4y1x7Rs
        # - [x] 获取每个视频真正的播放地址
            # 视频支持格式和清晰度["support_formats"]
            # 视频链接["video"]
                # id 代表不同的视频清晰度         ["16","32","64",...]
            # 音频链接["audio"]
                # id 代表不同的音频编码方式        ["30216","30232","30280"]

        # -[x] 下载视频      
        # -[x] 拼接视频音频


'''

class Bilibili():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        # 'referer': 'https://www.bilibili.com/'
    }
    audio_quality = {
        "30216": "64K",
        "30232": "132K",
        "30280": "192K"
    }
    video_quality = {
        "16": "360P 流畅",
        "32": "480P 清晰",
        "64": "720P 高清",
        "74": "720P 60帧",
        "80": "1080P 高清",
        "112": "1080P 高码率"
    }

    '''
    @:param video_url   视频链接
    @:param save_path   视频位置
    '''

    def __init__(self, save_path=os.path.join(os.getcwd(), "bilibili"), cookie=""):
        # 下载临时目录
        self.save_temporary_doc = os.path.join(os.getcwd(), "temp")
        # 保存路径
        self.save_path = save_path
        # 请求视频链接
        self.video_url = ""
        # 视频详解
        self.video_detailed = None
        # 多个p
        self.video_episodes_abridge = None
        # 视频详情
        self.video_detailed_base_url = "https://api.bilibili.com/x/web-interface/view?"
        # bv 链接
        self.av_bv_base_url = [
            "https://www.bilibili.com/video/", "https://b23.tv/"
        ]
        self.bvid = None
        self.aid = None
        # 初始化
        self.video_id()
        # 每个视频的详细信息
        self.every_video_detailed = {}
        # 每个视频的详细信息
        self.every_video_detailed_url = "https://api.bilibili.com/x/player/playurl?cid={0}&qn=125&fourk=1&fnver=0&fnval=4048&bvid={1}"

        # 初始化下载器
        self.opener = urllib.request.build_opener()

        self.opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', "https://www.bilibili.com"),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(self.opener)
        #  检测目录是否存在
        if not os.path.exists(self.save_temporary_doc):
            os.mkdir(self.save_temporary_doc)

        # 添加cookie
        if cookie != "":
            Bilibili.headers["cookie"] = cookie

    def set(self,video_url):
        self.video_url = video_url
        # 初始化
        self.video_id()


    def BvAv(self, t):
        # AV BV

        t = urljoin(t, urlparse(t).path)

        if t[0: len(self.av_bv_base_url[1])] == self.av_bv_base_url[1]:
            return t[len(self.av_bv_base_url[1]):].split("/")[0]
        elif t[0: len(self.av_bv_base_url[0])] == self.av_bv_base_url[0]:
            return t[len(self.av_bv_base_url[0]):].split("/")[0]
        else:
            return None

    def video_id(self):
        bv_av = self.BvAv(self.video_url + "/")
        if bv_av is None:
            return

        if bv_av[:2].lower() == "bv":
            self.bvid = bv_av
        else:
            self.aid = bv_av[2:]


    # 发起详情请求
    def require_video_detailed(self, url):

        response = requests.get(url, headers=Bilibili.headers)
        video_detailed = json.loads(response.content.decode("utf-8"))

        return video_detailed



    # 获取视频信息
    def require_input_link_video(self):
        url = ""

        if self.aid is None:
            url = self.video_detailed_base_url + "bvid=" + self.bvid
        else:
            url = self.video_detailed_base_url + "aid=" + self.aid

        self.video_detailed = self.require_video_detailed(url)

        print(self.video_detailed)

        self.save_path = os.path.join(self.save_path, "".join(
            re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', self.video_detailed["data"]["title"], re.S)))

        # 创建目录
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)

        self.video_episodes_abridge = self.video_detailed["data"]["pages"]
        self.bvid = str(self.video_detailed["data"]["bvid"])
        self.aid = str(self.video_detailed["data"]["aid"])


        data = {}
        data["bvid"] = self.video_detailed["data"]["bvid"]
        data["aid"] = self.video_detailed["data"]["aid"]
        #视频个数
        data["videos"] = self.video_detailed["data"]["videos"]
        # 首页图片
        data["pic"] =QPixmap.fromImage(QImage.fromData(urlopen(self.video_detailed["data"]["pic"]).read()))
        # 标题
        data["title"] = self.video_detailed["data"]["title"]
        # 描述
        data["desc"] = self.video_detailed["data"]["desc"]
        # 硬币
        data["coin"] = self.video_detailed["data"]["stat"]["coin"]
        # 喜欢
        data["like"] = self.video_detailed["data"]["stat"]["like"]
        # 分享
        data["share"] = self.video_detailed["data"]["stat"]["share"]
        # 收藏
        data["favorite"] = self.video_detailed["data"]["stat"]["favorite"]
        # 发布者名称
        data["owner_name"] = self.video_detailed["data"]["owner"]["name"]
        # 发布者头像
        data["owner_face"] = QPixmap.fromImage(QImage.fromData(urlopen(self.video_detailed["data"]["owner"]["face"]).read()))
        # 数据
        data["pages"] = [ i  for i in self.video_detailed["data"]["pages"]]
        return data


    def require_video_episodes(self,video_eppisode):

        response = requests.get(self.every_video_detailed_url.format(video_eppisode["cid"], self.bvid),
                                headers=Bilibili.headers)
        t = json.loads(response.content.decode("utf-8"))
        self.every_video_detailed[str(video_eppisode["cid"])] = t

        if len(self.video_episodes_abridge) == 1:
            title = self.video_detailed["data"]["title"]
        else:
            title = video_eppisode["part"]

        def codecs(a):
            item = {}
            for c in a:
                if c[0] in item.keys():
                    item[c[0]].append(c[1])
                else:
                    item[c[0]] = [c[1]]
            return item


        item = {
            "cid": video_eppisode["cid"],
            "title": title,
            "audio_quality": [a["id"] for a in t["data"]["dash"]["audio"]],
            "video_quality_codes": codecs([[a["id"],a["codecs"]] for a in t["data"]["dash"]["video"]]),
            "video_quality":list({}.fromkeys([a["id"] for a in t["data"]["dash"]["video"]]).keys()),
        }

        return item

    def signalVideoParse(self,index):
        item = self.require_video_episodes(self.video_episodes_abridge[index])
        return item