import requests
import json, time
from urllib import parse

token = 'RGAPI-85d35a9f-efb2-469f-a55a-a83da1eaeda7'
name = '안잘하는사람'
url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name
request_headers = {
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": token
}
 
 
def check_my_team(*args):
    current_players = []
    for n in range(0, 1):
        name = args[n]
        print(name)
        encoded_name = parse.quote(name)
        current_players.append(encoded_name)
        summoner_account_id = requests.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encoded_name, headers=request_headers).json()["accountId"]


        win = 0
        for n in range(0, 10):
            get_latest_match_id = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id, headers=request_headers).json()["matches"][n]["gameId"]
            get_match_info = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(get_latest_match_id), headers=request_headers).json()
            for i in range(0, 10):
                if get_match_info["participantIdentities"][i]["player"]["summonerName"] == name:
                    if get_match_info["participants"][i]["stats"]["win"] == True:
                        win += 1
            time.sleep(1)
        print(win)
        time.sleep(2)
            
        latest_players = []
        for n in range(0, 10):
            get_latest_match_id = requests.get("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoner_account_id, headers=request_headers).json()["matches"][0]["gameId"]
            get_match_info = requests.get("https://kr.api.riotgames.com/lol/match/v4/matches/" + str(get_latest_match_id), headers=request_headers).json()
            latest_players.append(get_match_info["participantIdentities"][n]["player"]["summonerName"])
            time.sleep(1)
        print(latest_players)
        if len(set(current_players) & set(latest_players)) > 1:
            print(set(current_players) & set(latest_players))
        else:
            print("듀오가 없습니다")
        time.sleep(2)


def getUserInfo(summonId):
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonId
    res = requests.get(URL, headers={"X-Riot-Token": token})
    
    return res

def getSummonerInfo(summonId):
    URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+summonId
    res = requests.get(URL, headers={"X-Riot-Token": token})
    
    return res
#tmp = getUserInfo('HawardStark')['name']
#print(tmp)


def check_members():
    global name

    #name = '동냥아치'
    
    encoded_name = parse.quote(name)

    response = requests.get(url, headers={"X-Riot-Token": token})
    #response = requests.get(url, headers=request_headers)
    resobj = response.json()
    
    print(resobj)
    URL = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"+resobj["id"]
    res = requests.get(URL, headers={"X-Riot-Token": token})
    
    live_game = res.json()
    ask = ''
    
    ask += ''+live_game['gameLength']

    #print('게임모드 : {}'.format(live_game['gameType']))
    for n in range(0, 10):
        #summonerName = parse.quote(live_game["participants"][n]["summonerName"])
        summonerName = live_game["participants"][n]["summonerName"]
        summonerId = live_game["participants"][n]["summonerId"]
        teamId = live_game["participants"][n]["teamId"]

        URL = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/'+summonerId
        res = requests.get(URL, headers={"X-Riot-Token": token})
        summonerInfo = res.json()

        """if teamId == 100:
            print('RED team : ', end='')
        elif teamId == 200:
            print('BLUE team : ', end='')
        
        print(summonerInfo)
        print(summonerName, end=' : <')
        print(summonerInfo['tier'], end=' ')
        print(summonerInfo['rank'], end='> ')
        print(summonerInfo['wins'], end='승, ')
        print(summonerInfo['losses'], end='패\r\n')
        current_players.append(summonerName)"""


#check_members()

def matchList(summonerName):
    userinfo = getUserInfo(summonerName)
    
    puuid = 'v_29viDOu36fR2izZ_7NloIINKwg1UBPBYEyeamC_vIHcAciC7FgfqWll-J-RcKx5HeERrfwehuiiA'
    puuid = userinfo.json()['puuid']
    URL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start=0&count=20".format(puuid)
    res = requests.get(URL, headers={"X-Riot-Token": token})
    response = res.json()
    print(response)
    for txt in response:
        URL = "https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"

def checkActiveGame(summonerId):
    URL = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"+summonerId
    res = requests.get(URL, headers={"X-Riot-Token": token})
    rankinfo = json.loads(res.text)
    ask = ''

    ask += "소환사 이름: "+name+"\r\n"
    for i in rankinfo:
        print(i["queueType"])
        if i["queueType"] == "RANKED_SOLO_5x5":
            #솔랭과 자랭중 솔랭
            ask += "솔로랭크:"
            ask += '티어: {} {}'.format(i["tier"], i["rank"])
            ask += '승: {}판, 패: {}판'.format(i["wins"], i["losses"])
        else:
            # 솔랭과 자랭중 자랭
            ask += "자유랭크:"
            ask += '티어: {} {}'.format(i["tier"], i["rank"])
            ask += '승: {}판, 패: {}판'.format(i["wins"], i["losses"])



#check_my_team('장씨가문 장남')
#check_members()
