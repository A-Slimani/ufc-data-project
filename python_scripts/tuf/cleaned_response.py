import json

with open('all_response.json') as file:
    data = json.load(file)

filtered = []
for fight in data:
    if fight['LiveFightDetail']['Accolades']:
        filtered.append(
            {
                "EventName": fight['LiveFightDetail']['Event']['Name'],
                "FightDate": fight['LiveFightDetail']['Event']['StartTime'],
                "b_fighter": f"{fight['LiveFightDetail']['Fighters'][0]['Name']['FirstName']}, {fight['LiveFightDetail']['Fighters'][0]['Name']['LastName']}",
                "r_fighter": f"{fight['LiveFightDetail']['Fighters'][1]['Name']['FirstName']}, {fight['LiveFightDetail']['Fighters'][1]['Name']['LastName']}",
                "AccoladeData": fight['LiveFightDetail']['Accolades'][0],
            }
        )
    else:
        filtered.append(
            {
                "EventName": fight['LiveFightDetail']['Event']['Name'],
                "FightDate": fight['LiveFightDetail']['Event']['StartTime'],
                "b_fighter": f"{fight['LiveFightDetail']['Fighters'][0]['Name']['FirstName']}, {fight['LiveFightDetail']['Fighters'][0]['Name']['LastName']}",
                "r_fighter": f"{fight['LiveFightDetail']['Fighters'][1]['Name']['FirstName']}, {fight['LiveFightDetail']['Fighters'][1]['Name']['LastName']}",
                "AccoladeData": "" ,
            }
        )

with open('cleaned.json', 'w') as file:
    json.dump(filtered, file, indent=2)

