import streamlit as st
from pandas import DataFrame

from components import *
from data.reformat import *

side_bar = st.sidebar
main_panel = st

# side bar
season_selector, function_selector = generate_side_bar(side_bar)
season = season_selector.split('-')[0]


if function_selector == 'Top 10 worst players':
    st.title("Top 10 worst player")
    analytic_result_container = main_panel.container()
    col1, col2 = analytic_result_container.columns(2)
    # add a blank line between two containers
    add_blank_line(main_panel)

    dashboard_container = main_panel.container()

    analytic_result = col1.radio(
        'Analytic Results',
        ('Summations', 'Single player')
    )

    try:
        player_info: DataFrame = read_player('data/player/{}-player.txt'.format(season))
        if analytic_result == 'Summations':
            dashboard_container.dataframe(player_info.style.apply(highlight_min))
        elif analytic_result == 'Single player':
            player_name = col2.selectbox('Player Name', player_info['name'])
            # layout for pie chart and radar chart
            pie_col, radar_col = dashboard_container.columns(2)

            # pie chart
            player_pie_chart(pie_col, player_info, player_name)

            # radar chart
            player_radar_chart(radar_col, player_info, player_name, season)

            # bar chart
            player_bar_chart(dashboard_container, player_info, player_name)

    except FileNotFoundError:
        main_panel.error("{}赛季的数据文件暂时不存在，请联系huhuhu".format(season))
else:
    st.title("Top 5 worst teams")
    # main_panel.title("队伍看板功能暂时未做")
    team_info = read_team('data/team/{}-team.txt'.format(season))
    main_panel.table(team_info)


# TODO: 调整雷达图的max值，让它看起来好看点
# TODO: 实现球队统计看板
