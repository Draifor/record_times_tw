import pandas as pd
from utils.constants import (
    EXCEL_FILE,
    TASKS_SHEET,
    HISTORY_SHEET,
    DESCRIPTION,
    DATE,
    START_TIME,
    END_TIME,
    DEDICATED_TIME,
    TASK_TW,
)


def obtain_tasks_info():
    print("Obtaining tasks info...")
    df = pd.read_excel(EXCEL_FILE, sheet_name=TASKS_SHEET)

    # Format the date column
    df[DATE] = pd.to_datetime(df[DATE], format="%Y%m%d").dt.strftime("%d/%m/%Y")

    tasks_info = []

    for index, row in df.iterrows():
        try:
            dedicated_time = row[DEDICATED_TIME].strftime("%H:%M")
        except Exception as e:
            if str(e) == "'float' object has no attribute 'strftime'":
                continue
            else:
                print(e)

        description = row[DESCRIPTION]
        date = row[DATE]
        start_time = row[START_TIME].strftime("%I:%M %p")
        end_time = row[END_TIME].strftime("%I:%M %p")
        task_tw = row[TASK_TW]
        task = {
            "date": str(date),
            "start_time": start_time,
            "end_time": end_time,
            "dedicated_time": dedicated_time,
            "task_tw": task_tw,
            "description": description,
            "index": index,
        }
        tasks_info.append(task)
        print(task.values())

    print("Tasks info obtained")
    return tasks_info


def tasks_process(tasks_info):
    print("Starting tasks process...")
    finished_tasks = []
    for task in tasks_info:
        print(task)
        if isinstance(task["task_tw"], float):
            print("Task not found")
            continue
        finished_tasks.append(task)
    print("Tasks process finished")
    return finished_tasks


def move_finished_tasks_to_history(finished_tasks):
    print("Moving finished tasks to history...")
    df = pd.read_excel(EXCEL_FILE, sheet_name=TASKS_SHEET)
    df_history = pd.read_excel(EXCEL_FILE, sheet_name=HISTORY_SHEET)

    for task in finished_tasks:
        if task["index"] > 28:
            df_history = pd.concat(
                [df_history, df.loc[[task["index"]]]], ignore_index=True
            )
            df.drop(task["index"], inplace=True)

    df.to_excel(EXCEL_FILE, sheet_name=TASKS_SHEET, index=False)
    df_history.to_excel(EXCEL_FILE, sheet_name=HISTORY_SHEET, index=False)
    print("Finished tasks moved to history")


def start_process():
    print("Starting process...")
    tasks_info = obtain_tasks_info()
    tasks_info.reverse()

    finised_tasks = tasks_process(tasks_info)
    print("Process finished")
    print(finised_tasks)
    # move_finished_tasks_to_history(finised_tasks)


start_process()
