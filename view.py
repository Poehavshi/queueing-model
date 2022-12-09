import streamlit as st

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# todo create view to show different queues


def render_input_form():
    st.markdown("# Система массового обслуживания")

    simulation_time = st.number_input("Время моделирования", value=100, step=1, min_value=0)
    alpha = st.number_input("Показатель для времени", value=0.01, step=0.01)
    beta = st.number_input("Показатель для длительности", value=0.01, step=0.01)
    number_of_lines = st.number_input("Число линий", value=2, step=1, min_value=1)
    storage_capacity = st.number_input("Емкость накопителя", value=5, step=1)

    return simulation_time, alpha, beta, number_of_lines, storage_capacity


def render_distribution_plot_for_line(distribution):
    # словарь где ключ - начало, значение - длительность
    starts = []
    duration = []
    rows = [dict(start=0, duration=0.01, character=str(index)) for index in range(len(distribution))]
    for index, line_distribution in enumerate(distribution):
        for start, length in line_distribution.items():
            rows.append(dict(start=start, duration=length, character=str(index)))

    dataframe = pd.DataFrame(rows)
    print(dataframe)

    fig = go.Figure(
        layout={
            'barmode': 'stack',
            'xaxis': {'automargin': True},
            'yaxis': {'automargin': True}}  # , 'categoryorder': 'category ascending'}}
    )

    for character, character_df in dataframe.groupby('character'):
        fig.add_bar(x=character_df.duration,
                    y=character_df.character,
                    base=character_df.start,
                    orientation='h',
                    showlegend=False,
                    name=character)
    st.plotly_chart(fig)


def render_output_data(number_of_calls, efficiency, number_of_rejected_calls, busy_lines, busy_capacity):
    st.text(f"Количество вызовов {number_of_calls}")
    st.text(f"Эффективность {efficiency}")
    st.text(f"Количество отклонённых вызовов {number_of_rejected_calls}")
    st.text(f"Количество занятых линий {busy_lines}")
    st.text(f"Количество занятых накопителей {busy_capacity}")
