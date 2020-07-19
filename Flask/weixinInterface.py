#coding:UTF-8
import hashlib
import web
import time
import os
import urllib2,json
import lxml
from lxml import etree
import sae.kvdb
import random

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root=os.path.join(self.app_root,'templates')
        self.render=web.template.render(self.templates_root)
        self.kv_client = sae.kvdb.Client()
        
    def csz(self, strNum, strAnwser):
        if not (strNum.isdigit() and len(strNum) == 4):
            return "请输入四位正整数："
        A=B=0 
        for i in range(0,4):
            if int(strNum[i]) == int(strAnwser[i]):
                A+=1
            else:
                if strNum[i] in strAnwser:
                    B+=1
        if A==4:
            return "Bingo!"
        else:
            return ("%dA%dB" %(A,B))
        
    def listToString(self,s):
        # initialize an empty string 
        str1 = ""
        # traverse in the string   
        for ele in s:  
            str1 += str(ele)
        # return string   
        return str1  
		
    def GET(self):
        #获取输入参数
        data=web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="alvintang6232"
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()#sha1加密算法#如果是来自微信的请求，则回echostr
        if hashcode==signature:
            return echostr

    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #print "DEBUG_OUT" + content
        #下面创建一个欢迎消息，通过判断Event类型
        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                replayText = u'''\
                欢迎关注本微信，这个微信是本人业余爱好所建立，也是想一边学习Python一边玩的东西，
                现在还没有什么功能，只是弄了个翻译与豆瓣图书查询的小工具，你们有什么好的文章也欢迎反馈给我,我会不定期的分享给大家，输入help查看操作指令
                '''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            if mscontent == "unsubscribe":
                replayText = u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来'                
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
        if msgType == 'text':
            content=xml.find("Content").text
            if content.lower() == 'bye':
                self.kv_client.delete(fromUser)
                self.kv_client.delete(fromUser+'_answer')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经跳出了猜数字游戏，输入help来显示其他操作指令')
            if content.lower() == 'csz':
                print "DEBUG_OUT" + content + "in"
                self.kv_client.set(fromUser,'csz')
                str=self.listToString(random.sample(range(0,10),4))
                print str
                self.kv_client.set(fromUser+'_answer', str)
                print self.kv_client.get(fromUser+'_answer')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u'您已经进入猜数字游戏，请输入四位正整数！输入bye跳出游戏')
            if content.lower() == 'tyn':
                
                rstr = u'系统时间: %s\n当前水温: %s\n当前水位: %s\n上水中: %s\n加热中: %s\n 输入\"kss\"开始上水\n输入\"gss\"关闭上水\n输入\"kjr\"开始加热\n输入\"gjr\"关闭加热'\
                % (self.kv_client.get("Time"), self.kv_client.get("Temprature"), self.kv_client.get("WaterPos"), self.kv_client.get("ValveStatus")\
                , self.kv_client.get("HeaterStatus"))
                return self.render.reply_text(fromUser,toUser,int(time.time()),rstr)
            if content.lower() == 'kss':
                if self.kv_client.get("kss"):
                    self.kv_client.replace("kss", "1")
                else:
                    self.kv_client.add("kss", "1")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"打开上水")
            if content.lower() == 'gss':
                if self.kv_client.get("kss"):
                    self.kv_client.replace("kss", "0")
                else:
                    self.kv_client.add("kss", "0")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"关闭上水")
            if content.lower() == 'zdss':
                if self.kv_client.get("kss"):
                    self.kv_client.replace("kss", "3")
                else:
                    self.kv_client.add("kss", "3")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"自动上水")
            if content.lower() == 'kjr':
                if self.kv_client.get("kjr"):
                    self.kv_client.replace("kjr", "1")
                else:
                    self.kv_client.add("kjr", "1")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"打开加热")
            if content.lower() == 'gjr':
                if self.kv_client.get("kjr"):
                    self.kv_client.replace("kjr", "0")
                else:
                    self.kv_client.add("kjr", "0")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"关闭加热")
            if content.lower() == 'zdjr':
                if self.kv_client.get("kjr"):
                    self.kv_client.replace("kjr", "3")
                else:
                    self.kv_client.add("kjr", "3")
                return self.render.reply_text(fromUser,toUser,int(time.time()),"自动加热")
            if content.lower().startswith('swsd5'):
                swsd5 = content.lower()[5:]
                if self.kv_client.get("swsd5"):
                    self.kv_client.replace("swsd5", swsd5)
                else:
                    self.kv_client.add("swsd5", swsd5)
                return self.render.reply_text(fromUser,toUser,int(time.time()),"水位5设定:" + swsd5)
            if content.lower().startswith('swsd1'):
                swsd1 = content.lower()[5:]
                if self.kv_client.get("swsd1"):
                    self.kv_client.replace("swsd1", swsd1)
                else:
                    self.kv_client.add("swsd", swsd1)
                return self.render.reply_text(fromUser,toUser,int(time.time()),"水位1设定:" + swsd1)
            if content.lower().startswith('wdsd'):
                wdsd = content.lower()[4:]
                if self.kv_client.get("wdsd"):
                    self.kv_client.replace("wdsd", wdsd)
                else:
                    self.kv_client.add("wdsd", wdsd)
                return self.render.reply_text(fromUser,toUser,int(time.time()),"温度设定:" + wdsd)
            if self.kv_client.get(fromUser) =='csz':
                anwser=self.kv_client.get(fromUser+'_answer')
                res = self.csz(content,anwser)
                if(res == "Bingo!"):
                    str=self.listToString(random.sample(range(0,10),4))
                    self.kv_client.replace(fromUser+'_answer', str)
                return self.render.reply_text(fromUser,toUser,int(time.time()),res)            
            
            if content.lower() == 'help':
                replayText = u'''\
                1.输入\"csz\"进入猜数字游戏
                2.输入\"tyn\"查看太阳能热水器数据
                '''
                return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
            elif type(content).__name__ == "unicode":
                #content = content.encode('UTF-8')
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"我现在还在开发中，还没有什么功能，您刚才说的是："+content)


