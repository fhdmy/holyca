import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import math

class TL:
    url="https://liquipedia.net"

    def get_upcoming_rep(self):
        url="https://liquipedia.net/starcraft2/Liquipedia:Upcoming_and_ongoing_matches"
        req_header={
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "authority":"liquipedia.net"
        }
        res=requests.get(url,headers=req_header)
        soup = BeautifulSoup(res.text, 'lxml')
        re_wrapper=soup.find_all("div",id="infobox_matches")[-1]
        matches=[]
        for table in re_wrapper.find_all("table"):
            try:
                match={}
                # team_left=table.find("td",class_="team-left")
                # team_right=table.find("td",class_="team-right")

                # re_span1=team_left.find_all("span")
                # re_span2=team_right.find_all("span")
                # match["player1"]=re_span1[0].text
                # match["player2"]=re_span2[-1].text
                # a1=team_left.find_all("a")
                # a2=team_right.find_all("a")
                # if match["player1"]=="TBD" or match["player2"]=="TBD" or len(a1)==2 or len(a2)==2:  #len(a)==2时，为战队
                #     continue
                # match["player1_link"]=self.url+re_span1[0].find("a")["href"]
                # match["player2_link"]=self.url+re_span2[-1].find("a")["href"]
                # match["player1_race"]=a1[1]["href"].split("/")[-1]
                # match["player2_race"]=a2[1]["href"].split("/")[-1]
                # match["player1_raceimg"]=self.url+a1[1].find("img")["src"]
                # match["player2_raceimg"]=self.url+a2[1].find("img")["src"]
                # match["player1_ctryimg"]=self.url+re_span1[-1].find("img")["src"]
                # match["player2_ctryimg"]=self.url+re_span2[0].find("img")["src"]

                #时间和比赛名称
                team_more=table.find("td",class_="match-filler")
                dt=team_more.find("span",class_="match-countdown")
                dt=dt.find("span",class_="timer-object").text.strip()
                try:
                    time=datetime.strptime(dt,"%b %d, %Y - %H:%M UTC")+timedelta(hours=8)
                except:
                    time=datetime.strptime(dt,"%B %d, %Y - %H:%M UTC")+timedelta(hours=8)
                match["match_time"]=time
                match_name_wrapper=team_more.find("div")
                match["match_name"]=match_name_wrapper.find("div").find("a").text.strip()
                # print(match)
                matches.append(match)
            except Exception as e:
                print(e)
        return matches   
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)

    # def get_matchresult(self,player1_link,player2):
    #     url1=player1_link+"/Matches"
    #     req_header={
    #         "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    #         "authority":"liquipedia.net"
    #     }
    #     res=requests.get(url1,headers=req_header)
    #     soup = BeautifulSoup(res.text, 'lxml')
    #     table=soup.find("div",id="mw-content-text").find("table")
    #     for tr in table.find_all("tr"):
    #         td=tr.find_all("td")
    #         vs_player=""
    #         if len(td)==0:
    #             continue
    #         vs_a=td[-2].find_all("span")[-1].find("a")
    #         if vs_a:
    #             vs_player=self.url + vs_a["href"]
            
    #         date=td[0].text
    #         time=td[1].text
    #         print(date,time)
        # with open('./test.html', 'w') as f:
        #     f.write(res.text)
        

def main():
    tl=TL()
    tl.get_upcoming_rep()
    # tl.get_matchresult("https://liquipedia.net/starcraft2/TY","https://liquipedia.net/starcraft2/Solar")

if __name__=="__main__":
    main()

