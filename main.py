import pyautogui as pg
from pynput import mouse
import time


def run_clicker(coords, single=True, click_delay=None):
    if click_delay is None: click_delay = 5
    while True:
        if single:
            x, y = coords
            pg.click(x, y)
        else:
            x1, y1, x2, y2, x_dist, y_dist = coords
            for x in range(x1, x2, x_dist):
                for y in range(y1, y2, y_dist):
                    pg.click(x, y)
        time.sleep(click_delay)


def on_click(x, y, _, pressed):
    if pressed:
        on_click.coords = (x, y)
        return False


def set_on_click():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def set_single_clicker():
    print(f'Click where you want the clicking to occur.')
    set_on_click()
    x, y = on_click.coords
    print(f'Clicking at coords ({x}, {y})')
    return x, y


def set_area_clicker():
    print('Click your mouse in the top-left corner of the area to be clicked.')
    set_on_click()
    x1, y1 = on_click.coords
    print(f'Top-left: {x1, y1}')

    print('Click your mouse in the bottom-right corner of the area to be clicked.')
    set_on_click()
    x2, y2 = on_click.coords
    print(f'Btm-right: {x2, y2}')

    x_dist = int(input('Input the distance between x-coordinates for each click (int): '))
    y_dist = int(input('Input the distance between y-coordinates for each click (int): '))

    return x1, y1, x2, y2, x_dist, y_dist


def main():
    try:
        delay = int(input('Number of seconds between click times (int): '))
    except ValueError:
        print('The last submission was not an integer. The default delay of 1 second will be used.')
        delay = 1

    single_click = input('Single-click, or click throughout an area on the screen? [Y = single-click, N = in area on screen] ')
    single_click = False if single_click == 'N' else True

    coords = set_single_clicker() if single_click else set_area_clicker()

    print('Clicker will begin in 2 seconds.')
    time.sleep(2)
    run_clicker(coords, single=single_click, click_delay=delay)


if __name__ == '__main__':
    main()