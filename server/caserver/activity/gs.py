import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import math

class GS:
    url="https://www.gosugamers.net"

    def get_matches(self):
        url="https://www.gosugamers.net/starcraft2/matches"
        req_header={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8",
        }
        res=requests.get(url,headers=req_header)
        soup = BeautifulSoup(res.text, 'lxml')
        match_list=soup.find("div",class_="grid-x match-list")
        matches=[]
        for item in match_list.children:
            match={}
            a=item.find("a")
            try:
                match["match_url"]=self.url+a["href"]
                grid_x=a.find("div").find("div",class_="match-info").find("div",class_="grid-x")
                player_1=grid_x.find("div",class_="cell").find("span",class_="team-1").text.strip()
                player_2=grid_x.find("div",class_="cell").find("span",class_="team-2").text.strip()
                match["player_1"]=player_1
                match["player_2"]=player_2
                tournament=grid_x.find("div",class_="cell match-tournament").text.strip()
                match["tournament"]=tournament
                dt=a.find("div",class_="match-status").find("span").text.strip()
                time=dt
                if dt!="Live":
                    dt=a.find("div",class_="match-status").find("span").find("time")["datetime"].split("+")[0]
                    time=datetime.strptime(dt,"%Y-%m-%dT%H:%M:%S")+timedelta(hours=7)
                match["time"]=time
                matches.append(match)
            except:
                #一定会产生关于a["href"]的exception
                continue
        return matches
    
    def get_results(self,match_url):
        req_header={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8",
        }
        res=requests.get(match_url,headers=req_header)
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            players_wrapper=soup.find_all("div",class_="cell match finished")[0]
            player1=players_wrapper.find_all("h2")[0].find("a").text.strip()
            player2=players_wrapper.find_all("h2")[1].find("a").text.strip()
            score_wrapper=soup.find_all("div",class_="score")[0]
            score1=score_wrapper.find_all("span")[0].text.strip()
            score2=score_wrapper.find_all("span")[1].text.strip()
            score=score1+":"+score2
            winner=player1 if score1>=score2 else player2
            print(f"winner: {winner} score:{score}")
            return winner,score
        except Exception as e:
            print(e)
            return "",""
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)

def main():
    gs=GS()
    matches=gs.get_matches()
    # for match in matches:
    #     gs.get_results(match["match_url"])
    
if __name__=="__main__":
    main()

