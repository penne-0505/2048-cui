import curses
import os
from typing import Any

from core.config import get_save_path, save_config, set_save_path
from core.constants import ESCAPE_KEY_CODE
from core.key_config import (
    add_key_binding,
    code_to_key,
    get_action_display_name,
    get_key_display_name,
    is_key_safe,
    remove_key_binding,
)
from core.save_load import get_default_save_path
from ui.input import get_text_input
from ui.menu import select_from_menu


def show_key_config_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show the main key configuration menu."""
    while True:
        options = [
            "Movement Keys",
            "Action Keys",
            "Save Path Settings",
            "Reset to Defaults",
            "Back to Main Menu",
        ]

        choice = select_from_menu(stdscr, "Key Configuration", options)

        if choice == "Movement Keys":
            configure_movement_keys(stdscr, config)
        elif choice == "Action Keys":
            configure_action_keys(stdscr, config)
        elif choice == "Save Path Settings":
            configure_save_path(stdscr, config)
        elif choice == "Reset to Defaults":
            if confirm_reset_keys(stdscr):
                if reset_to_defaults(config):
                    show_message(stdscr, "Key bindings reset to defaults!")
                else:
                    show_message(
                        stdscr, "Key bindings reset but failed to save configuration"
                    )
        elif choice == "Back to Main Menu" or choice is None:
            break


def configure_movement_keys(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure movement key bindings."""
    while True:
        options = []
        for action in ["up", "down", "left", "right"]:
            keys = config["keys"]["movement"][action]
            key_display = ", ".join(get_key_display_name(key) for key in keys)
            options.append(
                f"{get_action_display_name('movement', action)}: {key_display}"
            )

        options.append("Back")

        choice = select_from_menu(stdscr, "Movement Key Configuration", options)

        if choice == "Back" or choice is None:
            break

        # Extract action from choice
        action = None
        for i, act in enumerate(["up", "down", "left", "right"]):
            if choice.startswith(get_action_display_name("movement", act)):
                action = act
                break

        if action:
            configure_single_action(stdscr, config, "movement", action)


def configure_action_keys(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure action key bindings."""
    while True:
        options = []
        for action in ["quit", "save", "return_to_title", "load", "change_theme"]:
            keys = config["keys"]["actions"][action]
            key_display = ", ".join(get_key_display_name(key) for key in keys)
            options.append(
                f"{get_action_display_name('actions', action)}: {key_display}"
            )

        options.append("Back")

        choice = select_from_menu(stdscr, "Action Key Configuration", options)

        if choice == "Back" or choice is None:
            break

        # Extract action from choice
        action = None
        for act in ["quit", "save", "return_to_title", "load", "change_theme"]:
            if choice.startswith(get_action_display_name("actions", act)):
                action = act
                break

        if action:
            configure_single_action(stdscr, config, "actions", action)


def configure_single_action(
    stdscr: curses.window, config: dict[str, Any], category: str, action: str
) -> None:
    """Configure key bindings for a single action."""
    while True:
        keys = config["keys"][category][action]
        options = []

        # Show current bindings
        for key in keys:
            options.append(f"Remove: {get_key_display_name(key)}")

        options.extend(["Add New Key", "Back"])

        title = f"Configure {get_action_display_name(category, action)}"
        choice = select_from_menu(stdscr, title, options)

        if choice == "Back" or choice is None:
            break
        elif choice == "Add New Key":
            add_new_key_binding(stdscr, config, category, action)
        elif choice.startswith("Remove: "):
            key_to_remove = choice.replace("Remove: ", "")
            # Find the actual key string (reverse lookup from display name)
            for key in keys:
                if get_key_display_name(key) == key_to_remove:
                    success, error = remove_key_binding(config, category, action, key)
                    if success:
                        if save_config(config):
                            show_message(
                                stdscr,
                                f"Removed key binding: {get_key_display_name(key)}",
                            )
                        else:
                            show_message(
                                stdscr,
                                "Key binding removed but failed to save configuration",
                            )
                    else:
                        show_message(stdscr, f"Error: {error}")
                    break


def add_new_key_binding(
    stdscr: curses.window, config: dict[str, Any], category: str, action: str
) -> None:
    """Add a new key binding for an action."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Show instructions
    stdscr.addstr(0, 1, f"Add key for {get_action_display_name(category, action)}")
    stdscr.addstr(2, 1, "Press the key you want to bind, or ESC to cancel")
    stdscr.addstr(3, 1, "Only safe keys from the whitelist are allowed")
    stdscr.refresh()

    # Get key press
    key = stdscr.getch()

    if key == ESCAPE_KEY_CODE:  # ESC
        return

    # Convert key code to key string
    key_str = code_to_key(key)

    # Check if key is safe
    if not is_key_safe(key_str):
        show_message(
            stdscr,
            f"Key '{get_key_display_name(key_str)}' is not in the safe bindable keys list",
        )
        return

    # Try to add the binding
    success, error = add_key_binding(config, category, action, key_str)

    if success:
        if save_config(config):
            show_message(stdscr, f"Added key binding: {get_key_display_name(key_str)}")
        else:
            show_message(stdscr, "Key binding added but failed to save configuration")
    else:
        show_message(stdscr, f"Error: {error}")


def confirm_reset_keys(stdscr: curses.window) -> bool:
    """Confirm if user wants to reset key bindings to defaults."""
    options = ["Yes", "No"]
    choice = select_from_menu(
        stdscr, "Are you sure you want to reset all key bindings to defaults?", options
    )
    return choice == "Yes"


def reset_to_defaults(config: dict[str, Any]) -> bool:
    """Reset key bindings to default values. Returns True if successful."""
    from core.config import DEFAULT_CONFIG

    config["keys"] = DEFAULT_CONFIG["keys"].copy()
    return save_config(config)


def show_message(stdscr: curses.window, message: str) -> None:
    """Show a message to the user and wait for key press."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    stdscr.addstr(height // 2, 1, message)
    stdscr.addstr(height // 2 + 2, 1, "Press any key to continue...")
    stdscr.refresh()

    stdscr.getch()


def show_key_bindings_help(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show current key bindings as help text."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = 0
    stdscr.addstr(y, 1, "Current Key Bindings:")
    y += 2

    # Movement keys
    stdscr.addstr(y, 1, "Movement:")
    y += 1
    for action in ["up", "down", "left", "right"]:
        keys = config["keys"]["movement"][action]
        key_display = ", ".join(get_key_display_name(key) for key in keys)
        stdscr.addstr(
            y, 3, f"{get_action_display_name('movement', action)}: {key_display}"
        )
        y += 1

    y += 1
    # Action keys
    stdscr.addstr(y, 1, "Actions:")
    y += 1
    for action in ["quit", "save", "return_to_title", "load", "change_theme"]:
        keys = config["keys"]["actions"][action]
        key_display = ", ".join(get_key_display_name(key) for key in keys)
        stdscr.addstr(
            y, 3, f"{get_action_display_name('actions', action)}: {key_display}"
        )
        y += 1

    stdscr.addstr(height - 2, 1, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()


def configure_save_path(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure save path settings."""
    while True:
        current_path = get_save_path(config)
        default_path = get_default_save_path()

        options = [
            f"Current: {current_path or '(Default)'}",
            "Set Custom Path",
            "Reset to Default",
            "Back",
        ]

        # Add current path info to the first option
        if current_path:
            options[0] = f"Current: {current_path}"
        else:
            options[0] = f"Current: (Default - {default_path})"

        choice = select_from_menu(stdscr, "Save Path Settings", options)

        if choice == "Set Custom Path":
            prompt = "Enter custom save path (or press Escape to cancel):"
            new_path = get_text_input(stdscr, prompt)

            if new_path is not None:
                # Validate the path
                if new_path.strip() == "":
                    if set_save_path(config, None):
                        show_message(stdscr, "Empty path! Setting to default.")
                    else:
                        show_message(stdscr, "Failed to save path configuration")
                else:
                    try:
                        # Try to create the directory to validate the path
                        os.makedirs(new_path, exist_ok=True)
                        if set_save_path(config, new_path):
                            show_message(stdscr, f"Save path set to: {new_path}")
                        else:
                            show_message(
                                stdscr, "Path set but failed to save configuration"
                            )
                    except Exception as e:
                        show_message(stdscr, f"Invalid path: {str(e)}")

        elif choice == "Reset to Default":
            if confirm_reset_save_path(stdscr):
                if set_save_path(config, None):
                    show_message(stdscr, "Save path reset to default!")
                else:
                    show_message(
                        stdscr, "Save path reset but failed to save configuration"
                    )

        elif choice == "Back" or choice is None:
            break


def confirm_reset_save_path(stdscr: curses.window) -> bool:
    """Confirm resetting save path to default."""
    options = ["Yes", "No"]
    choice = select_from_menu(stdscr, "Reset save path to default?", options)
    return choice == "Yes"
