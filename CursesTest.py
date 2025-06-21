import curses

def main(stdscr: curses.initscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr(10, 5, "First Position(10, 5)")
    stdscr.addstr(20, 5, "Second Position(20, 5)")
    stdscr.addstr(5, 20, "Third Position(5, 20)")

    stdscr.refresh()
    stdscr.getkey()

# Call the main function using curses.wrapper
curses.wrapper(main)