from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import connect
import json
import DB
from myConfig import configSERVER
from myConfig import configLocalIP
import pandas as pd
import datetime
import random

app = Flask(__name__)
api = Api(app)

#conn = connect.Connect()

'''
class Stats(Resource):
    def get(self, name):

        for player in DB.playersDatabase:
            if(name == player["playername"]):
                return player, 200
        # for user in users:
        #    if(name == user["name"]):
        #        return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200
'''


@app.route("/stats/ranking/best/<string:name>")
def getBest(name):
    if name == "bestplayer":
        player = dict(min(DB.playersDatabase, key=lambda x: x['rank']))
        return {"playername": player.get("playername"), "statvalue": player.get("rank")}
    elif name == "mostwins":
        player = dict(max(DB.playersDatabase, key=lambda x: x['wins']))
        return {"playername": player.get("playername"), "statvalue": player.get("wins")}
    elif name == "mostkills":
        player = dict(max(DB.playersDatabase, key=lambda x: x['kills']))
        return {"playername": player.get("playername"), "statvalue": player.get("kills")}
    else:
        return "User not found", 404


@app.route("/stats/player/profile/<string:name>")
def getPlayerProfile(name):
    if name == "test":
            #result = conn.getTest()
            # conn.closeConnection()
        return 'result', 200
    else:
        result = {}
        for player in DB.playersDatabase:
            if(name == player["playername"]):
                result = player
                result['kd'] = player['kills'] / player['deaths']
                result['kda'] = (player['kills'] +
                                 (player['assists'] / 3)) / player['deaths']
                result['killspermatch'] = player.get(
                    'kills') / player.get('playedmatches')
                result['scorepermatch'] = player['overallscore'] / \
                    player['playedmatches']
                result['killsperminute'] = player['kills'] / \
                    (player['overallgametime'] / 60.0)
                result['scoreperminute'] = player['overallscore'] / \
                    (player['overallgametime'] / 60)

                print(result)
                return result, 200
    # for user in users:
    #    if(name == user["name"]):
    #        return user, 200
    return "User not found", 404


@app.route("/stats/player/search/<string:name>")
def getPlayersByName(name):
    if name != "":
        players = []
        for player in DB.playersDatabase:
            if name.lower() in player.get("playername").lower():
                players.append({"playername": player.get(
                    "playername"), "rank": player.get("rank")})
        print(players)
        return json.dumps(players), 200
    else:
        return "User not found", 404


@app.route("/stats/player/search/<int:player_rank>")
def getPlayersByRank(player_rank):
    if player_rank > 0:
        players = []
        for player in DB.playersDatabase:
            if player_rank == player["rank"] or str(player_rank) in player["playername"]:
                players.append(
                    {"playername": player["playername"], "rank": player["rank"]})
        return json.dumps(players), 200
    else:
        return "User not found", 404


@app.route("/stats/player/history/<string:player_name>/<string:stat_type>")
def getPlayerHistory(player_name, stat_type):
    if player_name != "":
        if stat_type != "":
            player_id = ''
            for player in DB.playersDatabase:
                if player_name.lower() in player.get('playername').lower():
                    player_id = player.get('id')
                lastweekdaterange = pd.date_range(datetime.datetime.now(
                ) - datetime.timedelta(days=7), datetime.datetime.now())
                lastmonthdaterange = pd.date_range(datetime.datetime.now(
                ) - datetime.timedelta(days=30), datetime.datetime.now())
                lastWeekStats = []
                lastMonthStats = []
            if stat_type == 'wins_losses':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 8)),
                                           str(random.randint(0, 8) * -1)])
            elif stat_type == 'wins_percent':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 100))])
            elif stat_type == 'kills':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 34))])
            elif stat_type == 'deaths':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 28))])
            elif stat_type == 'kd':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 34)),
                                           str(random.randint(0, 28) * -1)])
            elif stat_type == 'kda':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 34)),
                                           str(random.randint(0, 34)),
                                           str(random.randint(0, 28) * -1)])
            elif stat_type == 'kills_per_match':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(0, 10))])
            elif stat_type == 'kills_per_minute':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.random()/2.0)])
            elif stat_type == 'score_per_match':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.randint(100, 8000))])
            elif stat_type == 'score_per_minute':
                for single_date in lastmonthdaterange:
                    lastMonthStats.append(["'" + single_date.strftime("%d-%m") + "'",
                                           str(random.random()*random.randint(4, 400))])
            return json.dumps(
                {
                    # 'lastweek': lastWeekStats,
                    'lastmonth': lastMonthStats
                },
            ), 200

        else:
            return 'Stat type not found', 404
    else:
        return 'Player not found', 404


@app.route('/posttest', methods=['POST'])
def posttest():
    input_json = request.get_json(force=True)
    print(input_json)
    return 'Submitted score'


app.run(host=configLocalIP(), port=configSERVER('port'))
#app.run(host="192.168.1.102", port=configSERVER('port'))
