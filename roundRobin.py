"""
Posibles tie-breakers:
1. FCFS
2 - 3. SJF, SRTF
4. Priority
SJF and SRTF will be treated as the same algorithm (order by burst time).
"""

import utilities as ut

ties = {
    "FCFS": None,
    "SJF": "Burst Time",
    "SRTF": "Burst Time",
    "Priority": "Priority",
}

dataframe = None


def initialize():
    global dataframe
    dataframe = ut.loadData()


def planner(quantum):
    initialize()
    global dataframe

    print(
        "Round Robin Scheduling",
        "Quantum:",
        quantum,
    )

    process_list = []
    for i in range(len(dataframe)):
        process = dataframe.iloc[i]
        process_list.append(
            {
                "Process ID": process.name,
                "Arrival Time": process["Arrival Time"],
                "Burst Time": process["Burst Time"],
                "Waiting Time": 0,
                "Completition Time": None,
            }
        )

    process_list.sort(key=lambda x: (x["Arrival Time"]))
    num_processes = len(process_list)
    gantt_chart = []
    completed = []
    time = 0

    while len(completed) != num_processes:
        for process in process_list:
            if process["Arrival Time"] <= time and process["Burst Time"] > 0:
                initial_time = time
                if process["Burst Time"] <= quantum:
                    time += process["Burst Time"]
                    process["Burst Time"] = 0
                    process["Completition Time"] = time
                    process["Waiting Time"] = (
                        process["Completition Time"] - process["Arrival Time"]
                    ) - dataframe.loc[process["Process ID"], "Burst Time"]
                    gantt_chart.append([initial_time, time, process["Process ID"]])
                    completed.append(process)
                    continue
                else:
                    time += quantum
                    process["Burst Time"] -= quantum
                    gantt_chart.append([initial_time, time, process["Process ID"]])

    for p in completed:
        dataframe.loc[p["Process ID"], "Waiting Time"] = p["Waiting Time"]
        dataframe.loc[p["Process ID"], "Response Time"] = (
            p["Completition Time"] - p["Arrival Time"]
        )

    dataframe = ut.getDataframeAverages(dataframe)
    ut.dataframeToExcel(dataframe)

    ut.openExcel()
    ut.ganttChart(gantt_chart, "Round Robin Scheduling")

