import pandas as pd
import numpy as np


def read_player(file_name):
    columns = [
        'season', 'name', 'adjusted rate', 'fgM', 'fgA',
        'fgM / fgA', 'threePM', 'threePA', 'threePM / threePA', 'free throwM',
        'free throwA', 'free throwM / free throwA', 'assist', 'rebound', 'block',
        'steal', 'turnover', 'plusMinus', 'win', 'lose'
    ]
    data = pd.read_table(file_name, sep='\t', names=columns)
    return data.iloc[:, 1:]


def read_team(file_name):
    #columns = ['season', 'team', 'score']
    columns = ['team', 'score']
    return pd.read_table(file_name, sep='\t', names=columns)


def highlight_min(s):
    if s.dtype == np.object:
        is_min = [False for _ in range(s.shape[0])]
    else:
        is_min = s == s.min()
    return ['background: lightgreen' if cell else '' for cell in is_min]


if __name__ == '__main__':
    filename = 'player/2010-player.txt'
    data = read_player(filename)
    print(data['name'])
    print(list(data['name']))
    print(list(data.columns[1:]))
    name = 'Andrew Bynum'
    print(data.loc[data['name'] == name].values.squeeze().tolist())
    print(list(data.loc[data['name'] == name]['win'])[0])
    # print(list(data.columns).index('adjusted rate'))
