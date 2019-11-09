from flask import Flask
from flask_restful import Api, Resource, reqparse
import connect

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

players = [
    {
        "rank": 1,
        "playername": "Player1",
        "lvl": 24,
        "actualxp": 3095,
        "maxxp": 4963,
        "playedmatches": 1038,
        "wins": 466,
        "winpercent": 44.89,
        "kills": 456,
        "deaths": 357,
        "assists": 45,
        "kd": 2.5,
        "kda": 3.1,
        "killspermatch": 6.24,
        "killsperminute": 1.41,
        "scorepermatch": 346,
        "scoreperminute": 56,
    },
    {
        "rank": 2,
        "playername": "Player2",
        "lvl": 23,
        "actualxp": 3135,
        "maxxp": 4663,
        "playedmatches": 1038,
        "wins": 266,
        "winpercent": 25.62,
        "kills": 456,
        "deaths": 357,
        "assists": 45,
        "kd": 2.5,
        "kda": 3.1,
        "killspermatch": 6.24,
        "killsperminute": 1.41,
        "scorepermatch": 346,
        "scoreperminute": 56,
    },
    {
        "rank": 4,
        "playername": "Player3",
        "lvl": 14,
        "actualxp": 2135,
        "maxxp": 3663,
        "playedmatches": 638,
        "wins": 166,
        "winpercent": 26.01,
        "kills": 256,
        "deaths": 357,
        "assists": 75,
        "kd": 0.71,
        "kda": 3.1,
        "killspermatch": 2.24,
        "killsperminute": 3.41,
        "scorepermatch": 236,
        "scoreperminute": 36,
    },
    {
        "rank": 3,
        "playername": "Player4",
        "lvl": 19,
        "actualxp": 2635,
        "maxxp": 3163,
        "playedmatches": 238,
        "wins": 206,
        "winpercent": 86.55,
        "kills": 356,
        "deaths": 217,
        "assists": 105,
        "kd": 0.71,
        "kda": 3.1,
        "killspermatch": 3.24,
        "killsperminute": 2.41,
        "scorepermatch": 346,
        "scoreperminute": 66,
    }
]


conn = connect.Connect()

class Stats(Resource):
    def get(self, name):
        if name == "test":
            result = conn.getTest()
            conn.closeConnection()
            return result, 200
        else:
            for player in players:
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

class Ranking(Resource):
    def get(self,name):
        if name == "bestplayer":
            player = dict(min(players, key=lambda x:x['rank']))
            return {"playername":player.get("playername"), "rank":player.get("rank")}
        elif name == "mostwins":
            player = dict(max(players, key=lambda x:x['wins']))
            return {"playername":player.get("playername"), "wins":player.get("wins")}
        elif name == "mostkills":
            player = dict(max(players, key=lambda x:x['kills']))
            return {"playername":player.get("playername"), "kills":player.get("kills")}
        else:
            return "User not found", 404

      
api.add_resource(Stats, "/stats/player/<string:name>")
api.add_resource(Ranking, "/rank/<string:name>")

app.run(host='192.168.1.102', port='5000')