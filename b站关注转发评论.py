import requests,re
from bs4 import BeautifulSoup
import json



headers={
'User-Agent': 'User-Agent":"',

'cookie':"",

}   #浏览器里你自己B站账号的cookie

url1=''       #更改的抽奖网址
html2=requests.get(url1,headers=headers)
con2=html2.text

csrf=""


text3=re.findall("https...b23.tv........(?=..htt)",con2)
#region 列表
zflb={       #转发的列表文件
    'uid':'',#自己的uid
    'content':'', #自己想转发的时候发什么
    'type':'1',
    'repost_code': '30000',
    'from': 'create.comment',
    'extension':'{"emoji_type":1}',

}
pllb1={    #短的数字的评论的列表文件

    "type":'11',
    'message':" ",   #自己想评论的时候发什么
    'plat':"1",
    'ordering': 'time',
    'jsonp': 'jsonp',
    'csrf': csrf,

}
pllb2={    #长的评论的列表文件

    "type":'17',
    'message':" ",  #自己想评论的时候发什么
    'plat':"1",
    'ordering': 'time',
    'jsonp': 'jsonp',
    'csrf': csrf,

}


dzlb={      #点赞的列表
    'up':'1',
'csrf': csrf,
}
formdata={    #关注的列表
    'act':'1',   #act为1时点赞 为2时取消点赞
    'csrf': csrf,

}
#endregion
#region 方法函数
#方法
def gz(aid):  #关注
    url="https://api.bilibili.com/x/relation/modify"#动态关注
    formdata['fid']=aid         #up主的uid
    # print(formdata)
    try:
        requests.post(url,data=formdata,headers=headers)

    except:
        print('there has some trouble')



def dianzhan(aid):    #点赞
    url1 = 'https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb'  # 动态点赞
    dzlb['dynamic_id'] =aid        #动态页面的一串数字
    requests.post(url1,data=dzlb,headers=headers)


def pl1(aid):     #评论
    urlpl = 'https://api.bilibili.com/x/v2/reply/add'  # 动态评论
    pllb1['oid']=aid     #评论的有两种 暂时还不能很好的进行工作 23.05.09/
    requests.post(urlpl,data=pllb1,headers=headers)
def pl2(aid):     #评论
    urlpl = 'https://api.bilibili.com/x/v2/reply/add'  # 动态评论
    pllb2['oid']=aid     #评论的有两种 暂时还不能很好的进行工作 23.05.09/
    requests.post(urlpl,data=pllb2,headers=headers)

def zf(aid):     #转发
    urzf = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/reply'
    zflb['rid']=aid       #动态页面的一串数字
    requests.post(urzf,data=zflb,headers=headers)
#endregion


ns=0
ne=90  #选择页面的抽奖个数
try:
    for n in range(ns,ne):

        zurl=requests.head(text3[n],allow_redirects=True)
        wzurl=zurl.url

        dtsz=re.findall('(?<=com.)..................(?=.plat.id)',wzurl) #获取动态网页的数字
        print(dtsz[0])
        dianzhan(dtsz[0])
        zf(dtsz[0])
        pl2(dtsz[0])

        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={dtsz[0]}'

        html1 = requests.get(url, headers=headers)
        con = html1.text
        uidhq = re.findall('(?<=.uid..).*?(?=..type.*)',con)   #获取动态up的UID
        gz(uidhq[0])
        text1 = re.findall('(?<=..type.....rid..).........(?=..acl)',con) #获取短的数字 还有一个长的 可能要写两套获取代码
        pl1(text1[0])
        print(f"   {n}")
except:
    print("数字不对")

