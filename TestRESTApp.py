from flask import Flask
from flask_restful import Api, Resource, reqparse
import connect
import json
import DB
from myConfig import configSERVER
from myConfig import configLocalIP

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nicholas",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Elvin",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jass",
        "age": 22,
        "occupation": "Web Developer"
    }
]




#conn = connect.Connect()

class Stats(Resource):
    def get(self, name):
        
        for player in DB.playersDatabase:
            if(name == player["playername"]):
                return player, 200
        #for user in users:
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


@app.route("/stats/ranking/best/<string:name>")
def getBest(name):
    if name == "bestplayer":
        player = dict(min(DB.playersDatabase, key=lambda x:x['rank']))
        return {"playername":player.get("playername"), "statvalue":player.get("rank")}
    elif name == "mostwins":
        player = dict(max(DB.playersDatabase, key=lambda x:x['wins']))
        return {"playername":player.get("playername"), "statvalue":player.get("wins")}
    elif name == "mostkills":
        player = dict(max(DB.playersDatabase, key=lambda x:x['kills']))
        return {"playername":player.get("playername"), "statvalue":player.get("kills")}
    else:
        return "User not found", 404

@app.route("/stats/player/profile/<string:name>")
def getPlayerProfile(name):
        if name == "test":
            #result = conn.getTest()
            #conn.closeConnection()
            return 'result', 200
        else:
            for player in DB.playersDatabase:
                if(name == player["playername"]):
                    player['killspermatch'] = player.get('kills') / player.get('playedmatches')
                    print(player)
                    return player, 200
        #for user in users:
        #    if(name == user["name"]):
        #        return user, 200
        return "User not found", 404
      

@app.route("/stats/search/<string:name>")
def getPlayersByName(name):
    if name != "":
        players = []
        for player in DB.playersDatabase:
            if name.lower() in player.get("playername").lower():
                players.append({"playername": player.get("playername"), "rank": player.get("rank")})
        print(players)
        return json.dumps(players), 200
    else:
        return "User not found", 404

@app.route("/stats/player/history/<string:player_name>/<string:stat_type>")
def getPlayerHistory(player_name,stat_type):
    if player_name != "":
        if stat_type != "":
            player_id = ''
            for player in DB.playersDatabase:
                if player_name.lower() in player.get('playername').lower():
                    player_id = player.get('id')
            returnValue = []
            for stat in DB.matches:
                if player_id in stat.get('player_id'):
                    returnValue.append({'date': stat['date'], 'wins': stat['wins'], 'losses': stat['losses']})
            return json.dumps(returnValue), 200
        else:
            return 'Stat type not found', 404
    else:
        return 'Player not found', 404


#api.add_resource(Stats, "/stats/player/<string:name>")

app.run(host=configLocalIP(), port=configSERVER('port'))