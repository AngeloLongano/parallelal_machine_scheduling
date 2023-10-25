import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from utils.types import ScheduleType


def create_gantt(
    schedule: ScheduleType, num_machines: int, total_time: int, version: int = 1
) -> None:
    """
    Create a Gantt chart from a given schedule.

    Args:
        schedule (list): A list of dictionaries representing the schedules.
        num_machines (int): The number of machines.
        total_time (int): The total time of execution.
        version (int, optional): The version of the schedule. Defaults to 1.

    Returns:
        None: Displays the Gantt chart.
    """
    # Create a new figure and axis
    fig, ax = plt.subplots()
    ax.set_title(f"Schedule {version}")

    # Iterate over each machine in the schedule
    for index, machine in enumerate(schedule):
        # Add a horizontal bar for the machine
        ax.broken_barh(
            [(job["start_time"], job["work_time"]) for job in machine["list_jobs"]],
            ((index + 1) * 10, 8),
            # facecolors=("tab:orange", "tab:green", "tab:red"),
            facecolors=mcolors.TABLEAU_COLORS,
        )
    # Set the y-axis limits and tick labels
    ax.set_ylim(5, num_machines * 15)
    ax.set_yticks(
        [(i + 1) * 10 for i, machine in enumerate(schedule)],
        labels=[machine["name"] for machine in schedule],
    )
    # Set the x-axis limits and label
    ax.set_xlim(0, total_time + 10)
    ax.set_xlabel(f"best time {total_time}")
    # Make grid lines visible
    ax.grid(True)

    # Display the Gantt chart
    plt.show()
