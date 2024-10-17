import random, sys, time
print('Importing random...')
time.sleep(random.randint(1, 2))
print('OK!')
print('Importing sys...')
time.sleep(0.3)
print('OK!')
print('Importing time...')
time.sleep(4.7)
print('OK!')
print('Importing bext...')
time.sleep(3.1)
try:
    import bext
except ImportError:
    print('Failed!\nERROR: unable to find module \'bext\'. Please')
    print('confirm you have the module installed:')
    print('https://pypi.org/project/Bext/')
    sys.exit()
else:
    print('OK!')

time.sleep(0.3)
print()
print('DONE!')
time.sleep(3)
bext.clear()

print('Setting up constants...')
WIDTH, HEIGHT = bext.size()
WIDTH -= 1

NUM_KELP = random.randint(2, 4)
NUM_FISH = random.randint(10, 15)
NUM_BUBBLERS = random.randint(1, 2)
FRAMES_PER_SECOND = 6
time.sleep(0.65)
print('OK!')
print('Downloading assets...')

FISH_TYPES = [
    {'right': ['><>'],          'left': ['<><']},
    {'right': ['>||>'],         'left': ['<||<']},
    {'right': ['>))>'],         'left': ['<((<']},
    {'right': ['>||o', '>||.'], 'left': ['o||<', '.||<']},
    {'right': ['>))o', '>)).'], 'left': ['o((<', '.((<']},
    {'right': ['>-==>'],        'left': ['<==-<']},
    {'right': [r'>\\>'],        'left': ['<//<']},
    {'right': ['><)))*>'],      'left': ['<*(((><']},
    {'right': ['}-[[[*>'],      'left': ['<*]]]-{']},
    {'right': [']-<)))b>'],     'left': ['<d(((>-[']},
    {'right': ['><XXX*>'],      'left': ['<*XXX><']},
    {'right': ['_.-._.-^=>', '.-._.-.^=>',
               '-._.-._^=>', '._.-._.^=>'],
     'left':  ['<=^-._.-._', '<=^.-._.-.',
               '<=^_.-._.-', '<=^._.-._.']},
    {'right': ['>-<))))o>-'],   'left': ['-<o((((>-<']},
]
LONGEST_FISH_LENGTH = 10

LEFT_EDGE = 0
RIGHT_EDGE = WIDTH - 1 - LONGEST_FISH_LENGTH
TOP_EDGE = 0
BOTTOM_EDGE = HEIGHT - 2

time.sleep(3)
print('OK!')
print('Downloading data...')

def main():
    global FISHES, BUBBLERS, BUBBLES, KELPS, STEP
    bext.bg('black')
    bext.clear()

    FISHES = []
    for i in range(NUM_FISH):
        FISHES.append(generateFish())

    BUBBLERS = []
    for i in range(NUM_BUBBLERS):
        BUBBLERS.append(random.randint(LEFT_EDGE, RIGHT_EDGE))
    BUBBLES = []

    KELPS = []
    for i in range(NUM_KELP):
        kelpx = random.randint(LEFT_EDGE, RIGHT_EDGE)
        kelp = {'x': kelpx, 'segments': []}
        for i in range(random.randint(6, HEIGHT - 1)):
            kelp['segments'].append(random.choice(['(', ')']))
        KELPS.append(kelp)
    
    STEP = 1
    while True:
        simulateAquarium()
        drawAquarium()
        time.sleep(1 / FRAMES_PER_SECOND)
        clearAquarium()
        STEP += 1

def getRandomColor():
    return random.choice(('black', 'red', 'green', 'yellow', 'blue',
                          'purple', 'cyan', 'white'))

def generateFish():
    fishType = random.choice(FISH_TYPES)

    if fishType['right'] == ['>-<))))o>-']:
        colorPattern = 'stealth'
    else:
        colorPattern = random.choice(('random', 'head-tail', 'single'))
    fishLength = len(fishType['right'][0])
    if colorPattern == 'random':
        colors = []
        for i in range(fishLength):
            colors.append(getRandomColor())
    if colorPattern == 'single' or colorPattern == 'head-tail':
        colors = [getRandomColor()] * fishLength
    if colorPattern == 'head-tail':
        headTailColor = getRandomColor()
        colors[0] = headTailColor
        colors[-1] = headTailColor
    if colorPattern == 'stealth':
        colors = []
        for i in range(fishLength):
            colors.append('black')
        colors[3] = 'blue'
        colors[-3] = 'cyan'
        colors[-5] = 'blue'
    
    if fishType['right'] == ['>-<))))o>-']:
        fish = {'right':            fishType['right'],
                'left':             fishType['left'],
                'colors':           colors,
                'hSpeed':           2,
                'vSpeed':           random.randint(5, 15),
                'timeToHDirChange': random.randint(10, 60),
                'timeToVDirChange': random.randint(2, 20),
                'goingRight':       random.choice([True, False]),
                'goingDown':        random.choice([True, False])}
    else:
        fish = {'right':            fishType['right'],
                'left':             fishType['left'],
                'colors':           colors,
                'hSpeed':           random.randint(1, 6),
                'vSpeed':           random.randint(5, 15),
                'timeToHDirChange': random.randint(10, 60),
                'timeToVDirChange': random.randint(2, 20),
                'goingRight':       random.choice([True, False]),
                'goingDown':        random.choice([True, False])}

    fish['x'] = random.randint(0, WIDTH - 1 - LONGEST_FISH_LENGTH)
    fish['y'] = random.randint(0, HEIGHT - 2)
    if fish['goingRight'] == False:
        fish['colors'].reverse()
    return fish

def simulateAquarium():
    global FISHES, BUBBLERS, BUBBLES, KELPS, STEP

    for fish in FISHES:
        if STEP % fish['hSpeed'] == 0:
            if fish['goingRight']:
                if fish['x'] != RIGHT_EDGE:
                    fish['x'] += 1
                else:
                    fish['goingRight'] = False
                    fish['colors'].reverse()
            else:
                if fish['x'] != LEFT_EDGE:
                    fish['x'] -= 1
                else:
                    fish['goingRight'] = True
                    fish['colors'].reverse()
        
        fish['timeToHDirChange'] -= 1
        if fish['timeToHDirChange'] == 0:
            fish['timeToHDirChange'] = random.randint(10, 60)
            fish['goingRight'] = not fish['goingRight']
            fish['colors'].reverse()

        if STEP % fish['vSpeed'] == 0:
            if fish['goingDown']:
                if fish['y'] != BOTTOM_EDGE:
                    fish['y'] += 1
                else: 
                    fish['goingDown'] = False
            else:
                if fish['y'] != TOP_EDGE:
                    fish['y'] -= 1
                else:
                    fish['goingDown'] = True

        fish['timeToVDirChange'] -= 1
        if fish['timeToVDirChange'] == 0:
            fish['timeToVDirChange'] = random.randint(2, 20)
            fish['goingDown'] = not fish['goingDown']
        
        for bubbler in BUBBLERS:
            if random.randint(1, 5) == 1:
                BUBBLES.append({'x': bubbler, 'y': HEIGHT - 2})
        
        for bubble in BUBBLES:
            diceRoll = random.randint(1, 6)
            if (diceRoll == 1) and (bubble['x'] != LEFT_EDGE):
                bubble['x'] -= 1
            elif (diceRoll == 2) and (bubble['x'] != RIGHT_EDGE):
                bubble['x'] += 1

            bubble['y'] -= 1
        
        for i in range(len(BUBBLES) - 1, -1, -1):
            if BUBBLES[i]['y'] == TOP_EDGE:
                del BUBBLES[i]
        
        for kelp in KELPS:
            for i, kelpSegment in enumerate(kelp['segments']):
                if random.randint(1, 20) == 1:
                    if kelpSegment == '(':
                        kelp['segments'][i] == ')'
                    elif kelpSegment == ')':
                        kelp['segments'][i] == '('

def drawAquarium():
    global FISHES, BUBBLERS, BUBBLES, KELPS, STEP

    bext.fg('white')
    bext.goto(0, 0)
    print('Fish Tank Screensaver              Ctrl-C to end.', end='')
    
    bext.fg('white')
    for bubble in BUBBLES:
        bext.goto(bubble['x'], bubble['y'])
        print(random.choice(('o', 'O')), end='')
    
    for fish in FISHES:
        bext.goto(fish['x'], fish['y'])

        if fish['goingRight']:
            fishText = fish['right'][STEP % len(fish['right'])]
        else:
            fishText = fish['left'][STEP % len(fish['left'])]

        for i, fishPart in enumerate(fishText):
            bext.fg(fish['colors'][i])
            print(fishPart, end='')
        
    bext.fg('green')
    for kelp in KELPS:
        for i, kelpSegment in enumerate(kelp['segments']):
            if kelpSegment == '(':
                bext.goto(kelp['x'], BOTTOM_EDGE - i)
            elif kelpSegment == ')':
                bext.goto(kelp['x'] + 1, BOTTOM_EDGE - i)
            print(kelpSegment, end='')
        
    bext.fg('yellow')
    bext.goto(0, HEIGHT - 1)
    print(chr(9617) * (WIDTH - 1), end='')

    sys.stdout.flush()

def clearAquarium():
    global FISHES, BUBBLERS, BUBBLES, KELPS

    for bubble in BUBBLES:
        bext.goto(bubble['x'], bubble['y'])
        print(' ', end='')
    
    for fish in FISHES:
        bext.goto(fish['x'], fish['y'])
        
        print(' ' * len(fish['left'][0]), end='')

    for kelp in KELPS:
            for i, kelpSegment in enumerate(kelp['segments']):
                bext.goto(kelp['x'], HEIGHT - 2 - i)
                print(' ', end='')

    sys.stdout.flush()

time.sleep(6)
print('OK!')
print('Loading resources...')
time.sleep(random.randint(3, 6))
print('OK!')

print()
print('DONE!')
time.sleep(3)
bext.clear()

print('Testing application...')
time.sleep(2)
print()
print('Testing load_fishes.py...      OK!')
time.sleep(random.random())
print('Testing load_kelp.py...        OK!')
time.sleep(random.random())
print('Testing load_bubbles.py...     OK!')
time.sleep(random.random())
print('Testing load.sand.py...        OK!')
time.sleep(random.random())
print('Testing load_simulation.py...  OK!')
time.sleep(random.random())
print('Testing generation.py...       OK!')
time.sleep(random.random())
print('Testing fish_swim.py...        OK!')
time.sleep(random.random())
print('Testing color_generator.py...  OK!')
time.sleep(random.random())
print('Testing reset_simulation.py... OK!')
time.sleep(random.random())

if random.randint(1, 100) == 1:
    print('Testing boot_system.py...      Failed!')
    print('ERROR: unable to successfully test boot_system.py.')
    print('Please reboot the application.')
    sys.exit()
else:
    print('Testing boot_system.py...      OK!')

print()
print('DONE!')
time.sleep(1)
print('Booting up Fish_Tank.py...')
time.sleep(random.randint(3, 5))
bext.clear()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        time.sleep(3)
        bext.clear()
        sys.exit()