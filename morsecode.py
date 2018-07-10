from microbit import *
import music
import radio

# morse code table
MORSE_CODE_LOOKUP = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}


# get charater by morse code
def decode(buffer):
    return MORSE_CODE_LOOKUP.get(buffer, '.')

# show start message
def show_start_msg():
    # Count down for start sending morse codes.
    COUNT_DOWN = ['3', '2', '1', Image.HAPPY]
    START_HINT = 'PRESS BUTTON A TO START'

    # show start hint and waiting to start signal
    display.scroll(START_HINT, wait=False, loop=True)
    while True:
        if button_a.was_pressed():
            # count down for start sending morse code
            display.show(COUNT_DOWN, delay=1000)
            # beep for start
            music.pitch(880, 300)
            break


# dot image
DOT = Image("00000:"
            "00000:"
            "00900:"
            "00000:"
            "00000:")


# dash image
DASH = Image("00000:"
             "00000:"
             "09990:"
             "00000:"
             "00000:")
             
# no message income
NO_MSG = Image("00000:"
               "00000:"
               "00000:"
               "00000:"
               "00000:")

# new message income
NEW_MSG = Image("00009:"
                "00000:"
                "00000:"
                "00000:"
                "00000:")

INCM  =  NO_MSG

# less than 250ms is a dot
DOT_THRESHOLD = 250
# 250ms to 500ms is a dash, great than 500 is a gap
DASH_THRESHOLD = 500

# Morse signals
buffer = ''
# Morse charater
message = ''

started_to_wait = running_time()

# receive message
recv_msg = []

# init radio
radio.config(group=1)
radio.on()

# show starting message
show_start_msg()

while True:
    # waiting for a keypress time
    waiting = running_time() - started_to_wait
    key_down_time = None

    # reading morse code input
    while pin2.read_digital():
        music.pitch(360, 1)
        if not key_down_time:
            key_down_time = running_time()

    # this is a morse code, dot or dash
    if key_down_time:
        key_up_time = running_time()
        duration = key_up_time - key_down_time
        if duration < DOT_THRESHOLD:
            buffer += '.'
            display.show(DOT + INCM)
        elif duration < DASH_THRESHOLD:
            buffer += '-'
            display.show(DASH + INCM)
        else:
            # keydown duration great than 500ms will be ignored
            pass
        started_to_wait = running_time()
    # this is a gap between charater
    elif len(buffer) > 0 and waiting > DASH_THRESHOLD:
        character = decode(buffer)
        buffer = ''
        display.show(character)
        message += character

    # receiving message
    while True:
        incomming = radio.receive()
        if incomming is None:
            break

        recv_msg.append(incomming)
        print('incoming message:', incomming)
        INCM  = NEW_MSG
        display.show(INCM)
        
    # if button b is pressed, show the message
    if button_b.was_pressed():
        radio.send(message)
        display.scroll(message)
        message = ''
    
    if button_a.was_pressed():
        for msg in recv_msg:
            display.scroll(msg) 
        recv_msg = []
        INCM  =  NO_MSG
        
        
