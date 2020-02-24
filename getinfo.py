import bilibili.getinfo as bGetinfo

bilibilicookies = "_uuid=B2263352-83C8-E817-4011-C5A862BBC19B25528infoc; buvid3=EAC1EDF5-60B4-4461-8E46-D8B4B81B6E14155832infoc; CURRENT_FNVAL=16; rpdid=|(umRJl|||mJ0J'ul~)lJ)~Jk; LIVE_BUVID=AUTO4715785517982545; im_notify_type_25437908=0; CURRENT_QUALITY=80; INTVER=1; sid=d448x1gs; DedeUserID=25437908; DedeUserID__ckMd5=516bfbcc2136a97d; SESSDATA=228af7e9%2C1585093835%2C48daa321; bili_jct=4d91f1d39d2a066feaf0c274622ad44c; bp_t_offset_25437908=359378270349537868"


bGetinfo = bGetinfo.GetInfo()
bGetinfo.init(bilibilicookies)
bGetinfo.getuinfo();