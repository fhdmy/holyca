import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta

class API:
    auth=""
    url="https://sc2replaystats.com/"
    PHPSESSID=""
    sc2replayreferer=""
    season=0
    repstats_id=0
    battlenet_infos=[]
    email=""
    password=""
    reps=[]

    def __init__(self,email,password,auth):
        self.email=email
        self.password=password
        self.auth=auth
    
    #登陆账号
    def login(self):
        login_url=self.url+"Account/signin"
        req_data={
            "email":self.email,
            "password":self.password
        }
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer":"https://sc2replaystats.com/Account/signin",
            "authority":"sc2replaystats.com",
            "origin":"https://sc2replaystats.com"
        }
        session = requests.Session()
        res=session.post(login_url,data=req_data,headers=req_header)
        re_season=re.findall(r'<h2>Season <strong>.*?</strong> Quick Statistics</h2>', res.text)
        self.season=re_season[0][19:-31]
        re_repstats_id=re.findall(r'<a href=\"/account/display/.*\">', res.text)
        soup = BeautifulSoup(res.text, 'lxml')
        re_bn_opts=soup.find(id='account_name')
        re_bn_opts=re_bn_opts.find_all("option")
        self.battlenet_infos.clear()
        for k in re_bn_opts:
            self.battlenet_infos.append(
            {
                "name":k.text.split(" (")[0],
                "id":k["value"]
            })
        self.repstats_id=re_repstats_id[0][26:-2]
        self.PHPSESSID=session.cookies.get_dict()['PHPSESSID']
        self.sc2replayreferer=session.cookies.get_dict()['sc2replayreferer']
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)
        return self.repstats_id,self.battlenet_infos
    
    #获得近期rep
    def get_rep(self):
        game_type="All"
        bn_ids=""
        for index,content in enumerate(self.battlenet_infos):
            if index==len(self.battlenet_infos)-1:
                bn_ids+=(str(content["id"]))
            else:
                bn_ids+=(str(content["id"])+"-")
        rep_url=self.url+"account/replays/"+str(self.repstats_id)+"/0/"+bn_ids+"/1v1/"+game_type+"/"+str(self.season)+"/"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer":"https://sc2replaystats.com/Account/signin",
            "authority":"sc2replaystats.com",
            "origin":"https://sc2replaystats.com"
        }
        cookie={
            "sc2replayreferer":self.sc2replayreferer,
            "PHPSESSID":self.PHPSESSID
        }
        res=requests.get(rep_url,headers=req_header,cookies=cookie)
        soup = BeautifulSoup(res.text, 'lxml')
        re_tbody=soup.find("tbody")
        re_tr=re_tbody.find_all("tr")
        self.reps.clear()
        for row in re_tr:
            tds=row.find_all("td")
            dt=str(tds[0].text)
            date=datetime.strptime(dt,"%d %b, %Y %I:%M %p")
            rep_map=str(tds[2].text)
            game_length=str(tds[3].text)
            vs_race=str(tds[7].text)
            player1=str(tds[4].find("a").text)
            comp=re.compile(r"\[.*\] ")
            player1=comp.sub("",player1)
            player1_id=str(tds[4].find("a")["href"].split("/")[2])
            player1_mmr=str(tds[4].find("a")["title"].split(" ")[2].replace(",",""))
            player2=str(tds[5].find("a").text)
            player2=comp.sub("",player2)
            player2_id=str(tds[5].find("a")["href"].split("/")[2])
            player2_mmr=str(tds[5].find("a")["title"].split(" ")[2].replace(",",""))
            rep_id=str(tds[6].find("a")["href"].split("/")[2])
            w1=len(tds[4].find_all("span"))
            w2=len(tds[5].find_all("span"))
            if w1==3:
                winner=player1
            elif w2==3:
                winner=player2
            else:
                winner="平局"
            self.reps.append(
            {
                "rep_id":rep_id,
                "date":date,
                "rep_map":rep_map,
                "game_length":game_length,
                "vs_race":vs_race,
                "player1":player1,
                "player1_id":player1_id,
                "player1_mmr":player1_mmr,
                "player2":player2,
                "player2_id":player2_id,
                "player2_mmr":player2_mmr,
                "winner":winner
            })
        return self.reps
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)

    def get_repinfo(self,rep_id):
        rep_url=self.url+"replay/"+rep_id
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer":"https://sc2replaystats.com/Account/signin",
            "authority":"sc2replaystats.com",
            "origin":"https://sc2replaystats.com"
        }
        cookie={
            "sc2replayreferer":self.sc2replayreferer,
            "PHPSESSID":self.PHPSESSID
        }
        res=requests.get(rep_url,headers=req_header,cookies=cookie)
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)
        soup = BeautifulSoup(res.text, 'lxml')
        re_tbody=soup.find("tbody")
        re_tds=re_tbody.find_all("td")
        return re_tds[5].find("span").text

def main():
    auth="ba729318a506a1ec476654053cf7e7483b1056df;eff1d56f879b05be0b8f53cf3aec7d65bffdc2fe;1584699974"
    email="holyca@126.com"
    password="HolyHolyCA"
    api=API(email,password,auth)
    api.login()
    # api.get_rep()

if __name__=="__main__":
    main()

