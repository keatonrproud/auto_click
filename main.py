import pyautogui as pg
from pynput import mouse, keyboard
import time

class ClickerRunner:
    def __init__(self, coords, single=True, click_delay=1, stop_key='X'):
        self.coords = coords
        self.single = single
        self.click_delay = click_delay
        self.stop_key = stop_key
        self.run = True
        self.listener = keyboard.Listener(on_release=self.on_key_release)

    def run_clicker(self):
        self.listener.start()

        while self.run:
            if self.single:
                x, y = self.coords
                pg.click(x, y)
            else:
                x1, y1, x2, y2, x_dist, y_dist = self.coords
                for x in range(x1, x2, x_dist):
                    for y in range(y1, y2, y_dist):
                        pg.click(x, y)
            time.sleep(self.click_delay)

    def on_key_release(self, key):
        try:
            if key.char == self.stop_key:
                self.run = False
        except AttributeError:
            pass

    def stop(self):
        self.listener.stop()
        self.listener.join()

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

    stop_key = input('Submit the key you want to press to end the clicking: ')
    if stop_key == '':
        print("No stop key was submitted. Your stop key is 'X'.")
        stop_key = 'X'
    elif len(stop_key) > 1: stop_key = stop_key[0]

    single_click = input('Single-click, or click throughout an area on the screen? [Y = single-click, N = area on screen] ')
    single_click = False if single_click == 'N' else True

    coords = set_single_clicker() if single_click else set_area_clicker()

    print('Clicker will begin in 2 seconds.')
    time.sleep(2)

    clicker = ClickerRunner(coords, single=single_click, click_delay=delay, stop_key=stop_key)
    clicker.run_clicker()
    clicker.stop()

if __name__ == '__main__':
    main()
