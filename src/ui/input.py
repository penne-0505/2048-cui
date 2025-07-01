import curses


def get_text_input(stdscr, prompt, max_length=30):
    """Get text input from user with cursor navigation."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Display prompt
    prompt_y = height // 2 - 2
    stdscr.addstr(prompt_y, 2, prompt)

    # Input field
    input_y = prompt_y + 2
    input_x = 2

    # Instructions
    stdscr.addstr(input_y + 2, 2, "Press Enter to confirm, Esc to cancel")
    stdscr.addstr(input_y + 3, 2, "Use Backspace to delete characters")

    # Input box border
    box_width = min(max_length + 4, width - 4)
    stdscr.addstr(input_y - 1, input_x - 1, "+" + "-" * box_width + "+")
    stdscr.addstr(input_y, input_x - 1, "|" + " " * box_width + "|")
    stdscr.addstr(input_y + 1, input_x - 1, "+" + "-" * box_width + "+")

    # Enable cursor
    curses.curs_set(1)

    text = ""
    cursor_pos = 0

    while True:
        # Display current text
        display_text = text.ljust(max_length)[:max_length]
        stdscr.addstr(input_y, input_x, display_text)

        # Position cursor
        stdscr.move(input_y, input_x + cursor_pos)
        stdscr.refresh()

        key = stdscr.getch()

        if key == 27:  # Escape
            curses.curs_set(0)
            return None
        elif key in [10, 13]:  # Enter
            curses.curs_set(0)
            return text.strip()
        elif key in [8, 127, curses.KEY_BACKSPACE]:  # Backspace
            if cursor_pos > 0:
                text = text[: cursor_pos - 1] + text[cursor_pos:]
                cursor_pos -= 1
        elif key == curses.KEY_LEFT:
            cursor_pos = max(0, cursor_pos - 1)
        elif key == curses.KEY_RIGHT:
            cursor_pos = min(len(text), cursor_pos + 1)
        elif key == curses.KEY_HOME:
            cursor_pos = 0
        elif key == curses.KEY_END:
            cursor_pos = len(text)
        elif 32 <= key <= 126:  # Printable characters
            if len(text) < max_length:
                text = text[:cursor_pos] + chr(key) + text[cursor_pos:]
                cursor_pos += 1
