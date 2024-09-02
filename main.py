import numpy

import spreadsheet
import utilities as ut
import priority
import fcfs
import sjf
import roundRobin


ties = ["FCFS", "SJF", "SRTF", "Priority"]


def menu():
    while True:
        try:
            num_processes = int(input("Enter the number of processes: "))
            if num_processes > 0:
                break
            raise ValueError
        except ValueError:
            print("Please enter a valid number.")

    while True:
        print(
            """
    \nSelect a scheduling algorithm:
    1. First Come First Serve (FCFS)
    2. Shortest Job First (SJF)
    3. Shortest Remaining Time First (SRTF)
    4. Priority Scheduling (Preemptive)
    5. Priority Scheduling (Non-preemptive)
    6. Round Robin
    """
        )

        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 6:
                break
            raise ValueError
        except ValueError:
            print("Please enter a valid number.")

    quantum = None
    if choice == 6: # Round Robin choice
        quantum = getQuantum()

    tie_breaker = None
    if choice != 6: # Any choice except Round Robin
        while True:
            print(
                """
        \nThe tie-breaker for processes with the same arrival:
        1. FCFS
        2. SJF
        3. SRTF
        4. Priority
        5. Random
            """
            )

            try:
                tie_breaker = int(input("Enter your choice: "))
                if 1 <= tie_breaker <= 5:
                    if tie_breaker == 5: # Random tie-breaker
                        tie_breaker = numpy.random.choice(ties)
                    tie_breaker = ties[tie_breaker - 1]
                    break
                raise ValueError
            except ValueError:
                print("Please enter a valid number.")

    return num_processes, choice, quantum, tie_breaker

def getQuantum():
    while True:
        try:
            quantum = int(input("Enter the quantum: "))
            if quantum > 0:
                break
            raise ValueError
        except ValueError:
            print("Please enter a valid number.")
    return quantum



def switch_choice(choice, quantum, tie_breaker):
    {
        1: fcfs.planner(tie_breaker),
        2: sjf.nonPreemptive(tie_breaker),
        3: sjf.preemtive(tie_breaker),
        4: priority.preemptive(tie_breaker),
        5: priority.nonPreemptive(tie_breaker),
        6: roundRobin.planner(quantum)
    }.get(choice, lambda: print("Invalid choice. Please try again."))()


def main():
    print("Processes Scheduler Algorithms\n")

    num_processes, choice, quantum, tie_breaker = menu()
    spreadsheet.fill_table_structure(spreadsheet.worksheet, num_processes, choice, tie_breaker, quantum)
    ut.openExcel()

    print(
        """
The file data.xlsx has been created in the current directory.
Modify the file as needed and press Enter to continue.
"""
    )
    input("Press Enter to continue...")

    switch_choice(choice, quantum, tie_breaker)


if __name__ == "__main__":
    main()
