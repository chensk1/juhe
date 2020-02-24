import bilibili.file as bF
import bilibili.upload as bUpload

bilibilicookies = "LIVE_BUVID=AUTO4715785517982541; DedeUserID=25437901;  SESSDATA=228af7e9%2C1585093835%2C48daa321; bili_jct=4d91f1d39d2a066feaf0c274622ad44c"


json = {
    "copyright": 2,  # 1自治，2搬运
    "videos": [{
        "filename": 0,  # 别管
        "title": "日常第二十一话",  # 分p标题
        "desc": ""  # 不知道
    }],
    "source": "测试投稿",  # 转载地址
    "tid": 21,  # 分类
    "cover": "",  # 封面图  可以不管
    "title": "日常第二十一话",  # 总标题
    "tag": "日漫",  # 标签
    "desc_format_id": 0,  # 不知道
    "desc": "测试投稿",  # 简介
    "dynamic": "#日漫#",  # 粉丝动态
    "subtitle": {"open": 0, "lan": ""}  # 不知道
}

# 视频文件
f = bF.File('/Users/chensk/Downloads/1582502173642103.mp4')

# print(f.read(2500))

bUpload = bUpload.Upload()
bUpload.init('23333.mp4', f.size, bilibilicookies)  # '23333.mp4' 可以随便填，但必须有相应的视频格式后缀
bUpload.set_post_json(json)
bUpload.run(f)



f.close()
