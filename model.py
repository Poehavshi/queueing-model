import numpy as np


def create_calls_distribution(alpha, beta, simulation_time):
    calls_starts = [-np.log(np.random.random_sample()) / alpha]
    calls_durations = [np.random.random_sample() / beta]
    length = calls_durations[0]  # конец первого отрезка

    while length < simulation_time:
        calls_starts.append((-np.log(np.random.random_sample()) / alpha) + calls_starts[-1])
        calls_durations.append(((np.random.random_sample()) / beta))
        length = calls_starts[-1]
    calls_starts = calls_starts[:-1]
    calls_durations = calls_durations[:-1]
    return calls_starts, calls_durations


def get_distribution(alpha: float,  # показатель для времени?
                     beta: float,  # показатель для длительности
                     number_of_lines: int,
                     storage_capacity: int,
                     simulation_time: int,
                     ):
    call_starts, calls_durations = create_calls_distribution(alpha, beta, simulation_time)

    number_of_rejected_calls = 0
    number_of_calls = 0
    busy_lines = 0

    lines = [dict() for _ in range(number_of_lines)]
    # на 1 линию помещаем первый вызов
    lines[0][call_starts[0]] = calls_durations[0]
    capacity = []
    # Разыгрываем вызов среди всех линий
    for j in range(1, len(call_starts)):
        line_number = 0
        rejected_by_lines = True
        while line_number < number_of_lines:
            current_line = lines[line_number]
            if len(current_line) == 0:
                current_line[call_starts[j]] = calls_durations[j]
                rejected_by_lines = False
                break
            last_call_start = list(current_line.keys())[-1]
            last_call_duration = current_line[last_call_start]
            if last_call_start + last_call_duration < call_starts[j]:
                current_line[call_starts[j]] = calls_durations[j]
                rejected_by_lines = False
                break
            line_number += 1  # смотрим следующую линию

        if busy_lines < line_number < number_of_lines:
            busy_lines = line_number

        if rejected_by_lines:
            min_index = 0
            min_time_start = simulation_time
            for i in range(number_of_lines):
                if list(lines[i].keys())[-1] < min_time_start:
                    min_time_start = list(lines[i].keys())[-1]
                    min_index = i
            count = 0
            for i in range(len(capacity)):
                if capacity[i][0] < call_starts[j] < capacity[i][1]:
                    count += 1
            if count < storage_capacity:
                lines[min_index][list(lines[min_index].keys())[-1]] += calls_durations[j]
                capacity.append([call_starts[j], list(lines[min_index].keys())[-1] + lines[min_index][
                    list(lines[min_index].keys())[-1]]])
            else:
                number_of_rejected_calls += 1
        number_of_calls += 1

    busy_capacity = 0
    for cap in capacity:
        if cap[0] < simulation_time < cap[1]:
            busy_capacity += 1

    efficiency = number_of_calls / (number_of_rejected_calls + number_of_calls)
    busy_capacity = 0
    for i in capacity:
        if i[0] < simulation_time < i[1]:
            busy_capacity += 1

    return lines, number_of_calls, efficiency, number_of_rejected_calls, busy_lines + 1, busy_capacity


if __name__ == '__main__':
    np.random.seed(1)
    get_distribution(0.1, 0.1, 3, 1, 100)
