from streamlit.delta_generator import DeltaGenerator
from streamlit_echarts import st_echarts


def add_blank_line(obj):
    obj.text("")
    obj.markdown('''---''')
    obj.text("")


def generate_side_bar(side_bar: DeltaGenerator):
    season_selector = side_bar.selectbox(
        'First select the season you want to analyze 👇', (
            '2010-2011', '2011-2012', '2012-2013',
            '2013-2014', '2014-2015', '2015-2016',
            '2016-2017', '2017-2018', '2018-2019'
        )
    )

    add_blank_line(side_bar)

    function_selector = side_bar.radio(
        'Functions',
        ('Top 10 worst players', 'Top 5 worst teams')
    )

    return season_selector, function_selector


def player_bar_chart(container, player_info, player_name):
    headers = list(player_info.columns)
    x_axis = ['assist', 'rebound', 'block', 'steal', 'turnover', 'plusMinus']
    indexes = [headers.index(x) for x in x_axis]
    row = player_info.loc[player_info['name'] == player_name].values.squeeze().tolist()
    y_axis = []
    for i in indexes:
        y_axis.append((row[i] if row[i] != 'NaN' else 0))
    options = {
        "title": {"text": "Contribution for team", "subtext": "average value", "left": "center"},
        "tooltip": {"trigger": "item"},
        "xAxis": {
            "type": "category",
            "data": x_axis,
        },
        "yAxis": {"type": "value"},
        "series": [{"data": y_axis, "type": "bar"}],
        "color": ["#a3000c"]
    }

    with container:
        st_echarts(options=options, height="500px")


def player_pie_chart(container, player_info, player_name):
    win_num = list(player_info.loc[player_info['name'] == player_name]['win'])[0]
    lose_num = list(player_info.loc[player_info['name'] == player_name]['lose'])[0]
    options = {
        "title": {
            "text": "Win / Lose",
            "left": "center"
        },
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "left"},
        "series": [
            {
                "name": "Number",
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": win_num, "name": "win"},
                    {"value": lose_num, "name": "lose"}
                ],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
                #"color": ["#F38181", "#FCE38A", "#95E1D3"]
                "color": ["#a3000c", "#092972", "#0B346E"]
            }
        ],
    }
    with container:
        st_echarts(options=options, height="400px")


def player_radar_chart(container, player_info, player_name, season):
    abilities = ['fgM', 'assist', 'rebound', 'block', 'steal', 'turnover']
    avg_file = 'data/player/{}-avg.txt'.format(season)
    data = [list(player_info.loc[player_info['name'] == player_name][x])[0] for x in abilities]

    with open(avg_file, 'r', encoding='utf-8') as f:
        line = f.read()
    raw_data = line.strip().split('\t')[1:2] + line.strip().split('\t')[10:15]
    avg_value = []
    for x in raw_data:
        avg_value.append(('%.2f' % float(x)) if x != 'NaN' else 0)

    option = {
        "title": {"text": "Player Ability", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "left": "right"},
        "radar": {
           "indicator": [
                {"name": "FGM", "max": 8},
                {"name": "AST", "max": 5},
                {"name": "REB", "max": 8},
                {"name": "BLK", "max": 5},
                {"name": "STL", "max": 5},
                {"name": "TOV", "max": 5},

            ]
        },
        "series": [
            {
                "name": "player vs average",
                "type": "radar",
                "data": [
                    {
                        "value": data,
                        "name": "player",
                    },
                    {
                        "value": avg_value,
                        "name": "average",
                    },
                ],
            }

        ],
        "color": ["#c40808", "#0B346E"]
    }
    with container:
        st_echarts(option, height="400px")
