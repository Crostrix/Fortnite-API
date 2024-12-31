import requests
import os
import dotenv
import json

#Load in the variables
dotenv.load_dotenv()

#Load the API Key
api_key = os.getenv('API_KEY')

#Make The Menu
def menu():
    global req
    action = str(input("What would you like to do?\n1. Get stats of an Player\n2. Get info about a Creator\n"
                       "What do you want to do: "))
    if action != "1":
        if action != "2":
            print("Invalid input. Please try again.")
            menu()

    if action == "1":
        player_name = str(input("What is the name of the player: "))
        account_type = str(input("Epic/psn/xbl\nWhat is your account type: "))

        try:
            req = requests.get(
                f"https://fortnite-api.com/v2/stats/br/v2?name={player_name}&account_type={account_type}",
                headers={"Authorization": api_key})
        except requests.exceptions.RequestException as e:
            print(e)
            menu()


        #Parse JSON
        response = json.loads(req.text)
        data = response["data"]
        account = data["account"]
        battle_pass = data["battlePass"]
        stats = data["stats"]
        all = stats["all"]
        overall = all["overall"]

        print(f"Name = {account['name']}\nId  = {account['id']}\nBattle Pass Level = {battle_pass['level']}\nWins = {overall['wins']}\nKills = {overall['kills']}\nMinutes Played = {overall['minutesPlayed']}")


    if action == "2":
        creator_code = str(input("What is the Creator Code: "))

        req = requests.get(f"https://fortnite-api.com/v2/creatorcode?name={creator_code}")
        #print(req.json())

        json_obj = json.loads(req.text)
        status = json_obj["status"]
        if status == 404:
            print("Creator Code not found.")
            menu()

        data = json_obj["data"]
        code = data["code"]
        account = data["account"]
        id = account["id"]
        name = account["name"]
        status = data["status"]
        verified =data["verified"]

        print(f"Creator Code = {code}\nCreator Account Name = {name}\nCreator Account ID = {id}\nCreator Code Status = {status}\nCreator Verified = {verified}")

menu()
