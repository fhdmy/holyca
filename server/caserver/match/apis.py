import requests
from requests_toolbelt  import MultipartEncoder #multipart/form-data request
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import math
import json

class API:
    auth=""
    url="https://sc2replaystats.com"
    api_url="https://api.sc2replaystats.com"
    PHPSESSID=""
    sc2replayreferer=""
    season=0
    repstats_id=0
    battlenet_infos=defaultdict(lambda:0)
    email=""
    password=""
    reps=[]

    def __init__(self,email,password,auth):
        self.email=email
        self.password=password
        self.auth=auth
    
    def login(self):
        login_url=f"{self.url}/Account/signin"
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
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)
        if "Failed to login, please try your email and password again." in res.text:
            # print("login failed")
            return -1,self.battlenet_infos
        soup = BeautifulSoup(res.text, 'lxml')
        self.season=int(soup.find("input",id="seasons_id")["value"])
        re_repstats_id=re.findall(r'<a href=\"/account/display/.*\">', res.text)
        re_bn_opts=soup.find(id='account_name')
        re_bn_opts=re_bn_opts.find_all("option")
        self.battlenet_infos.clear()
        for k in re_bn_opts:
            self.battlenet_infos[k.text.split(" (")[0]]=k["value"]
        self.repstats_id=re_repstats_id[0][26:-2]
        self.PHPSESSID=session.cookies.get_dict()['PHPSESSID']
        self.sc2replayreferer=session.cookies.get_dict()['sc2replayreferer']
        # print(self.season,self.PHPSESSID,self.repstats_id,self.battlenet_infos)
        return self.repstats_id,self.battlenet_infos
    
    #获得近期rep
    def get_rep(self):
        game_type="All"
        bn_ids=""
        for name,nid in self.battlenet_infos.items():
            bn_ids+=(str(nid)+"-")
        bn_ids=bn_ids[:-1]
        rep_url=f"{self.url}/account/replays/{self.repstats_id}/0/{bn_ids}/1v1/{game_type}/{self.season}/"
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
            comp=re.compile(r"\[.*\] ")
            dt=str(tds[0].text)
            date=datetime.strptime(dt,"%d %b, %Y %I:%M %p")
            rep_map=str(tds[2].text)
            game_length=str(tds[3].text)
            race1=str(tds[4].find("span")['class'][1])
            race2=str(tds[5].find("span")['class'][1])
            if race1=='terran':
                race1="T"
            elif race1=='zerg':
                race1='Z'
            else:
                race1='P'
            if race2=='terran':
                race2="T"
            elif race2=='zerg':
                race2='Z'
            else:
                race2='P'
            vs_race=race1+"v"+race2
            player1=str(tds[4].find("a").text)
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
        # print(self.reps)
        return self.reps
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)

    def get_repinfo(self,rep_id):
        rep_url=f"{self.url}/replay/{rep_id}"
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
        players_info={}
        try:
            res=requests.get(rep_url,headers=req_header,cookies=cookie)
            soup = BeautifulSoup(res.text, 'lxml')
            # re_tbody=soup.find("tbody")
            # re_tds=re_tbody.find_all("td")
            # return re_tds[5].find("span").text
            re_section=soup.find("section",class_="container")
            re_table=re_section.find_all("table")[1]
            re_tbody=re_table.find("tbody")
            kill1=int(re_tbody.find_all("tr")[0].find_all("td")[6].text)
            kill2=int(re_tbody.find_all("tr")[1].find_all("td")[6].text)
            player1=re_tbody.find_all("tr")[0].find_all("td")[0].find("strong").text
            player2=re_tbody.find_all("tr")[1].find_all("td")[0].find("strong").text
            players_info[player1]=kill1
            players_info[player2]=kill2
            # print(players_info)
            return players_info
        except Exception as e:
            print(e)
            return ""
        
    
    def get_attack(self,bn_id):
        attack_url=f"{self.url}/account/ability/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/"
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
        attack=0
        try:
            res=requests.get(attack_url,headers=req_header,cookies=cookie)
            soup = BeautifulSoup(res.text, 'lxml')
            re_tbody=soup.find("table")
            re_tr=re_tbody.find_all("tr")
            for tr in re_tr:
                try:
                    title=tr.find_all("td")[0].text
                    if title=="attack":
                        attack=tr.find_all("td")[1].text.split(" ")[1][:-1]
                        break
                except Exception as e:
                    pass
            # print("attack: ",attack)
            return attack
        except Exception as e:
            print(e)
            return 0
    
    def get_general(self,bn_id):
        general_url=f"{self.url}/stats/runReport"
        # print(general_url)
        # general_url=f"{self.url}/account/display/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "referer":f"{self.url}account/display/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/",
            "authority":"sc2replaystats.com",
            "origin":"http://sc2replaystats.com"
        }
        cookie={
            "sc2replayreferer":self.sc2replayreferer,
            "PHPSESSID":self.PHPSESSID,
            "referer":f"{self.url}/account/display/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/"
        }
        # payload={
        #     "request":json.dumps({
        #         "metrics":["games","player_workers_avg","player_supply_block_time_avg"],
        #         "group_bys":[],
        #         "filters":{
        #             "account_id":{"logic":"equal","value":42919},
        #             "format":{"logic":"equal","value":"1v1"},
        #             "player_id":{"logic":"in","value":2633556},
        #             "season_id":{"logic":"relative","value":"current_season"}
        #         },
        #         "order":[],
        #         "date":"season_id:current_season",
        #         "settings":{"account_id":42919}
        #     })
        # }
        payload={
            "request":json.dumps({
                "metrics":["player_workers_avg","player_supply_block_time_avg"],
                "group_bys":[],
                "filters":{
                    "account_id":{"logic":"equal","value":self.repstats_id},
                    "format":{"logic":"equal","value":"1v1"},
                    "player_id":{"logic":"in","value":bn_id},
                    "season_id":{"logic":"relative","value":"current_season"}
                },
                "order":[],
                "date":"season_id:current_season",
                "settings":{"account_id":self.repstats_id}
            })
        }
        m=MultipartEncoder(payload)
        req_header['Content-Type'] = m.content_type
        variance,worker_created,supply_blocked=0,0,0
        try:
            res=requests.post(general_url,headers=req_header,cookies=cookie,data=m)
            soup = BeautifulSoup(res.text, 'lxml')
            # with open('./test.html', 'w') as f:
            #     f.write(res.text)
            # print(res.request.body)
            # print(json.loads(res.text))
            # print(json.loads(res.text)["results"]["data"])
            worker_created=int(json.loads(res.text)["results"]["data"][0]["player_workers_avg"])
            supply_blocked=int(json.loads(res.text)["results"]["data"][0]["player_supply_block_time_avg"])

        except Exception as e:
            print(e)

        payload={
            "request":json.dumps({
                "metrics":["account_matchup","games","win_loss_percentage"],
                "group_bys":["account_matchup"],
                "filters":{
                    "account_id":{"logic":"equal","value":self.repstats_id},
                    "format":{"logic":"equal","value":"1v1"},
                    "player_id":{"logic":"in","value":bn_id},
                    "replay_date":{"logic":"relative","value":"last_30_days"}
                },
                "order":[{"account_matchup":""}],
                "date":"replay_date:last_30_days",
                "settings":{"account_id":self.repstats_id}
            })
        }
        m=MultipartEncoder(payload)
        req_header['Content-Type'] = m.content_type

        try:
            res=requests.post(general_url,headers=req_header,cookies=cookie,data=m)
            soup = BeautifulSoup(res.text, 'lxml')
            with open('./test.html', 'w') as f:
                f.write(res.text)
            res_data=json.loads(res.text)["results"]["data"]
            race_sum=[[],[],[]] #p,t,z
            # print(res_data)
            for race_vs in res_data:
                if race_vs["account_matchup"].split("v")[0]=="P":
                    race_sum[0].append(race_vs["win_loss_percentage"].split(" ")[0])
                elif race_vs["account_matchup"].split("v")[0]=="T":
                    race_sum[1].append(race_vs["win_loss_percentage"].split(" ")[0])
                elif race_vs["account_matchup"].split("v")[0]=="Z":
                    race_sum[2].append(race_vs["win_loss_percentage"].split(" ")[0])
            top_race=[]
            sum_max=0
            for r in race_sum:
                temp_sum=0
                for i in r:
                    temp_sum+=(int(i.split("-")[0])+int(i.split("-")[1]))
                if temp_sum>sum_max:
                    sum_max=temp_sum
                    top_race=r
            
            winrates=[]
            for i in top_race:
                wins=int(i.split("-")[0])
                loses=int(i.split("-")[1])
                s=wins+loses
                if s==0:
                    winrates.append(50)
                    continue
                else:
                    winrates.append(round(wins*100/s,1))
            avg=0
            for i in winrates:
                avg+=i
            avg=round(avg/3,1)
            for i in winrates:
                variance+=(i-avg)**2
            variance=math.sqrt(100/(variance/3+1))

        except Exception as e:
            print(e)

        # print("general: ",worker_created,supply_blocked,variance)
        return worker_created,supply_blocked,variance
    
    def get_gamelength(self,bn_id):
        general_url=f"{self.url}/account/gamelength/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/"
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
        try:
            res=requests.get(general_url,headers=req_header,cookies=cookie)
            # with open('./test.html', 'w') as f:
            #     f.write(res.text)
            soup = BeautifulSoup(res.text, 'lxml')
            re_div=soup.find_all("div",{'class':'col-xs-6 col-sm-3 col-md-3'})
            win_rates=defaultdict(lambda:0)
            for d in re_div:
                re_gl=re.findall(r'<th>Wins/Losses</th>', str(d))
                if re_gl!="":
                    try:
                        w=int(d.find("tbody").find_all("tr")[3].find_all("td")[2].text[:-1])
                        win_rates[d.find("h4").text]=w
                    except:
                        pass
        except Exception as e:
            print(e)

        exponent=0
        s=1
        for item,text in win_rates.items():
            t=int(item.split(" min")[0].split(" - ")[0])
            if text==0:
                text=50
            exponent+=t*text
            s+=1
        # print("game_length: ",round(math.sqrt(exponent/s),1))
        return round(math.sqrt(exponent/s),1)
    
    def get_style(self,bn_id):
        attack=self.get_attack(bn_id)
        worker_created,supply_blocked,variance=self.get_general(bn_id)
        operation=round(worker_created/(supply_blocked+1),1)
        game_length=self.get_gamelength(bn_id)
        return attack,operation,game_length,variance
    
    def get_map_winrate(self,bn_id):
        general_url=f"{self.url}/account/maps/{self.repstats_id}/0/{bn_id}/1v1/All/{self.season}/"
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
        map_winrates=[]
        try:
            res=requests.get(general_url,headers=req_header,cookies=cookie)
            soup = BeautifulSoup(res.text, 'lxml')
            re_div=soup.find("div",class_="col-md-10")
            re_div=re_div.find_all("div",class_="col-xs-6 col-sm-4 col-md-4")
            map_winrates=[]
            for d in re_div:
                g_map=d.find("h2").find("span").text
                re_tr=d.find("table").find_all("tr")
                w=int(re_tr[-1].find_all("td")[2].text[:-1])
                map_winrates.append({
                    'g_map':g_map,
                    'winrate':w
                })
            # sort取前5
            for index,i in enumerate(map_winrates):
                for j in range(0,index):
                    if map_winrates[j]['winrate']<map_winrates[j+1]['winrate']:
                        temp=map_winrates[j]
                        map_winrates[j]=map_winrates[j+1]
                        map_winrates[j+1]=temp
        except Exception as e:
            print(e)
        # print("win_rates: ",map_winrates[0:5])
        return map_winrates[0:5]

        

def main():
    auth="ba729318a506a1ec476654053cf7e7483b1056df;eff1d56f879b05be0b8f53cf3aec7d65bffdc2fe;1584699974"
    email="holyca@126.com"
    password="HolyHolyCA"
    api=API(email,password,auth)
    api.login()
    # attack=api.get_attack(2860039)
    # worker_created,supply_blocked,variance=api.get_general(2633556)
    # operation=round(worker_created*5/(supply_blocked+10),1)
    # game_length=api.get_gamelength(2633556)
    # api.get_repinfo(13843563)
    # api.get_map_winrate(2633556)

if __name__=="__main__":
    main()

