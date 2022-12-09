import view
import model

def run():
    # 1) get data from view
    simulation_time, alpha, beta, number_of_lines, storage_capacity = view.render_input_form()
    distributions, number_of_calls, efficiency, number_of_rejected_calls, busy_lines, busy_capacity = model.get_distribution(alpha, beta, number_of_lines, storage_capacity, simulation_time)

    view.render_distribution_plot_for_line(distributions)
    view.render_output_data(number_of_calls, efficiency, number_of_rejected_calls, busy_lines, busy_capacity)

    # 2) move it to model and get response from it
    # 3) move data to view
