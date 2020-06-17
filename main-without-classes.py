import curses as c
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from random import randint
from time import sleep


def main(stdscr):
    win = c.newwin(20, 60, 0, 0)
    win.keypad(True)
    c.curs_set(0)

    win.border(0)
    win.nodelay(True)

    snake = [[4, 10], [4, 9], [4, 8]]
    food = [10, 20]

    win.addch(food[0], food[1], 'O')
    key = KEY_RIGHT
    score = 0
    while key != 27:
        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(score) + ' ')
        win.addstr(0, 27, ' SNAKE ')
        x = 140 - 10*(int((len(snake) / 5 + len(snake) / 10) % 12))
        if x < 50:
            x = 50
        win.addstr(0, 40, 'LEVEL: ' + str(15 - x/10) + ' ')
        win.timeout(x)
        default_key = key
        event = win.getch()
        key = key if event == -1 else event

        if key == ord(' '):
            key = -1
            win.addstr(10, 28, "PAUSED")
            win.refresh()
            while key != ord(' '):
                key = win.getch()
            key = default_key
            win.addstr(10, 28, "      ")
            continue

        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
            key = default_key

        if default_key == KEY_RIGHT and key == KEY_LEFT:
            key = default_key
        if default_key == KEY_LEFT and key == KEY_RIGHT:
            key = default_key
        if default_key == KEY_UP and key == KEY_DOWN:
            key = default_key
        if default_key == KEY_DOWN and key == KEY_UP:
            key = default_key

        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                         snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59:
           break
        """
        if snake[0][0] == 0:
            snake[0][0] = 18

        if snake[0][1] == 0:
            snake[0][1] = 58

        if snake[0][0] == 19:
            snake[0][0] = 1

        if snake[0][1] == 59:
            snake[0][1] = 1
        """
        if snake[0] in snake[1:]:
            break

        if snake[0] == food:
            win.addch(food[0], food[1], 'X')
            food = []
            score += 1
            while food == []:
                food = [randint(1, 18), randint(1, 58)]
                if food in snake:
                    win.addch(food[0], food[1], 'X')
                    score -= 1
                    food = []
            win.addch(food[0], food[1], 'O')
        else:
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
            win.addch(snake[0][0], snake[0][1], 'X')
    win.addstr(8, 20, '     YOU LOSE     ')
    win.addstr(10, 17, '     Final Score : ' + str(score) + '      ')
    win.refresh()
    sleep(3)


c.wrapper(main)
