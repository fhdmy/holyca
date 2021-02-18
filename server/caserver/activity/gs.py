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
                    time=datetime.strptime(dt,"%m/%d/%y, %I:%M %p")+timedelta(hours=6)
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
            winner=soup.find("div",id="gosubetSpoiler").text.strip().split(" ")[1]
            score=soup.find_all("div",class_="score")[0]
            score=score.find_all("span")[0].text.strip()+":"+score.find_all("span")[1].text.strip()
            # print(f"winner: {winner} score:{score}")
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

