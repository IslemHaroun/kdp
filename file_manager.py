# file_manager.py

import os
from nicegui import ui
from PyQt5.QtWidgets import QApplication, QFileDialog
from logging_utils import log_message, ConsoleColor
from tracing import create_span

@create_span("open_directory_picker")
def open_directory_picker(input_field):
    """Open a directory picker and set the chosen directory into the input field."""
    try:
        if not QApplication.instance():
            _ = QApplication([])
        folder = QFileDialog.getExistingDirectory(None, "Select Directory")
        if folder:
            input_field.value = folder
            ui.notify(f"Selected directory: {folder}", color="green", position="top")
        return folder
    except Exception as e:
        log_message(f"Error in open_directory_picker: {e}", level="error", color=ConsoleColor.RED)
        ui.notify("Directory selection failed.", color="red", position="top")
        return None

@create_span("flush_directory")
def flush_directory(wizard):
    """Clear the directory selection and related UI components."""
    try:
        wizard.root_directory_input.set_value("")
        wizard.subfolder_selection_container.clear()
        wizard.subfolder_checkboxes.clear()
        ui.notify("Directory selection cleared.", color="yellow", position="top")
    except Exception as e:
        log_message(f"Error in flush_directory: {e}", level="error", color=ConsoleColor.RED)
        ui.notify("Failed to flush directory.", color="red", position="top")

@create_span("list_subfolders")
def list_subfolders(wizard):
    """List subfolders in the selected directory and display checkboxes."""
    try:
        dir_path = wizard.root_directory_input.value.strip()
        if not os.path.isdir(dir_path):
            ui.notify(f"Directory '{dir_path}' not found.", color="red", position="top")
            return
        
        # Créer un span pour le nettoyage des conteneurs
        with trace.get_tracer(__name__).start_as_current_span("clear_containers") as span:
            wizard.subfolder_selection_container.clear()
            wizard.subfolder_checkboxes.clear()
        
        # Créer un span pour la lecture des sous-dossiers
        with trace.get_tracer(__name__).start_as_current_span("read_subfolders") as span:
            subfolders = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
            span.set_attribute("subfolder_count", len(subfolders))
        
        if not subfolders:
            ui.notify("No subfolders found.", color="yellow", position="top")
            return
        
        # Créer un span pour la création des UI elements
        with trace.get_tracer(__name__).start_as_current_span("create_ui_elements") as span:
            with wizard.subfolder_selection_container:
                for folder in subfolders:
                    with ui.row().classes("items-center"):
                        cb = ui.checkbox(value=False).classes("m-2")
                        ui.label(folder).classes("m-2")
                        wizard.subfolder_checkboxes.append((folder, cb))
        
        ui.notify("Subfolders loaded.", color="green", position="top")
        log_message("Subfolders listed successfully.", session_id=wizard.session_id)
    
    except Exception as e:
        log_message(f"Error in list_subfolders: {e}", level="error", session_id=wizard.session_id)
        ui.notify("Failed to list subfolders.", color="red", position="top")