from collections import namedtuple
import json
import plotly
from plotly.graph_objs import Scatter
from trueskill import Rating, rate


class Game:

    def __init__(self, json_object):
        self.id = json_object["gameID"]
        self.h = json_object["mapHeight"]
        self.w = json_object["mapWidth"]
        self.name = json_object["replayName"]
        self.timestamp = json_object["timestamp"]
        self.users = []
        for u in range(len(json_object["users"])):
            self.users.append(GameUserInfo(json_object["users"][u]))


class GameUserInfo:

    def __init__(self, json_object):
        self.error_log = json_object["errorLogName"]
        self.oauth_id = json_object["oauthID"]
        self.rank = json_object["rank"]
        self.sigma = json_object["sigma"]
        self.user_id = json_object["userID"]
        self.user_rank = json_object["userRank"]
        if json_object["username"] == "twg16" or json_object["username"] == "KalraA":
            self.user_name = json_object["username"] + " v" + json_object["versionNumber"]
        else:
            self.user_name = json_object["username"]
        self.version = json_object["versionNumber"]


class Player:

    def __init__(self, name):
        self.name = name
        self.rating_data = []
        self.record_match("2017-02-13 06:00:00", Rating(25, 8.333))

    def record_match(self, timestamp, rating):
        self.rating = rating
        self.rating_data.append(PlayerData(timestamp, len(self.rating_data) + 1, rating.mu, rating.sigma))


PlayerData = namedtuple("PlayerData", "timestamp game_number mu sigma")


def do_game(game, players, style="allplayer-trueskill"):
    # Takes a game and stores the results
    game_rank_list = []
    player_list = []
    rating_groups = []
    
    rankable_users = []
    if style=="allplayer-trueskill":
        rankable_users = game.users
    elif style=="topbottom-trueskill":
        rankable_users = [game.users[0],game.users[-1]]
        
    for user_data in rankable_users:
        if user_data.user_name not in players:
            players[user_data.user_name] = Player(user_data.user_name)
        rating_groups.append({user_data.user_name: players[user_data.user_name].rating})
        game_rank_list.append(user_data.rank)
        player_list.append(user_data.user_name)
    rated_list = rate(rating_groups, game_rank_list)
    for i in range(len(rankable_users)):
        if rankable_users[i].user_name not in players:
            players[rankable_users[i].user_name] = Player(rankable_users.user_name)
        players[rankable_users[i].user_name].record_match(game.timestamp, rated_list[i][rankable_users[i].user_name])


def plot_players(player_list, players):
    mu_data = {}
    timestamp_data = {}
    for p in player_list:
        player_mu_data = []
        player_time_data = []
        for r_data in players[p].rating_data:
            player_mu_data.append(r_data.mu)
            player_time_data.append(r_data.timestamp)
        mu_data[p] = player_mu_data
        timestamp_data[p] = player_time_data

    traces = []
    for p in player_list:
        trace = Scatter(x=timestamp_data[p], y=mu_data[p], mode="lines", name=p)
        traces.append(trace)

    plotly.offline.iplot(traces)


def load_all_games():    
    games = []
    # To pull data:
    # wget "https://halite.io/api/web/game?previousID=2331401&limit=100000" -O games.json --no-check-certificate
    # replace previousID value with the last game you DO have. it will stop AT that game and NOT pull it.
    games.extend(json.load(open("data/games-2331402-2359106.json")))
    games.extend(json.load(open("data/games-2359107-2362974.json")))
    games.extend(json.load(open("data/games-2362975-2374581.json")))
    games.extend(json.load(open("data/games-2374582-2384577.json")))
    games.extend(json.load(open("data/games-2384578-2405481.json")))
    games.extend(json.load(open("data/games-2405482-2418383.json")))
    games.extend(json.load(open("data/games-2418384-2426963.json")))

    gamelist = []
    for g in games:
        gamelist.append(Game(g))
    return gamelist
        
def score_with_default_trueskill(gamelist, style="allplayer-trueskill"):

    # Just in case gamelist isn't sorted
    gamelist.sort(key=lambda x: x.id)

    players = {}

    game_count = 0
    print "Loading Games"
    for g in gamelist:
        game_count += 1
        if game_count % 5000 == 0:
            print("%d of %d" %(game_count, len(gamelist)))
        do_game(g, players, style)
    print "Done"
    return players

# player_name = "shummie"
#
# plot_players(["mzotkiew", "erdman", "shummie", "timfoden", "cdurbin", "nmalaguti", "PeppiKokki", "DexGroves", "ewirkerman", "moonbirth"])
# plot_players(["KalraA v91", "KalraA v92"])
