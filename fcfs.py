"""
Posible tie-breakers:
1  FCFS -> Arrival Time
2 -3. SJF, SRTF -> Burst Time
4. Priority -> Priority

Only priority scheduling has a tie-breaker different from the others.
The other tie-breakers will act as a default value.
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


def planner(tie_breaker):
    initialize()
    global dataframe

    print("First-Come, First-Served Scheduling", "Tie-breaker:", tie_breaker)

    dataframe = dfSort(dataframe, tie_breaker)

    gantt_chart = []
    time = 0

    for i in range(len(dataframe)):
        process = dataframe.iloc[i]

        # Since the processes are sorted, the waiting time of the
        # first process is the time
        if process["Arrival Time"] > time:
            time = process["Arrival Time"]

        dataframe.loc[process.name, "Waiting Time"] = time - process["Arrival Time"]
        dataframe.loc[process.name, "Response Time"] = time + process["Burst Time"]

        gantt_chart.append([time, process["Response Time"], process.name])

        time += process["Burst Time"]

    ut.dataframeToExcel(dataframe)
    ut.openExcel()
    ut.ganttChart(gantt_chart, "First-Come, First-Served Scheduling")


def dfSort(dataframe, tie_breaker):
    dataframe.sort_values(by=["Arrival Time"], inplace=True)

    if tie_breaker != "FCFS":
        dataframe.sort_values(by=["Arrival Time", ties[tie_breaker]], inplace=True)

    return dataframe
