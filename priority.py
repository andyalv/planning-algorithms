"""
Possible tie-breaker values:
    1. FCFS
    2. SJF
    3. SRTF
    4. Priority
Other values are not considered in this snippet.
If tie-breaker is 4, ties would be ordered by FCFS.

This are things to consider of non_preemptive function:
    - The SJF and SRTF algorithms are treated the same way in the code.
    - The FCFS is not considered since the algorithm doesn't really needs them.
"""

import utilities as ut

ties = {
    "FCFS": "Arrival Time",
    "SJF": "Burst Time",
    "SRTF": "Burst Time",
    "Priority": "Priority",
}

dataframe = None  # Pandas DataFrame


def initialize():
    global dataframe
    dataframe = ut.loadData()


def nonPreemptive(tie_breaker):
    initialize()
    global dataframe

    print("Non-preemptive Priority Scheduling", "Tie-breaker:", tie_breaker)

    process_list = []
    for i in range(len(dataframe)):
        process = dataframe.iloc[i]
        process_list.append(
            {
                "Process ID": process.name,
                "Arrival Time": process["Arrival Time"],
                "Burst Time": process["Burst Time"],
                "Priority": process["Priority"],
                "Waiting Time": 0,
                "Completition Time": None,
            }
        )

    gantt_chart = []
    time = 0
    while process_list != []:
        wait_list = []

        for p in process_list:
            if p["Arrival Time"] <= time:
                wait_list.append(p)

        if wait_list == []:
            time += 1
            continue
        else:
            wait_list.sort(key=lambda x: (x["Priority"]))

            if ties[tie_breaker] != "Priority":  # If the tie-breaker is not priority
                wait_list.sort(key=lambda x: (x["Priority"], x[ties[tie_breaker]]))

            process = wait_list.pop(0)

            process["Waiting Time"] = time - process["Arrival Time"]
            process["Completition Time"] = time + process["Burst Time"]
            gantt_chart.append(
                [time, process["Completition Time"], process["Process ID"]]
            )
            time += process["Burst Time"]

            process_list.remove(process)
            dataframe.loc[process["Process ID"], "Waiting Time"] = process[
                "Waiting Time"
            ]
            dataframe.loc[process["Process ID"], "Response Time"] = process[
                "Completition Time"
            ]

    # Calculate the averages and add them to the dataframe
    dataframe = ut.getDataframeAverages(dataframe)
    ut.dataframeToExcel(dataframe)

    ut.openExcel()
    ut.ganttChart(gantt_chart, "Non-preemptive Priority Scheduling")


def waitlistSort(wait_list, tie_breaker):
    if tie_breaker == "FCFS":
        return sorted(wait_list, key=lambda x: (x["Priority"], x["Arrival Time"]))

    # Sort by bust time of df instead of wait_list
    elif tie_breaker in ["SJF", "SRTF"]:
        temp_list = []

        # Make a copy of df to sort it by burst time
        temp_df = dataframe.copy()
        temp_df.sort_values(by=["Priority", "Burst Time"], inplace=True)

        for p in temp_df.index:
            for q in wait_list:
                if p == q["Process ID"]:
                    temp_list.append(q)
                    break

        return temp_list

    return sorted(wait_list, key=lambda x: (x["Priority"]))


def preemptive(tie_breaker):
    initialize()
    global dataframe

    print("Preemptive Priority Scheduling", "Tie-breaker:", tie_breaker)

    # Dinamic process list
    process_list = []
    for i in range(len(dataframe)):
        process = dataframe.iloc[i]
        process_list.append(
            {
                "Priority": process["Priority"],
                "Arrival Time": process["Arrival Time"],
                "Burst Time": process["Burst Time"],
                "Waiting Time": 0,
                "Was Executed": False,
                "Process ID": process.name,
                "Start Time": None,
                "Completition Time": None,
            }
        )

    if ties[tie_breaker] == "Burst Time":
        process_list.sort(
            key=lambda x: (x["Arrival Time"], x["Priority"], x[ties[tie_breaker]])
        )
    else:
        process_list.sort(key=lambda x: (x["Arrival Time"], x["Priority"]))

    gantt_chart = []
    completed = []
    time = 0

    while process_list != []:
        wait_list = []

        for p in process_list:
            if p["Arrival Time"] <= time and p not in completed:
                wait_list.append(p)

        # If there are no processes to execute, increment time and continue
        if wait_list == []:
            time += 1
            continue
        else:
            wait_list = waitlistSort(wait_list, tie_breaker)

            process = wait_list.pop(0)  # Get the process with the highest priority

            if not process["Was Executed"]:
                # Condition to prevent the start time from being updated if the process is already running
                if process["Start Time"] is None:
                    process["Start Time"] = time
            else:  # Process Was executed and is now being executed
                process["Start Time"] = (
                    time  # Update the start time once the process is running
                )
                process["Was Executed"] = False

            time += 1
            process["Burst Time"] -= 1

            # If the process has finished, remove it from the process list, add it to the gantt chart and to the completed list
            if process["Burst Time"] == 0:
                gantt_chart.append([process["Start Time"], time, process["Process ID"]])
                process_list.remove(process)
                process["Completition Time"] = time
                completed.append(process)

        # Update waiting time for the other processes
        gantt_chart, process_list = ut.updateWaitingProcesses(
            dataframe, process["Process ID"], gantt_chart, time, wait_list, process_list
        )

    # Update the dataframe with the waiting and response times
    for p in completed:
        dataframe.loc[p["Process ID"], "Waiting Time"] = p["Waiting Time"]
        dataframe.loc[p["Process ID"], "Response Time"] = (
            p["Completition Time"] - p["Arrival Time"]
        )

    ut.dataframeToExcel(dataframe)

    print(gantt_chart)
    ut.openExcel()
    ut.ganttChart(gantt_chart, "Preemptive Priority Scheduling")
