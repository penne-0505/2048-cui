import curses
from typing import Any

from core.config import is_emoji_enabled
from core.constants import ENTER_KEY_CODES, ESCAPE_KEY_CODE
from core.i18n import t
from core.save_load import MANUAL_SAVE_SLOTS, get_all_save_slots_info, get_save_slots
from ui.input import get_text_input


def select_from_menu(
    stdscr: curses.window, title: str, options: list[str]
) -> str | None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 1, title)

    current_option = 0
    while True:
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.addstr(i + 2, 4, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 4, f"  {option}")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in ENTER_KEY_CODES:
            return options[current_option]
        elif key in [ord("q"), ESCAPE_KEY_CODE]:
            return None


def show_start_menu(stdscr: curses.window, config: Any = None) -> str | None:
    emoji_on = config and is_emoji_enabled(config)

    options = [t("menu.new_game", use_emoji=emoji_on)]
    if get_save_slots():
        options.append(t("menu.load_game", use_emoji=emoji_on))
    options.append(t("menu.settings", use_emoji=emoji_on))

    choice = select_from_menu(stdscr, t("menu.welcome_title"), options)

    # Parse choice regardless of emoji
    if choice and (
        t("menu.new_game") in choice or t("menu.new_game", use_emoji=True) in choice
    ):
        return "new"
    elif choice and (
        t("menu.load_game") in choice or t("menu.load_game", use_emoji=True) in choice
    ):
        return "load"
    elif choice and (
        t("menu.settings") in choice or t("menu.settings", use_emoji=True) in choice
    ):
        return "settings"
    return None


def show_load_menu(
    stdscr: curses.window, config: dict[str, Any] | None = None
) -> int | None:
    slots_info = get_all_save_slots_info(config)
    if not slots_info:
        return None

    # Create display options with score information
    options = []
    slot_mapping = {}

    for info in slots_info:
        status = t("game.game_over") if info["game_over"] else t("game.in_progress")
        display_text = f"{info['name']} ({t('game.slot')} {info['slot']}): {t('game.score')} {info['score']} ({status}) - {info['date']}"
        options.append(display_text)
        slot_mapping[display_text] = info["slot"]

    choice = select_from_menu(stdscr, t("game.load.title"), options)
    if choice and choice in slot_mapping:
        return slot_mapping[choice]
    return None


def show_save_menu(
    stdscr: curses.window, config: dict[str, Any] | None = None
) -> tuple[int, str] | None:
    # Get existing save slot info to show current names
    slots_info = get_all_save_slots_info(config)
    existing_slots = {info["slot"]: info["name"] for info in slots_info}

    options = []
    slot_mapping = {}

    for i in range(1, MANUAL_SAVE_SLOTS + 1):
        existing_name = existing_slots.get(i, "")
        if existing_name:
            display_text = f"{t('game.slot')} {i}: {existing_name}"
        else:
            display_text = f"{t('game.slot')} {i}: {t('game.empty')}"
        options.append(display_text)
        slot_mapping[display_text] = i

    choice = select_from_menu(stdscr, t("game.save.title"), options)
    if choice and choice in slot_mapping:
        slot = slot_mapping[choice]

        # Get save name from user
        current_name = existing_slots.get(slot, "")
        prompt = (
            t("game.save.name_current", current_name)
            if current_name
            else t("game.save.name_prompt")
        )
        name = get_text_input(stdscr, prompt)

        if name is not None:  # User didn't cancel
            return slot, name
    return None
