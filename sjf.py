"""
Posible tie-breakers:
1. FCFS
2-3. SJF, SRTF
4. Priority

SJF and SRTF on will be treated as the same algorithm.
"""

import utilities as ut

ties = {
    "FCFS": "Arrival Time",
    "SJF": "Burst Time",
    "SRTF": "Burst Time",
    "Priority": "Priority",
}

dataframe = None


def initialize():
    global dataframe
    dataframe = ut.loadData()


def nonPreemptive(tie_breaker):
    initialize()
    global dataframe

    print("Shortest Job First (SJF)", "Tie-breaker:", tie_breaker)

    gantt_chart = []
    time = 0
    process_list = []

    for p in range(len(dataframe)):
        process = dataframe.iloc[p]
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

    while process_list != []:
        wait_list = []

        for p in process_list:
            if p["Arrival Time"] <= time:
                wait_list.append(p)

        if wait_list == []:
            time += 1
            continue
        else:
            wait_list.sort(key=lambda x: (x["Burst Time"]))
            if ties[tie_breaker] != "Burst Time":  # If the tie-breaker is priority
                wait_list.sort(key=lambda x: (x["Burst Time"], x[ties[tie_breaker]]))

            process = wait_list.pop(0)
            process["Completition Time"] = time + process["Burst Time"]
            process["Waiting Time"] = time - process["Arrival Time"]
            gantt_chart.append(
                [time, process["Completition Time"], process["Process ID"]]
            )
            time += process["Burst Time"]
            process_list.remove(process)
            dataframe.loc[process["Process ID"], "Waiting Time"] = process[
                "Waiting Time"
            ]
            dataframe.loc[process["Process ID"], "Response Time"] = (
                process["Completition Time"] - process["Arrival Time"]
            )

    ut.dataframeToExcel(dataframe)
    ut.openExcel()
    ut.ganttChart(gantt_chart, "Shortest Job First (SJF)")


# SJF preemtive is the same as SRTF
def preemtive(tie_breaker):
    initialize()
    global dataframe

    print("Shortest Remaining Time First (SRTF)", "Tie-breaker:", tie_breaker)

    process_list = []
    for i in range(len(dataframe)):
        process = dataframe.iloc[i]
        process_list.append(
            {
                "Process ID": process.name,
                "Arrival Time": process["Arrival Time"],
                "Burst Time": process["Burst Time"],
                "Priority": process["Priority"],
                "Was Executed": False,
                "Waiting Time": 0,
                "Start Time": None,
                "Completition Time": None,
            }
        )

    process_list.sort(key=lambda x: (x["Arrival Time"], x["Burst Time"]))
    gantt_chart = []
    time = 0
    completed = []

    while process_list != []:
        wait_list = []

        for p in process_list:
            if p["Arrival Time"] <= time and p not in completed:
                wait_list.append(p)

        if wait_list == []:
            time += 1
            continue
        else:
            wait_list = waitlistSort(wait_list, tie_breaker)

            process = wait_list.pop(0)

            # If the process has not been executed
            if process["Start Time"] is None:
                process["Start Time"] = time

            # If the process was executed, but was interrupted
            if process["Was Executed"]:
                process["Start Time"] = time
                process["Was Executed"] = False

            time += 1
            process["Burst Time"] -= 1

            if process["Burst Time"] == 0:
                process["Completition Time"] = time
                completed.append(process)
                process_list.remove(process)
                gantt_chart.append([process["Start Time"], time, process["Process ID"]])

            gantt_chart, process_list = ut.updateWaitingProcesses(
                dataframe,
                process["Process ID"],
                gantt_chart,
                time,
                wait_list,
                process_list,
            )

    for p in completed:
        dataframe.loc[p["Process ID"], "Waiting Time"] = p["Waiting Time"]
        dataframe.loc[p["Process ID"], "Response Time"] = (
            p["Completition Time"] - p["Arrival Time"]
        )

    dataframe = ut.getDataframeAverages(dataframe)
    ut.dataframeToExcel(dataframe)

    print(gantt_chart)
    ut.openExcel()
    ut.ganttChart(gantt_chart, "Shortest Remaining Time First (SRTF)")


def waitlistSort(wait_list, tie_breaker):
    tie = ties[tie_breaker]
    if tie != "Burst Time":
        wait_list.sort(key=lambda x: (x["Burst Time"], x[tie]))
    else:
        wait_list.sort(key=lambda x: (x["Burst Time"]))
    return wait_list
