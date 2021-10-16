import pytz
from datetime import datetime

pst = pytz.timezone('America/Los_Angeles')

def game_search(games, game_count, teams_req):
    games_req = []
    counter = 0

    while counter < game_count:
        home_team = games[counter]['teams']['home']['team']['name']
        away_team = games[counter]['teams']['away']['team']['name']
        if [i for i in teams_req if i.lower() in home_team.lower() or i.lower() in away_team.lower()]:
            games_req.append(counter)
        counter += 1
    return games_req

def scores(games, game_count, games_req):
    counter = 0
    msg = ""
    while counter < game_count:
        if counter in games_req:
            game_status = games[counter]['status']['detailedState']
            home_team = games[counter]['teams']['home']['team']['name']
            away_team = games[counter]['teams']['away']['team']['name']
            home_score = games[counter]['teams']['home']['score']
            away_score = games[counter]['teams']['away']['score']
            
            msg += f'*{away_team} @ {home_team}*\n'

            #Scheduled
            if game_status == "Scheduled":
                game_time = datetime.strptime(games[counter]['gameDate'], "%Y-%m-%dT%H:%M:%S%z").astimezone(pst).time().strftime("%-I:%M %p")
                msg += f'{game_status}: {game_time} PT\n'

            #In Progress
            elif game_status == "In Progress":
                game_period = games[counter]['linescore']['currentPeriodOrdinal']
                msg += f'{game_status} ({game_period} Period): {away_score}-{home_score}\n'

            #"In Progress - Critical", "Pre-Game, Final"
            else: 
                msg += f'{game_status}: {away_score}-{home_score}\n'
            
        counter += 1
    return msg