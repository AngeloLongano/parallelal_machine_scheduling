from typing import TypedDict


class JobType(TypedDict):
    name: str
    start_time: int
    work_time: int


class MachineType(TypedDict):
    name: str
    list_jobs: list[JobType]
    time_to_execute: int


ScheduleType = list[MachineType]


class InstanceProblemType(TypedDict):
    id: str
    num_jobs: int
    max_time_jobs: int
    num_machines: int
    sort_from_longest_to_shortest: bool
    list_jobs: list[JobType]
    list_machines: list[MachineType]


class StatisticsType(TypedDict):
    standard_deviation_average: float
    num_best_average: int
    average_time: float
    standard_deviation_time_average: float


class AlgorithmType(TypedDict):
    id: str
    chooser_job: str
    neighbor_way: str
    statistics: StatisticsType


class ResultsInstanceType(TypedDict):
    best_solution: int
    wrongest_solution: int
    average_solution: float
    standard_deviation_solution: float
    num_best_solution: int
    average_time: float
    standard_deviation_time: float


class SolutionType(TypedDict):
    id_algorithm: str
    initial_solutions: list[int]
    final_solutions: list[int]
    executions_greedy_time: list[float]
    executions_local_search_time: list[float]
    results_per_instance: ResultsInstanceType


class BenchmarkType(TypedDict):
    instance_id: InstanceProblemType
    solutions: list[SolutionType]
    results_per_instance: ResultsInstanceType
