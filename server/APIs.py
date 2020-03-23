import requests

class API:
    auth="b858c001e8961049919f500f84ff87f39a3ff7de;842e1835db42cc0044151199a5fc24be83ac4c6c;1584627749"
    url="https://sc2replaystats.com/"
    
    #登陆账号
    def login(self):
        login_url=self.url+"Account/signin"
        req_data={
            "email":"1256623447@qq.com",
            "password":"jch199669"
        }
        req_header={
            "Authorization":self.auth
        }
        res=requests.post(login_url,data=req_data,headers=req_header)
        print(res.text)

def main():
    api=API()
    api.login()

if __name__=="__main__":
    main()

