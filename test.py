import threading
import tkinter as tk
import tkinter.messagebox as msg
# Read a Excel file and show in a console the content

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
    df = pd.read_excel(EXCEL_FILE, sheet_name=TASKS_SHEET)

    # Format the date column
    df[DATE] = pd.to_datetime(df[DATE], format="%Y%m%d").dt.strftime("%d/%m/%Y")

    tasks_info = []

    for index, row in df.iterrows():
        description = row[DESCRIPTION]
        date = row[DATE]
        start_time = row[START_TIME].strftime("%I:%M:%p")
        end_time = row[END_TIME].strftime("%I:%M:%p")
        dedicated_time = row[DEDICATED_TIME].strftime("%H:%M")
        task_tw = row[TASK_TW]
        tasks_info.append(
            {
                'description': description,
                'date': date,
                'start_time': start_time,
                'end_time': end_time,
                'dedicated_time': dedicated_time,
                'task_tw': task_tw,
            }
        )
        print(description, date, start_time, end_time, dedicated_time, task_tw)

    return tasks_info

def proceso_largo():
    # Aquí va el código del proceso que tarda mucho
    # Puedes usar try-except para capturar posibles errores
    try:
        # Simulamos un proceso que tarda 10 segundos
        import time
        time.sleep(10)
        # Si el proceso termina con éxito, mostramos un mensaje de información
        msg.showinfo("Proceso terminado", "El proceso ha finalizado correctamente.")
    except Exception as e:
        # Si el proceso falla, mostramos un mensaje de error con la excepción
        msg.showerror("Error en el proceso", f"El proceso ha fallado por el siguiente motivo:\n{e}")

def iniciar_proceso():
    # Creamos un hilo para ejecutar el proceso largo
    hilo = threading.Thread(target=proceso_largo)
    # Iniciamos el hilo
    hilo.start()
    # Mostramos un mensaje de que el proceso está en curso
    msg.showinfo("Proceso en curso", "El proceso está en curso. Por favor, espere...")

# Creamos la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación con Tkinter")
ventana.geometry("300x200")

# Creamos un botón para iniciar el proceso
boton = tk.Button(ventana, text="Iniciar proceso", command=iniciar_proceso)
boton.pack(padx=10, pady=10)

# Iniciamos el bucle principal de la ventana
# ventana.mainloop()

test = 'This is a test'
print(f"Test: {test}")

tasks = obtain_tasks_info()
print(tasks)
hour_parts = tasks[0]['start_time'].split(":")
# hour_parts = [part[1:] if part.startswith('0') else part for part in hour_parts]
# print(hour_parts)

hour, minute, indicator = [part[1:] if part.startswith('0') else part for part in hour_parts]
print(hour, minute, indicator)