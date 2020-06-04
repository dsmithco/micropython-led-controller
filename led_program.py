import machine, neopixel, time
import ujson

np = neopixel.NeoPixel(machine.Pin(4), 5)

# toggle the board led on or off
def toggle_onboard_led(state='on'):
    led = machine.Pin(16, machine.Pin.OUT)
    if state == 'on':
        led.off()
    else:
        led.on()

toggle_onboard_led()

def get_data(data_file='data.json'):
    f = open(data_file, "r")
    data = ujson.loads(f.read())
    return data

# Make some colors show up
def startup():
    data = get_data()
    run_steps(data)

def set_color(step1_color_arr):
    for n in range(np.n):
        np[n] = (step1_color_arr[0], step1_color_arr[1], step1_color_arr[2])
    np.write()

def run_steps(data, count=0):
    # Loop through the steps in the data object
    steps = data['steps']
    for i, step in enumerate(steps):

        last = len(steps) == i+1

        if last:
            next_step = steps[0]
        else:
            next_step = steps[i+1]

        # Loop through the colors in the array of rgb colors
        set_color(step['color'])

        # Do the step pause
        time.sleep_ms(step['pause_ms'])
        
        # Do the initial sleep only if this the very first time 
        if count == 0:
            time.sleep_ms(data['initial_pause_ms'])

        from_g = step['color'][0]
        from_r = step['color'][1]
        from_b = step['color'][2]

        to_g = next_step['color'][0]
        to_r = next_step['color'][1]
        to_b = next_step['color'][2]
        
        for r in range(1, 255):
            set_color([from_g + (r * (to_g - from_g)//255), from_r + (r * (to_r - from_r)//255), from_b + (r * (to_b - from_b)//255)])
            time.sleep_ms(step['transition_ms']//255)
        count += 1

    if data['loop_mode'] == 'continuous':
        run_steps(data, count)

startup()


# toggle the board led on or off
def toggle_onboard_led(state='on'):
    led = machine.Pin(16, machine.Pin.OUT)

    if state == 'on':
        led.off()

    if state == 'off':
        led.on()


def get_and_set_offset(increment):
    filename = 'tmp/offset.txt'
    f = open(filename, "w")
    f.write(str(increment))
    return

get_and_set_offset(10)

def demo(np):
    n = np.n

    # cycle
    # for i in range(4 * n):
    #     for j in range(n):
    #         np[j] = (0, 0, 0)
    #     np[i % n] = (255, 255, 255)
    #     np.write()
    #     time.sleep_ms(25)

    # bounce
    # for i in range(4 * n):
    #     for j in range(n):
    #         np[j] = (0, 0, 128)
    #     if (i // n) % 2 == 0:
    #         np[i % n] = (0, 0, 0)
    #     else:
    #         np[n - 1 - (i % n)] = (0, 0, 0)
    #     np.write()
    #     time.sleep_ms(60)

    # fade in/out
    for i in range(0, 8*256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        time.sleep_ms(30)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

# while True:
#     demo(np)