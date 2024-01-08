import pandas as pd
from utils.constants import (
    EXCEL_FILE,
    TASKS_SHEET,
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

        task_tw = row[TASK_TW]
        if isinstance(task_tw, float):
            print("Task not found")
            continue
        description = row[DESCRIPTION]
        date = row[DATE]
        start_time = row[START_TIME].strftime("%I:%M %p")
        end_time = row[END_TIME].strftime("%I:%M %p")
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