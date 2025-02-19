# main.py
from logging_utils import ConsoleColor, log_message
from nicegui import ui, app as nicegui_app
from wizard.ui_builder import setup_wizard_ui
from tracing import init_tracer
from fastapi import FastAPI

sovereign_art = """
            ███████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗   ██╗
            ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║██╔═══  ╗████╗  ██║
            ███████╗██║   ██║██║   ██║█████╗  ██████╔╝█████╗  ██║██║     ║██╔██╗ ██║
            ╚════██║██║   ██║ █║   █ ║██╔══╝  ██╔══██╗██╔══╝  ██║██║ ████║██║╚██╗██║
            ███████║╚██████╔╝╚ ████ ╔╝███████╗██║  ██║███████╗██║╚██████╔╝██║ ╚████║
            ╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""

def main():
    log_message(sovereign_art, color=ConsoleColor.PURPLE)
    fastapi_app = FastAPI()
    init_tracer(fastapi_app)
    setup_wizard_ui()
    ui.run(
        port=8080,
        reload=False,
        show=False,
        language='en',
        server=fastapi_app
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()