import curses

from src.core.save_load import MANUAL_SAVE_SLOTS, get_save_slots


def select_from_menu(stdscr, title, options):
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


def show_start_menu(stdscr):
    options = ["New Game"]
    if get_save_slots():
        options.append("Load Game")

    choice = select_from_menu(stdscr, "Welcome to 2048!", options)
    if choice == "New Game":
        return "new"
    elif choice == "Load Game":
        return "load"
    return None


def show_load_menu(stdscr):
    slots = sorted(get_save_slots())
    if not slots:
        return None

    choice = select_from_menu(stdscr, "Select a save slot to load:", slots)
    if choice:
        return int(choice.split("_")[1].split(".")[0])
    return None


def show_save_menu(stdscr):
    options = [f"Slot {i}" for i in range(1, MANUAL_SAVE_SLOTS + 1)]
    choice = select_from_menu(stdscr, "Select a slot to save:", options)
    if choice:
        return int(choice.split(" ")[1])
    return None
