"""
This module contains utility functions for scheduling jobs on machines.
"""
from utils.helpers import *
from utils.types import *
from utils.instances import *

import random
import copy
import time
import math


# CHOOSER_JOBS_WAY


def deterministic_way(jobs) -> JobType:
    return jobs[0]


K_NON_DETERMINISTIC_WAY = 10


def non_deterministic_way(jobs) -> JobType:
    randomChoose = random.randint(0, K_NON_DETERMINISTIC_WAY)
    if randomChoose >= len(jobs):
        randomChoose = 0
    return jobs[randomChoose]


def random_way(jobs) -> JobType:
    return jobs[random.randint(0, len(jobs) - 1)]


CHOOSER_JOBS_WAY = (deterministic_way, non_deterministic_way, random_way)


# NEIGHBORS_WAY


def _remove_job(machine: MachineType, job: JobType):
    index_job = machine["list_jobs"].index(job)
    machine["list_jobs"].remove(job)

    if index_job < len(machine["list_jobs"]):
        machine["list_jobs"][index_job] = {
            **machine["list_jobs"][index_job],
            "start_time": job["start_time"],
        }
        for index in range(index_job + 1, len(machine["list_jobs"])):
            machine["list_jobs"][index] = {
                **machine["list_jobs"][index],
                "start_time": machine["list_jobs"][index - 1]["start_time"]
                + machine["list_jobs"][index - 1]["work_time"],
            }
    machine["time_to_execute"] -= job["work_time"]


def _insert_job(machine: MachineType, job: JobType):
    machine["list_jobs"].append({**job, "start_time": machine["time_to_execute"]})
    machine["time_to_execute"] += job["work_time"]


def insert_move(initial_schedule: list[MachineType]):
    best_schedule = copy.deepcopy(initial_schedule)
    new_schedule = copy.deepcopy(initial_schedule)

    for index_machine in range(len(initial_schedule)):
        for index_job in range(len(initial_schedule[index_machine]["list_jobs"])):
            for index_other_machine in range(len(initial_schedule)):
                if index_machine == index_other_machine:
                    continue

                job = new_schedule[index_machine]["list_jobs"][index_job]
                machine = new_schedule[index_machine]
                other_machine = new_schedule[index_other_machine]

                _remove_job(machine, job)
                _insert_job(other_machine, job)

                if get_solution(new_schedule) < get_solution(best_schedule):
                    best_schedule = copy.deepcopy(new_schedule)

                new_schedule = copy.deepcopy(initial_schedule)
    return best_schedule


def swap_move(initial_schedule: list[MachineType]):
    best_schedule = copy.deepcopy(initial_schedule)
    new_schedule = copy.deepcopy(initial_schedule)

    for index_machine in range(len(initial_schedule)):
        for index_job_1 in range(len(initial_schedule[index_machine]["list_jobs"])):
            for index_other_machine in range(len(initial_schedule)):
                if index_machine == index_other_machine:
                    continue

                for index_job_2 in range(
                    len(initial_schedule[index_other_machine]["list_jobs"])
                ):
                    job_1 = new_schedule[index_machine]["list_jobs"][index_job_1]
                    job_2 = new_schedule[index_other_machine]["list_jobs"][index_job_2]
                    machine = new_schedule[index_machine]
                    other_machine = new_schedule[index_other_machine]

                    _remove_job(machine, job_1)
                    _remove_job(other_machine, job_2)
                    _insert_job(other_machine, job_1)
                    _insert_job(machine, job_2)

                    if get_solution(new_schedule) < get_solution(best_schedule):
                        best_schedule = copy.deepcopy(new_schedule)

                    new_schedule = copy.deepcopy(initial_schedule)
    return best_schedule


NEIGHBORS_WAY = (insert_move, swap_move)


def _create_neighbor_list(initial_solution, num_solutions=10, neighbor_way=insert_move):
    return [neighbor_way(initial_solution) for i in range(num_solutions)]


# ALGORITHMS


@time_function
def greedy_algorithm(
    _instance: InstanceProblemType,
    chooser_job=non_deterministic_way,
) -> list[MachineType]:
    jobs = _instance["list_jobs"].copy()
    schedule = copy.deepcopy(_instance["list_machines"])
    job = jobs[0]

    while len(jobs) > 0:
        # choose the next job
        job = chooser_job(jobs)
        # remove from list of jobs to assign
        jobs.remove(job)
        # select machine with minor time_to_execute
        machine = min(schedule, key=lambda x: x["time_to_execute"])
        # add job to machine
        machine["list_jobs"].append({**job, "start_time": machine["time_to_execute"]})
        # update time_to_execute of machine
        machine["time_to_execute"] = machine["time_to_execute"] + job["work_time"]

    return schedule


@time_function
def local_search_algorithm(
    initial_schedule,
    neighborWay=insert_move,
    stopTimeCondition=10,
):
    initial_time = get_solution(initial_schedule)
    best_solution = neighborWay(initial_schedule)
    best_time = get_solution(best_solution)

    start_time = time.time()

    while best_time < initial_time and time.time() - start_time < stopTimeCondition:
        initial_time = best_time
        best_solution = neighborWay(best_solution)
        best_time = get_solution(best_solution)

    return best_solution


@time_function
def simulated_annealing(
    initial_solution,
    start_value_t0=50,
    decrease_alpha=0.8,
    stop_tk=1,
    stop_time_condition=10,
    iterations_with_same_tk=10,
    neighbor_way=swap_move,
):
    start_solution = copy.deepcopy(initial_solution)
    accepted_solution = copy.deepcopy(initial_solution)
    time_accepted_solution = get_solution(accepted_solution)

    tk = start_value_t0

    start_time = time.time()

    while time.time() - start_time < stop_time_condition and tk > stop_tk:
        for i in range(iterations_with_same_tk):
            neighbors = _create_neighbor_list(start_solution, neighbor_way=neighbor_way)

            choosed_solution = neighbors[random.randrange(0, len(neighbors) - 1)]
            time_choosed_solution = get_solution(choosed_solution)

            if time_choosed_solution < time_accepted_solution:
                accepted_solution = copy.deepcopy(choosed_solution)
                time_accepted_solution = get_solution(accepted_solution)
            else:
                probability_to_choose = math.exp(
                    time_accepted_solution - time_choosed_solution / tk
                )
                if random.randrange(0, 100) / 100 < probability_to_choose:
                    accepted_solution = copy.deepcopy(choosed_solution)
                    time_accepted_solution = get_solution(accepted_solution)
    tk = tk * decrease_alpha
    return accepted_solution


def get_solution(schedule: list[MachineType]) -> int:
    return max(schedule, key=lambda x: x["time_to_execute"])["time_to_execute"]
