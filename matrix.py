#!/usr/bin/python
# -*- coding: utf8 -*-

import curses
import random

class RainingString():
    """ Defines a raining string that will be adding
    characters through the window vertically, from
    top to bottom.
    """
    characters = []
    changed = False
    char_health = 100
    health = 100
    window = None
    x = 0
    y = 0

    def __init__(self, window, health=100, x=0):
        self.changed = True
        self.char_health = random.randrange(10, 1000)
        self.health = health
        self.window = window
        self.x = x

    def update(self):
        if self.health > 0:
            self.health -= 1
            self.y += 1
            self.characters.append(Character(
                self.window,
                self.y,
                self.x,
                health=self.char_health
            ))
            self.changed = True

        for i, char in enumerate(self.characters):
            char.update()
            if char.health <= 0:
                char.die()
                del self.characters[i]
                del char


    def refresh(self):
        if self.changed:
            self.changed = False
            self.update()
            [character.render() for character in self.characters]


class Character():
    """ This is what we see on screen, with its life and
    the render. Once it dies, it cleans itself the character
    from the window.
    """
    changed = False
    character = None
    health = 0
    is_new = True
    loop = 0
    max_i = 5
    window = None
    x = 0
    y = 0

    def __init__(self, window, y, x, health=100):
        self.changed = True
        self.character = chr(random.randrange(90, 100))
        self.health = health
        self.window = window
        self.x = x
        self.y = y

    def update(self):
        if self.loop < self.max_i + 5:
            self.loop += 1

        if self.loop > self.max_i and self.is_new:
            self.changed = True
            self.is_new = False

        if self.health < 10:
            self.changed = True

        if self.health > 0:
            self.health -= 1

    def render(self):
        if self.changed and self.loop < self.max_i * 3:
            self.changed = False

            try:
                color = 1
                if self.is_new:
                    color = 2

                color_pair = curses.color_pair(color)

                self.window.move(self.y, self.x)
                self.window.addstr(self.character, color_pair)

            except:
                pass

    def die(self):
        self.health = 0
        try:
            self.window.move(self.y, self.x)
            self.window.addstr(" ")
        except:
            pass


def main(screen):
    # Config
    max_strings = 6
    probability = 75
    sleep_ms = 30

    # Disable the cursor displaying
    curses.curs_set(0)

    # White color for new characters and
    # green for anything else
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Prepares the window and define
    # its limits, so we can place the
    # strings safely
    window = curses.newwin(curses.LINES - 1, curses.COLS - 1)
    window_size = window.getmaxyx()
    max_x = window_size[1] - 1
    max_y = window_size[0] - 1

    # Here we go!
    strings = []
    while True:
        x = random.randrange(0, max_x)
        random_number = random.randrange(0, 100)

        # Generates a new string if we didn't
        # reach yet the limit and the random
        # number is higher than probability
        if len(strings) < max_strings and random_number > probability:
            new_string = RainingString(window, health=max_y, x=x)
            strings.append(new_string)

        # When strings die, we remove any
        # reference so the garbage collector
        # can clean them.
        for idx, string in enumerate(strings):
            if string.health is 0:
                del strings[idx]
                del string

        # Finally, we update every string
        # and the screen
        [string.refresh() for string in strings]
        curses.napms(sleep_ms)
        window.refresh()


if __name__ == '__main__':
    main(curses.wrapper(main))

