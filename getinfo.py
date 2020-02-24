import bilibili.getinfo as bGetinfo

bilibilicookies = "SESSDATA=228af7e9%2C1585093835%2C48daa321; bili_jct=4d91f1d39d2a066feaf0c274622ad44c;"





bGetinfo = bGetinfo.GetInfo()
bGetinfo.init(bilibilicookies)
print(bGetinfo.getuinfo().following);