from asyncio.windows_events import NULL
import pandas as pd

data_path = 'C:\\Users\\inwon\\Documents\\PythonProject\\separateLolTeams\\user_list.csv'


def loadData():
    global user_list
    user_list = pd.read_csv(data_path)
    user_list.set_index('userId')

def saveData():
    global user_list
    
    user_list.to_csv(data_path, index=False)

def insertUser(userId, userName, summonerId, summonerName):
    global user_list
    dump = {'userId':userId, 'userName':userName, 'summonerId':summonerId, 'summonerName':summonerName}
    user_list = user_list.append(dump, ignore_index=True)
    
def isReigisted(userId):
    global user_list
    print(user_list.head())

    return user_list[user_list['userId'] == userId].empty == False
    
def setUserName(userId, un):
    global user_list

    user_list.loc[user_list['userId'] == userId, 'userName'] = un
    
def setSummonerId(userId, si):
    global user_list

    user_list.loc[user_list['userId'] == userId, 'summonerId'] = si
    
def setSummonerName(userId, sn):
    global user_list

    user_list.loc[user_list['userId'] == userId, 'summonerName'] = sn
    
def getUserName(userId):
    global user_list

    if user_list[user_list['userId'] == userId].empty :
        return ''

    return user_list[user_list['userId'] == userId].values[0][1]
    
def getSummonerId(userId):
    global user_list

    if user_list[user_list['userId'] == userId].empty :
        return 0

    return user_list[user_list['userId'] == userId].values[0][2]
    
def getSummonerName(userId):
    global user_list

    if user_list[user_list['userId'] == userId].empty :
        return ''

    return user_list[user_list['userId'] == userId].values[0][3]
    
def getAllData():
    global user_list
    return user_list
    

"""loadData()
print(user_list.index)
for i in user_list.index:
    print(user_list['point'][i])

print(user_list['userId'].head())
print(getUserPoint(493971100183560202))
print(user_list.head())

saveData()
loadData()
print('1# {}'.format(getUserPoint(493971100183560202)))
print('2# {}'.format(getUserPoint(493971100183560203)))"""