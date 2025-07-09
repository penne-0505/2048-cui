import curses
import os
from typing import Any

from core.config import (
    get_animation_speed,
    get_save_path,
    is_animations_enabled,
    save_config,
    set_animation_speed,
    set_animations_enabled,
    set_save_path,
)
from core.constants import ESCAPE_KEY_CODE
from core.i18n import t
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
    """Show the key configuration menu (keys only)."""
    while True:
        options = [
            t("keys.movement_keys"),
            t("keys.action_keys"),
            t("settings.back"),
        ]

        choice = select_from_menu(stdscr, t("keys.title"), options)

        if choice == t("keys.movement_keys"):
            configure_movement_keys(stdscr, config)
        elif choice == t("keys.action_keys"):
            configure_action_keys(stdscr, config)
        elif choice == t("settings.back") or choice is None:
            break


def configure_movement_keys(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure movement key bindings."""
    while True:
        options = []
        for act in ["up", "down", "left", "right"]:
            keys = config["keys"]["movement"][act]
            key_display = ", ".join(get_key_display_name(key) for key in keys)
            options.append(f"{get_action_display_name('movement', act)}: {key_display}")

        options.append(t("settings.back"))

        choice = select_from_menu(stdscr, t("keys.movement_keys"), options)

        if choice == t("settings.back") or choice is None:
            break

        # Extract action from choice
        action: str | None = None
        for i, act in enumerate(["up", "down", "left", "right"]):
            if choice.startswith(get_action_display_name("movement", act)):
                action = act
                break

        if action is not None:
            configure_single_action(stdscr, config, "movement", action)


def configure_action_keys(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure action key bindings."""
    while True:
        options = []
        for act in ["quit", "save", "return_to_title", "load", "change_theme"]:
            keys = config["keys"]["actions"][act]
            key_display = ", ".join(get_key_display_name(key) for key in keys)
            options.append(f"{get_action_display_name('actions', act)}: {key_display}")

        options.append(t("settings.back"))

        choice = select_from_menu(stdscr, t("keys.action_keys"), options)

        if choice == t("settings.back") or choice is None:
            break

        # Extract action from choice
        action: str | None = None
        for act in ["quit", "save", "return_to_title", "load", "change_theme"]:
            if choice.startswith(get_action_display_name("actions", act)):
                action = act
                break

        if action is not None:
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
            options.append(t("keys.configure.remove_key", get_key_display_name(key)))

        options.extend([t("keys.configure.add_new_key"), t("messages.back")])

        title = t("keys.configure.title", get_action_display_name(category, action))
        choice = select_from_menu(stdscr, title, options)

        if choice == t("messages.back") or choice is None:
            break
        elif choice == t("keys.configure.add_new_key"):
            add_new_key_binding(stdscr, config, category, action)
        elif choice.startswith(t("keys.configure.remove_key", "").split(":")[0]):
            # Extract the key name from the choice
            key_display_name = choice.split(": ", 1)[1]
            # Find the actual key string (reverse lookup from display name)
            for key in keys:
                if get_key_display_name(key) == key_display_name:
                    success, error = remove_key_binding(config, category, action, key)
                    if success:
                        if save_config(config):
                            show_message(
                                stdscr,
                                t("keys.configure.removed_binding", get_key_display_name(key)),
                            )
                        else:
                            show_message(
                                stdscr,
                                t("keys.configure.remove_failed"),
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
    stdscr.addstr(2, 1, t("keys.configure.bind_prompt"))
    stdscr.addstr(3, 1, t("keys.configure.safe_keys_only"))
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
            t("keys.configure.key_not_safe", get_key_display_name(key_str)),
        )
        return

    # Try to add the binding
    success, error = add_key_binding(config, category, action, key_str)

    if success:
        if save_config(config):
            show_message(stdscr, t("keys.configure.added_binding", get_key_display_name(key_str)))
        else:
            show_message(stdscr, t("keys.configure.binding_failed"))
    else:
        show_message(stdscr, f"Error: {error}")


def confirm_reset_keys(stdscr: curses.window) -> bool:
    """Confirm if user wants to reset key bindings to defaults."""
    options = [t("messages.yes"), t("messages.no")]
    choice = select_from_menu(
        stdscr, t("messages.confirm_reset_keys"), options
    )
    return choice == t("messages.yes")


def reset_to_defaults(config: dict[str, Any]) -> bool:
    """Reset key bindings to default values. Returns True if successful."""
    from typing import cast

    from core.config import DEFAULT_CONFIG

    default_keys = cast(dict[str, Any], DEFAULT_CONFIG["keys"])
    config["keys"] = default_keys.copy()
    return save_config(config)


def show_message(stdscr: curses.window, message: str) -> None:
    """Show a message to the user and wait for key press."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    stdscr.addstr(height // 2, 1, message)
    stdscr.addstr(height // 2 + 2, 1, t("ui.input.any_key_continue"))
    stdscr.refresh()

    stdscr.getch()


def show_key_bindings_help(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show current key bindings as help text."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    y = 0
    stdscr.addstr(y, 1, "Current Key Bindings:")  # This can stay as is for help display
    y += 2

    # Movement keys
    stdscr.addstr(y, 1, "Movement:")  # This can stay as is for help display
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
    stdscr.addstr(y, 1, "Actions:")  # This can stay as is for help display
    y += 1
    for action in ["quit", "save", "return_to_title", "load", "change_theme"]:
        keys = config["keys"]["actions"][action]
        key_display = ", ".join(get_key_display_name(key) for key in keys)
        stdscr.addstr(
            y, 3, f"{get_action_display_name('actions', action)}: {key_display}"
        )
        y += 1

    stdscr.addstr(height - 2, 1, t("ui.input.any_key_continue"))
    stdscr.refresh()
    stdscr.getch()


def configure_save_path(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure save path settings."""
    while True:
        current_path = get_save_path(config)
        default_path = get_default_save_path()

        options = [
            f"Current: {current_path or '(Default)'}",
            t("file.path.set_custom"),
            t("file.path.reset_default"),
            t("messages.back"),
        ]

        # Add current path info to the first option
        if current_path:
            options[0] = f"Current: {current_path}"
        else:
            options[0] = f"Current: (Default - {default_path})"

        choice = select_from_menu(stdscr, t("file.path.title"), options)

        if choice == t("file.path.set_custom"):
            prompt = t("file.path.prompt")
            new_path = get_text_input(stdscr, prompt)

            if new_path is not None:
                # Validate the path
                if new_path.strip() == "":
                    if set_save_path(config, None):
                        show_message(stdscr, t("file.path.empty_path"))
                    else:
                        show_message(stdscr, t("messages.config_save_error"))
                else:
                    try:
                        # Try to create the directory to validate the path
                        os.makedirs(new_path, exist_ok=True)
                        if set_save_path(config, new_path):
                            show_message(stdscr, t("file.path.path_set", new_path))
                        else:
                            show_message(
                                stdscr, t("file.path.save_failed")
                            )
                    except Exception as e:
                        show_message(stdscr, t("file.path.invalid_path", str(e)))

        elif choice == t("file.path.reset_default"):
            if confirm_reset_save_path(stdscr):
                if set_save_path(config, None):
                    show_message(stdscr, t("file.path.path_reset"))
                else:
                    show_message(
                        stdscr, t("file.path.reset_failed")
                    )

        elif choice == t("messages.back") or choice is None:
            break


def confirm_reset_save_path(stdscr: curses.window) -> bool:
    """Confirm resetting save path to default."""
    options = [t("messages.yes"), t("messages.no")]
    choice = select_from_menu(stdscr, t("file.path.confirm_reset"), options)
    return choice == t("messages.yes")


def configure_animations(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure animation settings."""
    while True:
        enabled = is_animations_enabled(config)
        speed = get_animation_speed(config)
        
        options = [
            f"{t('visual.animation.enabled')}: {t('messages.enabled') if enabled else t('messages.disabled')}",
            f"{t('visual.animation.speed')}: {speed:.1f}x",
            t("messages.back"),
        ]
        
        choice = select_from_menu(stdscr, t("visual.animation.title"), options)
        
        if choice == t("messages.back") or choice is None:
            break
        elif choice.startswith(t("visual.animation.enabled")):
            toggle_animations(stdscr, config)
        elif choice.startswith(t("visual.animation.speed")):
            configure_animation_speed(stdscr, config)


def toggle_animations(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Toggle animation on/off."""
    current_state = is_animations_enabled(config)
    new_state = not current_state
    
    if set_animations_enabled(config, new_state):
        state_text = t("messages.animation_enabled") if new_state else t("messages.animation_disabled")
        show_message(stdscr, state_text)
    else:
        show_message(stdscr, t("messages.animation_save_failed"))


def configure_animation_speed(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure animation speed."""
    current_speed = get_animation_speed(config)
    speed_options = [
        t("visual.animation.values.slow"),
        t("visual.animation.values.normal"),
        t("visual.animation.values.fast"),
        t("visual.animation.values.very_fast"),
        t("messages.back")
    ]
    
    choice = select_from_menu(stdscr, f"{t('visual.animation.speed')}: {current_speed:.1f}x", speed_options)
    
    if choice == t("messages.back") or choice is None:
        return
    
    speed_map = {
        t("visual.animation.values.slow"): 0.5,
        t("visual.animation.values.normal"): 1.0,
        t("visual.animation.values.fast"): 1.5,
        t("visual.animation.values.very_fast"): 2.0,
    }
    
    new_speed = speed_map.get(choice)
    if new_speed is not None:
        if set_animation_speed(config, new_speed):
            show_message(stdscr, t("messages.animation_speed_set", new_speed))
        else:
            show_message(stdscr, t("messages.animation_speed_save_failed"))
