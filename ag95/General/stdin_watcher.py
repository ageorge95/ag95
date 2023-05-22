from os import path,\
    remove
from time import sleep
from sys import stdin

def stdin_watcher(trigger_command: str,
                  init_action: callable,
                  trigger_action: callable):
    init_action()

    input_data = ''

    while True:
        sleep(0.5)
        input_data += stdin.read(1).strip()
        input_data = input_data[-10:]
        if input_data.endswith(trigger_command):
            print(f'{trigger_command} command detected')
            trigger_action()
            return

if __name__ == '__main__':
    # create a file called exit if the user types exit in the console, after that return
    stdin_watcher(trigger_command='exit',
                  init_action=(lambda : remove('exit') if path.isfile('exit') else None),
                  trigger_action=(lambda :open('exit', 'w')))

    print('MANUAL assessment required !')