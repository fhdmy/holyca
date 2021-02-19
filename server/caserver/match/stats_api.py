import requests
from bs4 import BeautifulSoup
import json
#abandon api

class API:
    auth=""
    email=""
    password=""
    url="https://api.sc2replaystats.com"

    def __init__(self,email,password,auth):
        self.email=email
        self.password=password
        self.auth=auth
    
    '''
    token: 08c08ccd1ea337612ef71dd6ac076c22b4e410eb;dcdef01634f7f98e5270cccd93473380ec283101;1584627749
    '''
    def login(self):
        token=""
        func_url=f"{self.url}/account/login"
        req_data={
            "email_address":self.email,
            "password":self.password
        }
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }
        res=requests.post(func_url,data=req_data,headers=req_header)
        try:
            token=json.loads(res.text)["token"]
        except Exception as e:
            print(e)
        return token
    
    '''
    player: 
    {
        "player":
        {
            "players_replays_url":"https:\/\/sc2replaystats.com\/player\/2275521?tab=replays",
            "players_id":2275521,
            "players_name":"llllllllllll",
            "battle_net_url":"http:\/\/kr.battle.net\/sc2\/en\/profile\/6168518\/1\/llllllllllll\/",
            "legacy_link_id":6168518,
            "character_link_id":6168518,
            "legacy_link_realm":1,
            "battle_tag_name":"Xnick",
            "battle_tag_id":4111,
            "legacy_battle_tag_name":"llllllllllll",
            "updated_at":"2020-03-22T05:44:11-06:00"},
            "players_id":2275521,
            "default":0
        }
    }
    '''
    def account_players(self):
        rtn_players=[]
        func_url=f"{self.url}/account/players"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }
        res=requests.get(func_url,headers=req_header)
        players=json.loads(res.text)
        try:
            for player in players:
                # print(player)
                rtn_players.append({
                    "players_id":player["player"]["players_id"],
                    "players_name":player["player"]["players_name"],
                    "battle_tag_name":player["player"]["battle_tag_name"],
                    "battle_tag_id":player["player"]["battle_tag_id"],
                })
            # print(rtn_players)
            return rtn_players
        except Exception as e:
            print(e)
        
    '''
    res.text:
    {
        "players_replays_url":"https:\/\/sc2replaystats.com\/player\/2275521?tab=replays",
        "players_id":2275521,
        "players_name":"llllllllllll",
        "battle_net_url":"http:\/\/kr.battle.net\/sc2\/en\/profile\/6168518\/1\/llllllllllll\/",
        "legacy_link_id":6168518,
        "character_link_id":6168518,
        "legacy_link_realm":1,
        "battle_tag_name":"Xnick",
        "battle_tag_id":4111,
        "legacy_battle_tag_name":"llllllllllll",
        "clan":null,
        "updated_at":"2020-03-22T05:44:11-06:00"
    }
    '''
    def player_info(self,players_id):
        rtn_info={}
        func_url=f"{self.url}/player/{players_id}"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }
        res=requests.get(func_url,headers=req_header)
        info=json.loads(res.text)
        try:
            rtn_info["players_id"]=info["players_id"]
            rtn_info["players_name"]=info["players_name"]
            rtn_info["battle_tag_name"]=info["battle_tag_name"]
            rtn_info["battle_tag_id"]=info["battle_tag_id"]
            rtn_info["clan"]=info["clan"]
            # print(res.text)
            print(rtn_info)
            return rtn_info
        except Exception as e:
            print(e)
    
    '''
    res.text:
    {
        "page":1,
        "items_per_page":25,
        "total_items":1619,
        "items":
        [
            {
                "game_length":2,
                "replay_id":11538963,
                "maps_id":2270,
                "map_name":"\u6ee8\u6d77\u536b\u57ce-\u5929\u68af\u7248",
                "format":"1v1",
                "game_type":"AutoMM",
                "winning_player":"llllllllllll",
                "seasons_id":40,
                "replay_date":"2019-07-03T22:54:42-06:00",
                "replay_version":"4.9.2.74741",
                "hit_count":null,
                "last_viewed":null,
                "downloads":null,
                "events_events_id":null
            },
            {
                "game_length":827,
                "replay_id":11538974,
                "maps_id":2270,
                "map_name":"Acropolis LE",
                "format":"1v1",
                "game_type":"AutoMM",
                "winning_player":"llllllllllll",
                "seasons_id":40,
                "replay_date":"2019-06-07T07:37:43-06:00",
                "replay_version":"4.9.1.74456",
                "hit_count":null,
                "last_viewed":null,
                "downloads":null,
                "events_events_id":null
            },
            ...
        ]
    }
    '''
    def account_replays(self):
        func_url=f"{self.url}/replay"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }
        res=requests.get(func_url,headers=req_header)
        print(res.text)
    
    '''
    res.text:
    {
        "replay_url":"https:\/\/sc2replaystats.com\/replay\/11538974",
        "game_length":827,
        "replay_id":11538974,
        "map_name":"Acropolis LE",
        "format":"1v1",
        "game_type":"AutoMM",
        "winning_player":"llllllllllll",
        "players":
        [
            {
                "players_id":2275521,
                "clan":"",
                "race":"T",
                "mmr":4693,
                "division":"diamond",
                "server_rank":2348,
                "global_rank":11373,
                "apm":265,
                "team":1,
                "winner":1,
                "color":"180,20,30"
            },
            {
                "players_id":389051,
                "clan":"",
                "race":"T",
                "mmr":4323,
                "division":"diamond",
                "server_rank":4494,
                "global_rank":23425,
                "apm":209,
                "team":2,
                "winner":0,
                "color":"0,66,255"
            }
        ],
        "seasons_id":40,
        "replay_date":"2019-06-07T07:37:43-06:00",
        "replay_version":"4.9.1.74456",
        "hit_count":null,
        "last_viewed":null,
        "downloads":null,
        "events_events_id":null
    }
    '''
    def replay_info(self,replay_id):
        func_url=f"{self.url}/replay/{replay_id}"
        req_header={
            "Authorization":self.auth,
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }
        res=requests.get(func_url,headers=req_header)
        print(res.text)

def main():
    auth="08c08ccd1ea337612ef71dd6ac076c22b4e410eb;dcdef01634f7f98e5270cccd93473380ec283101;1584627749"
    # auth=""
    email="1256623447@qq.com"
    password="Jch199669"
    api=API(email,password,auth)
    # print(api.login())
    api.player_info(2275521)
    # api.account_players()
    # api.account_replays()
    # api.replay_info(11538974)

if __name__=="__main__":
    main()