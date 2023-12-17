import threading
import tkinter as tk
import tkinter.messagebox as msg
# Read a Excel file and show in a console the content

import pandas as pd

df = pd.read_excel('Registro_Tiempos_TW.xlsx', sheet_name='Hoja1')

for index, row in df.iterrows():
    description = row['Descripción Tarea']
    date = row['Fecha']
    start_time = row['Hora Inicio'].strftime("%I:%M%p")
    end_time = row['Hora Fin'].strftime("%I:%M%p")
    all_time = row['Tiempo Dedicado']
    task_tw = row['Tarea TW']
    print(description, date, start_time, end_time, all_time, task_tw)



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
ventana.mainloop()

