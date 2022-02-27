import re
import requests

class BaiduExpress:
    def __init__(self):
        self.url = "https://express.baidu.com/express/api/express"
        self.header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/98.0"
        }

    def get_token_v2(self):
        token_url = "https://www.baidu.com/s?tn=sitehao123&ie=UTF-8&wd=%E5%BF%AB%E9%80%92"
        result = requests.get(token_url, headers=self.header)
        return re.search('tokenV2=(.*)"', result.text).group(1), result.cookies
    
    def get_express_state(self, number, company):
        token_v2, cookie = self.get_token_v2()
        result = requests.get(self.url, headers=self.header, params={
            "tokenV2": token_v2,
            "appid": 4001,
            "nu": number,
            "com": company
        }, cookies=cookie).json()["data"]

        ret_dict = {
            "info": result["info"],
            "name": result["company"]["fullname"]
        }

        if (result["info"].get("state") and result["info"]["state"] == "0"):
            ret_dict["notice"] = result["notice"]
        return ret_dict

    def get_express_company(self, number):
        url = f"https://alayn.baidu.com/express/appdetail/autotip?&orderId={number}&sandbox=true"
        result = requests.get(url, headers=self.header).json()["data"]
        if (result.get("name")):
            return {
                "name": result["name"],
                "company": result["company"]
            }
        else:
            return {
                "name": "快递单号有误"
            }