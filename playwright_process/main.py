from playwright.sync_api import Playwright, sync_playwright
from utils.obtainTasksInfo import obtain_tasks_info
from utils.constants import TW_URL
import tkinter.messagebox as msg


def mainProcess(
    playwright: Playwright, username: str, password: str, tasks_info: dict
) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(TW_URL)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.get_by_label("Email address").click()
    page.get_by_label("Email address").fill(username)
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Log in").click()
    page.frame_locator("iframe").get_by_role(
        "heading", name="Tareas", exact=True
    ).click()

    for task in tasks_info:
        page.goto(task["task_tw"])

        try:
            # page.frame_locator("iframe").get_by_label("Log time").click()
            page.frame_locator("iframe").get_by_role(
                "button", name=" Log time"
            ).click()
        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            msg.showerror(
                "Ocurrió un error",
                f"Por favor verifica que la tarea\n{task['task_tw']}\nexista y que tengas los permisos necesarios\n{error_message}",
            )

        #  Fill date
        page.get_by_label("Fecha").click()
        page.get_by_label("Fecha").fill(task["date"])
        page.get_by_label("Fecha").press("Enter")

        # Fill start time
        page.get_by_label("Hora de inicio").click()
        page.get_by_label("Hora de inicio").fill(task["start_time"])
        page.get_by_label("Hora de inicio").press("Tab")

        # Fill end time
        page.get_by_label("Hora de finalización").click()
        page.get_by_label("Hora de finalización").fill(task["end_time"])
        page.get_by_label("Hora de finalización").press("Tab")

        # Uncheck billable
        page.get_by_label("Marcar como facturable").uncheck()

        # Fill description
        page.get_by_label("Descripción").click()
        page.get_by_label("Descripción").fill(task["description"])

        # Log time
        page.get_by_role("button", name="Registrar tiempo").click()

    # ---------------------
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()


def startProcess(username: str, password: str):
    with sync_playwright() as playwright:
        tasks_info = obtain_tasks_info()
        mainProcess(playwright, username, password, tasks_info)
