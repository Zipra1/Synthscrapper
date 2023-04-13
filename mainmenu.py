import subprocess
def drawmenu(): # I know this is a very "simplistic" way of programming this. I wanted that crappy terminal style. So I need a crappy terminal.
    print('##################')
    print('#=SYNTHSCRAPPERS=#\n')

    print('Load Save: L')
    print('New Game: N')
    print('Exit: ESC')
    print('Credits: C')
drawmenu()
userinput = input('Input is CaSe SeNsItIvE!: ') #I promise its just style, I know how to user .lower()

if(userinput == 'L'):
    print('Loading save...')
    subprocess.run(["python", "-c", "print('Hello, world!')"])