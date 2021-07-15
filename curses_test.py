import curses as c

screen = c.initscr()

def main(screen):

    window = c.newwin(40, 40, 5, 5)
    c.init_pair(1, c.COLOR_WHITE, c.COLOR_RED)
    window.addstr("This is a window", c.A_BOLD | c.color_pair(1))
    window.refresh()
    c.napms(3000)


c.wrapper(main)
