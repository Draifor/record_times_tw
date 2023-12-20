from playwright.sync_api import Playwright, sync_playwright
from utils.obtainTasksInfo import obtain_tasks_info
from utils.constants import TW_URL
import tkinter.messagebox as msg
import re


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

        page.frame_locator("iframe").get_by_placeholder("Sin fecha").fill(task["date"])
        page.frame_locator("iframe").get_by_placeholder("Sin fecha").press("Tab")
        page.frame_locator("iframe").get_by_role("textbox").nth(1).click()
        hour_parts = task["start_time"].split(":")
        hour, minute, indicator = [
            part[1:] if part.startswith("0") else part for part in hour_parts
        ]
        print(hour, minute, indicator)

        print("Aqui estoy")
        # Asign the action to the hour
        if (
            hour == "12"
            or hour == "1"
            or hour == "2"
            or hour == "3"
            or hour == "4"
            or hour == "6"
            or hour == "7"
            or hour == "8"
            or hour == "9"
        ):
            page.frame_locator("iframe").get_by_text(hour, exact=True).click()
        elif hour == "5":
            print("Aqui estoy5")
            # page.frame_locator("iframe").get_by_text(hour, exact=True).first().click()
            page.frame_locator("iframe").locator("a").filter(
                has_text=re.compile(rf"^{hour}$")
            ).nth(1).click()
        elif hour == "10":
            page.frame_locator("iframe").get_by_text(hour).first().click()
        elif hour == "11":
            page.frame_locator("iframe").get_by_text(hour).click()
        else:
            msg.showerror(
                "Ocurrió un error",
                f"Por favor verifica que la hora\n{task['start_time']}\nsea válida",
            )

        # try:
        #     page.frame_locator("iframe").locator("a").filter(
        #         has_text=re.compile(rf"^{hour}$")
        #     ).click()
        # except Exception as e:
        #     error_message = f"Error: {e}"
        #     print(error_message)
        #     if "strict mode violation" in error_message:
        #         page.frame_locator("iframe").locator("a").filter(
        #             has_text=re.compile(rf"^{hour}$")
        #         ).nth(1).click()

        print("Aqui estoy0")
        # Assign the action to the minute
        if minute == "0" or minute == "15" or minute == "20" or minute == "50":
            page.frame_locator("iframe").get_by_text(minute, exact=True).click()
        elif minute == "5":
            page.frame_locator("iframe").get_by_text(minute, exact=True).nth(1).click()
        elif minute == "10":
            page.frame_locator("iframe").get_by_text(minute).nth(1).click()
        elif (
            minute == "25"
            or minute == "30"
            or minute == "35"
            or minute == "40"
            or minute == "45"
            or minute == "55"
        ):
            page.frame_locator("iframe").get_by_text(minute).click()

        # try:
        #     page.frame_locator("iframe").locator("a").filter(
        #         has_text=re.compile(rf"^{minute}$")
        #     ).click()
        # except Exception as e:
        #     error_message = f"Error: {e}"
        #     print(error_message)
        #     if "strict mode violation" in error_message:
        #         page.frame_locator("iframe").locator("a").filter(
        #             has_text=re.compile(rf"^{minute}$")
        #         ).nth(2).click()
        print("Aqui estoy1")

        # Assign the action to the indicator
        page.frame_locator("iframe").get_by_text(indicator, exact=True).click()
        # page.frame_locator("iframe").locator("a").filter(
        #     has_text=re.compile(rf"^{indicator}$")
        # ).click()

        print("Aqui estoy2")

        page.frame_locator("iframe").get_by_role("textbox").nth(3).click()
        print("Aqui estoy3")
        page.frame_locator("iframe").get_by_role("textbox").nth(3).fill(
            task["dedicated_time"]
        )

        print("Aqui estoy4")
        page.frame_locator("iframe").locator(
            "#addOrEditTimeEntryDescriptionInput"
        ).fill(task["description"])
        page.frame_locator("iframe").get_by_role(
            "button", name="Registar esta Hora"
        ).click()

    # ---------------------
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()


def startProcess(username: str, password: str):
    with sync_playwright() as playwright:
        tasks_info = obtain_tasks_info()
        mainProcess(playwright, username, password, tasks_info)
