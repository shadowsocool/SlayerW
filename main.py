import requests, subprocess, os, json, time, urllib, re, datetime, discord, colorama, random
colorama.init(convert=True)
def gettime(): return datetime.datetime.today().strftime('%H:%M:%S %p')
print("""\033[95m
         ______     __         ______     __  __     ______     ______     __     __    
        /\  ___\   /\ \       /\  __ \   /\ \_\ \   /\  ___\   /\  == \   /\ \  _ \ \   
        \ \___  \  \ \ \____  \ \  __ \  \ \____ \  \ \  __\   \ \  __<   \ \ \/ ".\ \  
         \/\_____\  \ \_____\  \ \_\ \_\  \/\_____\  \ \_____\  \ \_\ \_\  \ \__/".~\_\ 
          \/_____/   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_/ /_/   \/_/   \/_/                                                                             

                                    credits: shadow.#9999
                            open source cause i dont release malware
""")
with open("./settings.json","r") as raw:
    settings = json.loads(raw)

launcher = f"{os.getenv('LOCALAPPDATA')}\\Roblox\\versions\\{settings['version']}\\RobloxPlayerLauncher.exe"
if not os.path.exists(launcher):
    print("Invalid roblox version!\nMake sure you have the right version in settings.json")
    time.sleep(3)
    exit()


def join(link):
    print(f"    \033[96m{gettime()} - \033[94mPreparing to join..")
    req = requests.post("https://auth.roblox.com/v1/authentication-ticket", headers={"Cookie":f".ROBLOSECURITY={settings['cookie']}"})
    print(f"    \033[96m{gettime()} - \033[94mRequest 1 finished")
    ticket = requests.post("https://auth.roblox.com/v1/authentication-ticket", headers={"Cookie":f".ROBLOSECURITY={settings['cookie']}", "Origin": "https://www.roblox.com", "Referer": "https://www.roblox.com/","x-csrf-token":req.headers["x-csrf-token"]}).headers['rbx-authentication-ticket']
    print(f"    \033[96m{gettime()} - \033[94mRequest 2 finished")
    request = requests.get(link, headers={"Referer": "https://www.roblox.com/games/606849621/Jailbreak","X-CSRF-TOKEN":req.headers["x-csrf-token"]}, cookies={".ROBLOSECURITY": settings['cookie']})
    print(f"    \033[96m{gettime()} - \033[94mRequest 3 finished") 
    match = re.search(r"Roblox.GameLauncher.joinPrivateGame\((\d+), '([a-f0-9\-]+)', '(\d+)'\)", request.text)
    if match:
        args = f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{'{0:.0f}'.format(round(time.time() * 1000))}+placelauncherurl:{urllib.parse.quote_plus(f'https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestPrivateGame&placeId={match.group(1)}&accessCode={match.group(2)}&linkCode={match.group(3)}')}+browsertrackerid:{random.randint(100000, 175000) + random.randint(100000, 900000)}+robloxLocale:en_us+gameLocale:en_us+channel:zprojectupdate-webrtc-fetch-content+LaunchExp:InApp"
        print(f"    \033[96m{gettime()} - \033[92m\033[1mLaunching roblox\033[22m")
        subprocess.Popen([launcher, args])

id = int(input(f"    \033[96m{gettime()} - \033[94mPlease enter channel ID where private server is dropped: "))
gameid = int(input(f"    \033[96m{gettime()} - \033[94mPlease enter game ID to join: "))
client = discord.Client()
@client.event
async def on_message(message):
    if message.channel.id == id:
        try:
            message = message.content
            ext = message.split(f"https://www.roblox.com/games/{gameid}?")[1]
            join(f"https://www.roblox.com/games/{gameid}?{ext}")
        except Exception as e:
            print(e)
            print(f"    \033[96m{gettime()} - \033[91mFailed to get private server link.")
            

@client.event
async def on_ready():
    print(f"    \033[96m{gettime()} - \033[92mSuccessfully logged into account.")

client.run(settings['token'], bot=False)
