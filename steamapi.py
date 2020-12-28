import requests, json, config
from json.decoder import JSONDecodeError

def get_Acc_Info(steamid64):
    finalSteamid = ""
    if len(steamid64) == 1: #if only one id is passed in, just set the id to it
        finalSteamid = steamid64[0]
    else: #else there is more than one ID passed in
        for id in steamid64: #Loop tru each id and concat them into comma seperated string which the API require to request multiple ids
            if id == steamid64[0]:
                finalSteamid = id + ','
            elif id == steamid64[-1]:
                finalSteamid = finalSteamid + id
            else:
                finalSteamid = finalSteamid + id + ','
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key='+ config.steam_api_key +'&steamids=' + finalSteamid
    req = requests.get(url)
    req_json = req.json()
    #write_Json('data.txt', req_json['players'][0])
    playerList = req_json['players']
    nameList = get_Display_Name(finalSteamid)
    for x in range(len(playerList)):
        playerList[x].pop('EconomyBan')
        playerList[x].pop('NumberOfGameBans')
        for name in nameList:
            if (playerList[x]['SteamId'] == name['steamid']):
                playerList[x]['personaname'] = name['personaname']
    #append_Json('data.txt', req_json)
    return playerList

def get_Display_Name(steamid64):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+ config.steam_api_key +'&steamids=' + steamid64
    req = requests.get(url)
    req_json = req.json()
    playerList = req_json['response']['players']
    return playerList

def validateSteamID(steamID):
    if len(steamID) == 17 and steamID.isdigit():
        return True
    return False

def get_Games_Owned(steamid64):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+ config.steam_api_key +'&steamid=' + steamid64
    req = requests.get(url)
    req_json = req.json()
    req_json = req_json['response']
    game_count = req_json['game_count']
    games = req_json['games']
    for item in games:
        if item['appid'] == 730:
            print("CSGO")
    #write_Json('data.txt', req_json)

def get_Game_Stats(appid, steamid64):
    url = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid='+ appid + '&key='+ config.steam_api_key +'&steamid=' + steamid64
    req = requests.get(url)
    req_json = req.json()
    #write_Json('data.txt', req_json)

def write_Json(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def read_Json(file):
    with open(file, 'r') as infile:
        #use try...except so we dont get error when the file is empty(it will return None if its empty)
        try:
            data = json.load(infile)
            return data
        except JSONDecodeError:
            pass

def append_Json(file, new_data):
    iDexist = False
    data = read_Json(file)
    #print(new_data)

    if (data == None):
        write_Json(file, new_data)
    else:
        #data.append(new_data)
        temp = data
        for items in temp:
            if items['SteamId'] == new_data['SteamId']:
                print("Id already exist!")
                iDexist = True
        if (not iDexist):
            temp.append(new_data)
            write_Json(file, temp)
            #print(temp)


#show_info()
#get_Games_Owned('76561198876714270')
#get_Game_Stats('730', '76561198876714270')
#get_Acc_Info('76561198876714270')
#get_Display_Name('76561198835787127')
#read_Json('data.txt')
