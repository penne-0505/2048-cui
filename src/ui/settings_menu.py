"""
Settings menu system for 2048-CLI.
Provides a well-organized menu structure for game configuration.
"""

import curses
from typing import Any

from core.i18n import t
from ui.key_config_menu import show_message
from ui.menu import select_from_menu


def show_settings_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show the main settings menu with organized categories."""
    from core.config import is_emoji_enabled

    while True:
        emoji_on = is_emoji_enabled(config)

        options = [
            t("settings.key_settings", use_emoji=emoji_on),
            t("settings.visual_effects", use_emoji=emoji_on),
            t("settings.file_settings", use_emoji=emoji_on),
            t("settings.language_settings", use_emoji=emoji_on),
            t("settings.reset_defaults", use_emoji=emoji_on),
            t("settings.back_main", use_emoji=emoji_on),
        ]

        choice = select_from_menu(
            stdscr, t("settings.title", use_emoji=emoji_on), options
        )

        if choice and (
            t("settings.key_settings") in choice
            or t("settings.key_settings", use_emoji=True) in choice
        ):
            show_key_settings_menu(stdscr, config)
        elif choice and (
            t("settings.visual_effects") in choice
            or t("settings.visual_effects", use_emoji=True) in choice
        ):
            show_visual_effects_menu(stdscr, config)
        elif choice and (
            t("settings.file_settings") in choice
            or t("settings.file_settings", use_emoji=True) in choice
        ):
            show_file_settings_menu(stdscr, config)
        elif choice and (
            t("settings.language_settings") in choice
            or t("settings.language_settings", use_emoji=True) in choice
        ):
            show_language_settings_menu(stdscr, config)
        elif choice and (
            t("settings.reset_defaults") in choice
            or t("settings.reset_defaults", use_emoji=True) in choice
        ):
            if confirm_reset_all_settings(stdscr):
                if reset_all_settings_to_defaults(config):
                    show_message(stdscr, t("messages.reset_success"))
                else:
                    show_message(stdscr, t("messages.reset_error"))
        elif (
            choice
            and (
                t("settings.back_main") in choice
                or t("settings.back_main", use_emoji=True) in choice
            )
            or choice is None
        ):
            break


def show_key_settings_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show key configuration settings."""
    from core.config import is_emoji_enabled
    from ui.key_config_menu import configure_action_keys, configure_movement_keys

    while True:
        emoji_on = is_emoji_enabled(config)

        options = [
            t("keys.movement_keys", use_emoji=emoji_on),
            t("keys.action_keys", use_emoji=emoji_on),
            t("settings.back", use_emoji=emoji_on),
        ]

        choice = select_from_menu(stdscr, t("keys.title", use_emoji=emoji_on), options)

        if choice and (
            t("keys.movement_keys") in choice
            or t("keys.movement_keys", use_emoji=True) in choice
        ):
            configure_movement_keys(stdscr, config)
        elif choice and (
            t("keys.action_keys") in choice
            or t("keys.action_keys", use_emoji=True) in choice
        ):
            configure_action_keys(stdscr, config)
        elif (
            choice
            and (
                t("settings.back") in choice
                or t("settings.back", use_emoji=True) in choice
            )
            or choice is None
        ):
            break


def show_visual_effects_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show visual effects and animation settings."""
    from core.config import is_emoji_enabled
    from ui.key_config_menu import configure_animations

    while True:
        emoji_on = is_emoji_enabled(config)

        options = [
            t("visual.animation_settings", use_emoji=emoji_on),
            t("visual.emoji_display", use_emoji=emoji_on),
            t("settings.back", use_emoji=emoji_on),
        ]

        choice = select_from_menu(
            stdscr, t("visual.title", use_emoji=emoji_on), options
        )

        if choice and (
            t("visual.animation_settings") in choice
            or t("visual.animation_settings", use_emoji=True) in choice
        ):
            configure_animations(stdscr, config)
        elif choice and (
            t("visual.emoji_display") in choice
            or t("visual.emoji_display", use_emoji=True) in choice
        ):
            configure_emoji_display(stdscr, config)
        elif (
            choice
            and (
                t("settings.back") in choice
                or t("settings.back", use_emoji=True) in choice
            )
            or choice is None
        ):
            break


def show_file_settings_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show file and save path settings."""
    from core.config import is_emoji_enabled
    from ui.key_config_menu import configure_save_path

    while True:
        emoji_on = is_emoji_enabled(config)

        options = [
            t("file.save_path", use_emoji=emoji_on),
            t("settings.back", use_emoji=emoji_on),
        ]

        choice = select_from_menu(stdscr, t("file.title", use_emoji=emoji_on), options)

        if choice and (
            t("file.save_path") in choice
            or t("file.save_path", use_emoji=True) in choice
        ):
            configure_save_path(stdscr, config)
        elif (
            choice
            and (
                t("settings.back") in choice
                or t("settings.back", use_emoji=True) in choice
            )
            or choice is None
        ):
            break


def confirm_reset_all_settings(stdscr: curses.window) -> bool:
    """Confirm if user wants to reset all settings to defaults."""
    options = [t("messages.yes"), t("messages.no")]
    choice = select_from_menu(stdscr, t("messages.confirm_reset"), options)
    return choice == t("messages.yes")


def reset_all_settings_to_defaults(config: dict[str, Any]) -> bool:
    """Reset all settings to default values. Returns True if successful."""
    from core.config import DEFAULT_CONFIG, save_config

    # Reset all configuration sections
    config.clear()
    config.update(DEFAULT_CONFIG.copy())

    return save_config(config)


def configure_emoji_display(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Configure emoji display settings."""
    from core.config import is_emoji_enabled

    while True:
        enabled = is_emoji_enabled(config)

        options = [
            f"{t('visual.emoji_display')}: {t('messages.enabled') if enabled else t('messages.disabled')}",
            t("messages.back"),
        ]

        choice = select_from_menu(stdscr, t("visual.emoji.title"), options)

        if choice == t("messages.back") or choice is None:
            break
        elif choice and f"{t('visual.emoji_display')}:" in choice:
            toggle_emoji_display(stdscr, config)


def toggle_emoji_display(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Toggle emoji display on/off."""
    from core.config import is_emoji_enabled, set_emoji_enabled

    current_state = is_emoji_enabled(config)
    new_state = not current_state

    if set_emoji_enabled(config, new_state):
        message = (
            t("messages.emoji_enabled") if new_state else t("messages.emoji_disabled")
        )
        show_message(stdscr, message)
    else:
        show_message(stdscr, t("messages.config_save_error"))


def show_language_settings_menu(stdscr: curses.window, config: dict[str, Any]) -> None:
    """Show language selection settings."""
    from core.config import get_available_languages, get_language, is_emoji_enabled
    from core.i18n import get_i18n_manager

    while True:
        emoji_on = is_emoji_enabled(config)
        current_language = get_language(config)
        available_languages = get_available_languages()
        i18n_manager = get_i18n_manager()

        # Build language display options
        language_options = []
        for lang_code in available_languages:
            display_name = i18n_manager.get_language_display_name(lang_code)
            marker = " ✓" if lang_code == current_language else ""
            language_options.append(f"{display_name}{marker}")

        language_options.append(t("settings.back", use_emoji=emoji_on))

        choice = select_from_menu(
            stdscr, t("language.title", use_emoji=emoji_on), language_options
        )

        if (
            choice
            and (
                t("settings.back") in choice
                or t("settings.back", use_emoji=True) in choice
            )
            or choice is None
        ):
            break
        elif choice:
            # Find selected language code
            for i, lang_code in enumerate(available_languages):
                display_name = i18n_manager.get_language_display_name(lang_code)
                if choice.startswith(display_name):
                    if lang_code != current_language:
                        change_language(stdscr, config, lang_code)
                    break


def change_language(
    stdscr: curses.window, config: dict[str, Any], language_code: str
) -> None:
    """Change the application language."""
    from core.config import set_language
    from core.i18n import get_i18n_manager

    i18n_manager = get_i18n_manager()

    if set_language(config, language_code):
        show_message(stdscr, t("language.success"))
    else:
        show_message(stdscr, t("language.error"))
