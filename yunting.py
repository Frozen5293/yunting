import hashlib
import time
import requests
import json

# tmo={
#     "Content-Type": "application/json",
#     "equipmentId": "0000",
#     "platformCode": "WEB",
#     "timestamp": "1717033704774",
#     "sign": "C3E5402AB0A628B6055EC15879BB47FF",
# }

# var_key = 'f0fc4c668392f9f9a447e48584c214ee'
# var_key = 'f0fc4c668392f9f9a447e48584c214ee'


# url="https://ytmsout.radio.cn/web/appBroadcast/list?categoryId=0&provinceCode=0"



# header={
#     "Content-Type":"application/json",
#     "equipmentId":"0000",
#     "platformCode": "WEB",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
# }


### 必要参数
### header=> equipmentId， platformCode， Content,
### parms=> categoryId, provinceCode=0



class FileM:
    def save_as_file(filename,content):
        with open(filename,'w',encoding="utf-8") as f :
            f.write(content)
            pass




class YunTing:

    var_key:str
    api:dict
    host:dict
    api_header:dict

    def __init__(self) -> None:
        self.var_key=None
        self.api=None
        self.api_header=None
        self.host=None

    def set_key(self,key:str):
        self.var_key=key

    def set_host(self,host,protocol):
        if protocol=="https":
            self.host="https://"+host

    def set_api(self,api_name,api,api_header):
        if self.api==None or self.api_header==None:
            self.api={
                api_name:api
            }
            self.api_header={
                api_name:api_header
            }
            return
        self.api[api_name]=api
        self.api_header[api_name]=api_header


    def get_api_from_file(self,filepath:str):
        with open(filepath) as f:
            opt=json.loads(f.read())
            for i in opt.keys():
                if self.api==None:
                    self.api={}
                if self.api_header==None:
                    self.api_header={}
                self.api[i]=opt[i]["url"]
                self.api_header[i]= dict(opt[i]["header"]) or {}
                

    ## 拼接参数
    def get_parms_str(self,parms:dict):
        res=""
        for i in list(parms.keys()):
            res+=i
            res+="="
            res+=parms[i]
            res+="&"
        res=res[:-1] if len(res)>1 else ""
        return res


    ## 产生需要加密的字符传
    def __get_parms_encrypt_string(self,parms:dict):
        now = str(int(time.time()*1000))
        # str= "1717055490485"
        # str= "1717056009"
        #now = "1717057943618"
        now="1717062027925"
        parms_str=self.get_parms_str(parms)
        res=parms_str+('&timestamp=' if len(parms_str)>0 else "timestamp=") + now + '&key=' + self.var_key
        #print(res)
        return (res,now)
    ## 计算signc参数，传入需要签名的参数
    def __calculate_sign(self,encrypt_str):
        print("tohash：",encrypt_str)
        var_sign=hashlib.md5(encrypt_str.encode("utf-8")).hexdigest().upper()
        print("hashres:",var_sign)
        return var_sign

    ## 构建header
    def header_remake(self,header,parms:dict)->str:
        en_str,timestamp=self.__get_parms_encrypt_string(parms)
        sign:str=self.__calculate_sign(en_str)
        header["sign"]=sign
        header["timestamp"]=timestamp

        return header
    
    ## 获取请求
    def request(self,api_name:str,parms:dict):

        header:dict=None

        url:str = self.api[api_name] if self.api!=None or self.api[api_name]!=None else None

        header=self.header_remake(self.api_header[api_name],parms)

        ret=requests.get(
            self.host+url+"?"+self.get_parms_str(parms),
            #params=self.get_parms_str(parms),
            headers=header
        )
        return ret
        # print("url:")
        # print(self.host+url)
        # print("header:")
        # print(header)

        # print(ret.content.decode("utf-8"))

yt= YunTing()
yt.set_key('f0fc4c668392f9f9a447e48584c214ee')
yt.set_host('ytmsout.radio.cn',"https")
yt.get_api_from_file("api.json")


tmp=yt.request("getRadioCategoryList",{})
FileM.save_as_file("getRadioCategoryList.json",tmp.content.decode("utf-8"))
tmp=yt.request("getProvinceList",{})
FileM.save_as_file("getProvinceList.json",tmp.content.decode("utf-8"))
tmp=yt.request("getRadioList",{"categoryId":"0","provinceCode":"0"})
FileM.save_as_file("getRadioList.json",tmp.content.decode("utf-8"))
#"https://ytmsout.radio.cn/web/appBroadcast/list?categoryId=0&provinceCode=0"
#"https://ytmsout.radio.cn/web/appBroadcast/list?categoryId=0&provinceCode=0"
# req(url)