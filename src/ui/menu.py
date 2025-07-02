import curses

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
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return options[current_option]
        elif key in [ord("q"), 27]:
            return None


def show_start_menu(stdscr: curses.window) -> str | None:
    options = ["New Game"]
    if get_save_slots():
        options.append("Load Game")

    choice = select_from_menu(stdscr, "Welcome to 2048!", options)
    if choice == "New Game":
        return "new"
    elif choice == "Load Game":
        return "load"
    return None


def show_load_menu(stdscr: curses.window) -> int | None:
    slots_info = get_all_save_slots_info()
    if not slots_info:
        return None

    # Create display options with score information
    options = []
    slot_mapping = {}

    for info in slots_info:
        status = "Game Over" if info["game_over"] else "In Progress"
        display_text = f"{info['name']} (Slot {info['slot']}): Score {info['score']} ({status}) - {info['date']}"
        options.append(display_text)
        slot_mapping[display_text] = info["slot"]

    choice = select_from_menu(stdscr, "Select a save slot to load:", options)
    if choice and choice in slot_mapping:
        return slot_mapping[choice]
    return None


def show_save_menu(stdscr: curses.window) -> tuple[int, str] | None:
    # Get existing save slot info to show current names
    slots_info = get_all_save_slots_info()
    existing_slots = {info["slot"]: info["name"] for info in slots_info}

    options = []
    slot_mapping = {}

    for i in range(1, MANUAL_SAVE_SLOTS + 1):
        existing_name = existing_slots.get(i, "")
        if existing_name:
            display_text = f"Slot {i}: {existing_name}"
        else:
            display_text = f"Slot {i}: [Empty]"
        options.append(display_text)
        slot_mapping[display_text] = i

    choice = select_from_menu(stdscr, "Select a slot to save:", options)
    if choice and choice in slot_mapping:
        slot = slot_mapping[choice]

        # Get save name from user
        current_name = existing_slots.get(slot, "")
        prompt = (
            f"Enter name for save (current: '{current_name}'):"
            if current_name
            else "Enter name for save:"
        )
        name = get_text_input(stdscr, prompt)

        if name is not None:  # User didn't cancel
            return slot, name
    return None
