from asyncio.windows_events import NULL
import lol_api, manage_data
import discord
import random

from discord.channel import DMChannel
from discord.ext import commands

import pandas as pd



def getPosIndex(p_str):
    if p_str == '탑':
        return 0
    elif p_str == '정글':
        return 1
    elif p_str == '미드':
        return 2
    elif p_str == '원딜':
        return 3
    elif p_str == '서폿':
        return 4
    return -1

def getPosName(p_idx):
    if p_idx == 0:
        return '탑'
    elif p_idx == 1:
        return '정글'
    elif p_idx == 2:
        return '미드'
    elif p_idx == 3:
        return '원딜'
    elif p_idx == 4:
        return '서폿'
    return ''


def tierPoint(tier_, rank_, position_):
    table = [[0 for row in range(0, 5)] for col in range(0, 9)]
    row_t = 8
    col_t = 4

    tier_ = tier_.lower()
    #rank_ = rank_.lower()

    table[0] = [49, 62, 59, 54, 48]
    table[1] = [45, 56, 54, 49, 45]
    table[2] = [42, 50, 48, 43, 43]
    table[3] = [36, 41, 40, 36, 37]
    table[4] = [29, 32, 32, 29, 29]
    table[5] = [22, 25, 24, 22, 25]
    table[6] = [17, 13, 16, 14, 17]
    table[7] = [9, 5, 8, 7, 13]
    table[8] = [0, 0, 0, 2, 7]

    if (tier_ == 'challnger' or tier_ == 'grand master' or tier_ == 'master'):
        row_t = 0
    elif tier_ == 'diamond' and rank_ == 'I':
        row_t = 2
    elif tier_ == 'diamond' and (rank_ == 'I' or rank_ == 'II'):
        row_t = 3
    elif tier_ == 'diamond' and (rank_ == 'IV' or rank_ == 'V'):
        row_t = 4
    elif tier_ == 'platinum' and (rank_ == 'I' or rank_ == 'II' or rank_ == 'III'):
        row_t = 4
    elif tier_ == 'platinum' and (rank_ == 'IV' or rank_ == 'V'):
        row_t = 5
    elif tier_ == 'gold' and (rank_ == 'I' or rank_ == 'II' or rank_ == 'III'):
        row_t = 5
    elif tier_ == 'gold' and (rank_ == 'IV' or rank_ == 'V'):
        row_t = 6
    elif tier_ == 'silver' and (rank_ == 'I' or rank_ == 'II' or rank_ == 'III'):
        row_t = 6
    elif tier_ == 'silver' and (rank_ == 'IV' or rank_ == 'V'):
        row_t = 7
    elif tier_ == 'bronze' and (rank_ == 'I' or rank_ == 'II' or rank_ == 'III'):
        row_t = 7
    else:
        row_t = 8

    col_t = position_ #getPosIndex(position_)

    return table[row_t][col_t]

def canMakeTeams(players):
    list_ = []

    for pl in players:
        userId = pl['userId']
        name = pl['summonerName']
        tier = pl['tier']
        rank = pl['rank']
        position = pl['position']
        list_.append({'userId':userId, 'chk':False, 'name':name, 'tier':tier, 'rank':rank, 'position':position})

    def rec2(list__, pls):
        tmp = list__

        if len(tmp) == 10:
            return True

        for idx in range(0, len(pls)):
            if pls[idx]['chk']:
                continue
            pls[idx]['chk'] = True
            for i in pls[idx]['position']:
                if len(tmp)%5 == getPosIndex(i):
                    tmp.append(pls[idx])
                    if rec2(tmp, pls) == True:
                        return True
                    tmp.pop()
            pls[idx]['chk'] = False

        return False

    return rec2([], list_)



def makeTeams(players):
    recommended_team = []
    team_gap = 10000
    list_ = []
    ask = ''

    def rec(list__, pls):
        tmp = list__

        if len(tmp) == 10:
            nonlocal team_gap

            tmp_gap = calcTeamsGap(tmp)

            if tmp_gap < team_gap:
                nonlocal recommended_team
                nonlocal ask

                ask = showme(tmp)
                recommended_team = tmp
                print(showme(tmp))
            return

        for idx in range(0, len(pls)):
            if pls[idx]['chk']:
                continue
            pls[idx]['chk'] = True
            for i in pls[idx]['position']:
                if len(tmp)%5 == getPosIndex(i):
                    tmp.append(pls[idx])
                    rec(tmp, pls)
                    tmp.pop()
            pls[idx]['chk'] = False

        return


    for pl in players:
        userId = pl['userId']
        name = pl['summonerName']
        tier = pl['tier']
        rank = pl['rank']
        position = pl['position']
        list_.append({'userId':userId, 'chk':False, 'name':name, 'tier':tier, 'rank':rank, 'position':position})

    rec([], list_)

    return ask


def calcTeamsGap(teams):
    team1_val = 0
    team2_val = 0

    for i in range(0, 5):
        team1_val += tierPoint(teams[i]['tier'], teams[i]['rank'], i)
    for i in range(5, 10):
        team2_val += tierPoint(teams[i]['tier'], teams[i]['rank'], i%5)

    return abs(team1_val - team2_val)

def showme(tmp):
    ask = ''

    team_val = 0
    for i in range(0, 5):
        team_val += tierPoint(tmp[i]['tier'], tmp[i]['rank'], i%5)
    ask += '=\r\n▶RED TEAM (팀 포인트 : {}pt)\r\n'.format(team_val)

    for i in range(0, 5):
        ask += '▷{} <{} {}> : {}'.format(tmp[i]['name'], tmp[i]['tier'], tmp[i]['rank'], getPosName(i%5))
        ask += '({}pt)\r\n'.format(tierPoint(tmp[i]['tier'], tmp[i]['rank'], i%5))


    team_val = 0
    for i in range(5, 10):
        team_val += tierPoint(tmp[i]['tier'], tmp[i]['rank'], i%5)
    ask += '\r\n▶BLUE TEAM (팀 포인트 : {}pt)\r\n'.format(team_val)

    for i in range(5, 10):
        ask += '▷{} <{} {}> : {}'.format(tmp[i]['name'], tmp[i]['tier'], tmp[i]['rank'], getPosName(i%5))
        ask += '({}pt)\r\n'.format(tierPoint(tmp[i]['tier'], tmp[i]['rank'], i%5))

    return ask


if __name__ == '__main__':

    client = discord.Client()
    manage_data.loadData()

    civil_war_players = []
    civil_war_players.clear()
    civil_war_players.append({'userId': 39711001835602023, 'summonerName': 'HawardStark3', 'tier': 'SILVER', 'rank': 'IV', 'position': ['정글', '탑']})
    civil_war_players.append({'userId': 39711001835602024, 'summonerName': 'HawardStark4', 'tier': 'Bronze', 'rank': 'V', 'position': ['미드', '원딜', '서폿']})
    civil_war_players.append({'userId': 39711001835602025, 'summonerName': 'HawardStark5', 'tier': 'Gold', 'rank': 'II', 'position': ['원딜', '서폿']})
    civil_war_players.append({'userId': 39711001835602026, 'summonerName': 'HawardStark6', 'tier': 'Gold', 'rank': 'I', 'position': ['미드']})
    civil_war_players.append({'userId': 39711001835602027, 'summonerName': 'HawardStark7', 'tier': 'SILVER', 'rank': 'I', 'position': ['원딜']})
    civil_war_players.append({'userId': 39711001835602028, 'summonerName': 'HawardStark8', 'tier': 'Bronze', 'rank': 'III', 'position': ['정글', '미드']})
    civil_war_players.append({'userId': 39711001835602029, 'summonerName': 'HawardStark9', 'tier': 'Bronze', 'rank': 'III', 'position': ['미드', '원딜', '탑']})
    civil_war_players.append({'userId': 39711001835602020, 'summonerName': 'HawardStark10', 'tier': 'SILVER', 'rank': 'II', 'position': ['미드', '원딜']})
    civil_war_players.append({'userId': 39711001835602021, 'summonerName': '동이스', 'tier': 'GOLD', 'rank': 'I', 'position': ['탑']})
    
    #civil_war_players.clear()
    #makeTeams(civil_war_players)

    
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client)) #봇이 실행되면 콘솔창에 표시

    @client.event
    async def on_message(message):
        if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
            return

        image = NULL


        if message.content.startswith('!'):
            recieve_message = message.content[1:]
            splited = recieve_message.split(' ')

            if message.author.id == 353579214517174273:
                image = discord.File("1640e6d4cd62c161.gif", filename="1640e6d4cd62c161.gif")
                recieve_message = '동희야 명령어 똑바로 치랬지!!!'
            else:
                #image = discord.File("1640e6d4cd62c161.gif", filename="1640e6d4cd62c161.gif")
                recieve_message = '잘못된 명령어입니다.'

            """elif splited[0] == '오늘의승률':
                userId = message.author.id
                summonerName = manage_data.getSummonerName(userId)
                recieve_message = lol_api.matchList('주사위쫌굴려바')
                print(recieve_message)

                if splited[1] == 'DBG':
                    recieve_message = lol_api.getUserInfo(message.author.id).str
                elif splited[1] == '내전':
                    recieve_message = lol_api.getUserInfo(message.author.id).str
            elif splited[0] == '게임현황':
                recieve_message = lol_api.getUserInfo(message.author.id).str"""



            #if random.randint(1, 50) == 37:
            #    image = discord.File("1640e6d4cd62c161.gif", filename="1640e6d4cd62c161.gif")

            if image != NULL:
                await message.channel.send(recieve_message, file=image)
            else:
                await message.channel.send(recieve_message)


    game = discord.Game('DBG 재결합')
    client = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('잘못된 명령어입니다.')
        

    @client.command(aliases=['등록'])
    async def registId(ctx, *text):
        userId = ctx.author.id
        userName = ctx.author

        summonerName = ''
        for t in text:
            summonerName += t


        userInfo = lol_api.getUserInfo(summonerName)
        
        if userInfo.status_code == 200:
            if manage_data.isReigisted(userId) == False:
                userInfo = userInfo.json()
                manage_data.insertUser(userId, userName, userInfo['id'], summonerName)
                manage_data.saveData()
                recieve_message = '성공적으로 등록되었습니다.'
            else:
                userInfo = userInfo.json()
                manage_data.setSummonerName(userId, summonerName)
                manage_data.setSummonerId(userId, userInfo['id'])
                manage_data.saveData()
                recieve_message = '[{}]님의 계정이 [{}]로 변경되었습니다.'.format(userName, summonerName)
        elif userInfo.status_code == 404:
            recieve_message = '존재하지 않는 소환사 닉네임입니다.'
        else:
            recieve_message = 'Error code : '+userInfo.status_code
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['참가', 'join'])
    async def joinCivilWar(ctx, *text):
        chk = False
        userId = ctx.author.id

        for i in civil_war_players:
            print(i)
            if i['userId'] == userId:
                chk = True

        if chk:
            recieve_message = '이미 내전 참가신청을 하셨습니다.'
        else:
            summonerName = manage_data.getSummonerName(userId)
            summonerInfo = lol_api.getSummonerInfo(manage_data.getSummonerId(userId)).json()
            
            tier = summonerInfo[len(summonerInfo)-1]['tier']
            rank = summonerInfo[len(summonerInfo)-1]['rank']
            positions = [] #summonerInfo['position']
            civil_war_players.append({'userId':userId, 'summonerName':summonerName, 'tier':tier, 'rank':rank, 'position':positions})

            recieve_message = '[{}]님이 내전에 참가하셨습니다.'.format(ctx.author)
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['포지션', '포지션설정'])
    async def setPositions(ctx, *text):
        userId = ctx.author.id
        idx = True


        idx = civil_war_players[civil_war_players['userId'] == userId].empty
        print(idx)

        if idx:
            recieve_message = '포지션설정은 참가신청 이후에 가능합니다.'
        else:
            tmp_pos = []
            for t in text:
                if t == '탑' or t == '정글' or t == '미드' or t == '원딜' or t == '서폿':
                    tmp_pos.append(t)

            civil_war_players.loc[civil_war_players['userId'] == userId, 'position'] = tmp_pos

            recieve_message = '[{}]님의 포지션이 {}로 설정되었습니다.'.format(civil_war_players[idx]['summonerName'], tmp_pos)
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['등록멤버', 'DBG멤버'])
    async def show_registed_members(ctx):
        registedMembers = manage_data.getAllData()
        if len(registedMembers) <= 0:
            recieve_message = '내전멤버가 없습니다.'
        else:
            recieve_message = ''

            print(registedMembers)
            for i, row in registedMembers.iterrows():
                summonerInfo = lol_api.getSummonerInfo(registedMembers['summonerId'][i]).json()
                tier = summonerInfo[len(summonerInfo)-1]['tier']
                rank = summonerInfo[len(summonerInfo)-1]['rank']

                recieve_message += '[{}] <{} {}>\r\n'.format(registedMembers['summonerName'][i], tier, rank)
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['내전멤버', '내전팀멤버'])
    async def show_members(ctx):
        if len(civil_war_players) <= 0:
            recieve_message = '내전멤버가 없습니다.'
        else:
            recieve_message = ''
            for i in civil_war_players:
                recieve_message += '[{}] <{} {}> : {}\r\n'.format(i['summonerName'], i['tier'], i['rank'], i['position'])
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['내전팀분배', '내전팀생성'])
    async def separate_teams(ctx):
        if len(civil_war_players) != 10:
            recieve_message = '내전 진행을 위해서는 멤버가 정확히 10명이여야합니다.'
        else:
            if canMakeTeams(civil_war_players):
                recieve_message = makeTeams(civil_war_players)
            else:
                recieve_message = '팀생성이 불가능합니다. 포지션을 다시 설정해주세요.'
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['내전초기화', '멤버초기화'])
    async def reset_members(ctx):
        civil_war_players.clear()
        recieve_message = '내전 참가자 목록이 초기화되었습니다.'
        await ctx.channel.send(recieve_message)
        

    @client.command(aliases=['DBG'])
    async def dbg_assemble(ctx, text):
        if text == 'assemble':
            recieve_message = '[{}]님이 DBG 소집을 요청하였습니다. 현재 모인 멤버는 총 {}명입니다. @everyone'.format(ctx.author, len(civil_war_players))
            image = discord.File("1611403576434.png", filename='1611403576434.png')
        await ctx.channel.send(recieve_message, file=image)
        

    @client.command(aliases=['티어표'])
    async def tier_table(ctx):
        image = discord.File("tier_table.png", filename="tier_table.png")
        recieve_message = '내전 팀분배시 참고되는 티어표 입니다.'
        await ctx.channel.send(recieve_message, file=image)


    @client.command(aliases=['도배'])
    async def repeat_message(ctx, cnt, *text):
        ms = ''
        for i in range(0, cnt):
            for t in text:
                ms += t+' '
            ms = '\r\n'
        ctx.channel.send(ms)


    @client.command(aliases=['도움말', '명령어'])
    async def help_function(ctx):
        recieve_message = '!등록 <소환사명> : 자신의 계정을 등록\r\n'
        recieve_message += '!참가 : 내전 참가 신청\r\n'
        recieve_message += '!포지션 <포지션명> : 내전시 원하는 포지션 (여러가지 등록가능)\r\n'
        recieve_message += '!내전멤버 : 내전 참가 멤버 출력\r\n'
        recieve_message += '!내전팀분배 : 내전팀 자동 분배\r\n'
        recieve_message += '!내전초기화 : 내전팀 멤버 초기화\r\n'
        recieve_message += '!DBG assemble : 내전 멤버 구인 메세지\r\n'
        ctx.channel.send(recieve_message)


    client.run('token') #토큰

    
