from utils.types import *
import random


def _create_random_jobs(num_jobs: int, max_time_jobs: int) -> list[JobType]:
    return [
        {
            "name": "job" + str(i),
            "start_time": 0,
            "work_time": random.randint(1, max_time_jobs),
        }
        for i in range(1, num_jobs + 1)
    ]


def _create_machines(num_machine: int) -> list[MachineType]:
    return [
        {"name": "M" + str(i), "list_jobs": [], "time_to_execute": 0}
        for i in range(1, num_machine + 1)
    ]


def create_instance_problem(
    num_jobs: int,
    max_time_jobs: int,
    num_machine: int,
    sort_from_longest: bool = True,
) -> InstanceProblemType:
    jobs = _create_random_jobs(num_jobs, max_time_jobs)
    jobs = sorted(jobs, key=lambda j: j["work_time"], reverse=sort_from_longest)
    return {
        "num_jobs": num_jobs,
        "max_time_jobs": max_time_jobs,
        "num_machines": num_machine,
        "sort_from_longest": sort_from_longest,
        "list_jobs": jobs,
        "list_machines": _create_machines(num_machine),
    }
