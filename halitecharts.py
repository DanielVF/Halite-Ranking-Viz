import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime

def plot_converge(player):
    player_mus = []
    player_sigmas = []
    player_dates = []
    for r_data in player.rating_data[20:]:
        player_mus.append(r_data.mu)
        player_sigmas.append(r_data.sigma)
        player_dates.append(datetime.datetime.strptime(r_data.timestamp,'%Y-%m-%d %H:%M:%S'))

    player_mus = np.array(player_mus)
    player_sigmas = np.array(player_sigmas)
    dates = matplotlib.dates.date2num(player_dates)

    sns.set_style("darkgrid")
    plt.rcParams["figure.figsize"] = [14.0, 6.0]
    plt.fill_between(range(20, len(player.rating_data)), player_mus+player_sigmas*2, player_mus-player_sigmas*2, facecolor='grey', alpha=0.5)
    plt.plot(range(20, len(player.rating_data)), player_mus)
    plt.show()
    
    
def leaderboard(players, num_players=10):
    ranked_players = []
    for username, player in players.iteritems():
        ranked_players.append([username, player.rating_data[-1].mu, player.rating_data[-1].sigma])
       
    ranked_players.sort(key=lambda x: 0-x[1])
    return ranked_players[0: num_players]
    
def leaderboard_user_names(players, num_players=10):
    return [x[0] for x in leaderboard(players, num_players)]


def plot_compare(players, player_names, ysize=8.0, starting_game=20, show_sigma=True):
    for name in player_names:
        player = players[name]
        player_mus = []
        player_sigmas = []
        player_dates = []
        for r_data in player.rating_data[starting_game:]:
            player_mus.append(r_data.mu)
            player_sigmas.append(r_data.sigma)
            player_dates.append(datetime.datetime.strptime(r_data.timestamp,'%Y-%m-%d %H:%M:%S'))

        player_mus = np.array(player_mus)
        player_sigmas = np.array(player_sigmas)
        dates = matplotlib.dates.date2num(player_dates)

        sns.set_style("darkgrid")
        plt.rcParams["figure.figsize"] = [14.0, ysize]
        if show_sigma:
            plt.fill_between(range(starting_game, len(player.rating_data)), player_mus+player_sigmas*2, player_mus-player_sigmas*2, facecolor='grey', alpha=0.5,)
        plt.plot(range(starting_game, len(player.rating_data)), player_mus)
    plt.show()