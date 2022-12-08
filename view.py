import streamlit as st


# todo create view to show different queues

def render_main_window():
    st.markdown("# Система массового обслуживания")

    simulation_time = st.number_input("Время моделирования")
    alpha = st.number_input("Показатель для времени")
    beta = st.number_input("Показатель для длительности")
    number_of_lines = st.number_input("Число линий")
    capacity_storage = st.number_input("Емкость накопителя")
    # use scatter plot maybe
