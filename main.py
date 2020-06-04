import uasyncio
import machine, neopixel, time
import ujson

def get_data(data_file='data.json'):
    f = open(data_file, "r")
    data = ujson.loads(f.read())
    return data

data = get_data()
np = neopixel.NeoPixel(machine.Pin(4), data['led_length'])

# toggle the board led on or off
async def toggle_onboard_led(state='on'):
    led = machine.Pin(16, machine.Pin.OUT)
    if state == 'on':
        led.off()
    else:
        led.on()

# Make some colors show up
def startup():
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
        
        trans_fade_ms = step['transition_ms']//64
        for r in range(1, trans_fade_ms):
            set_color([from_g + (r * (to_g - from_g)//trans_fade_ms), from_r + (r * (to_r - from_r)//trans_fade_ms), from_b + (r * (to_b - from_b)//trans_fade_ms)])
            time.sleep_ms(trans_fade_ms)
        count += 1

    if data['loop_mode'] == 'continuous':
        run_steps(data, count)


# toggle the board led on or off
def toggle_onboard_led(state='on'):
    led = machine.Pin(16, machine.Pin.OUT)

    if state == 'on':
        led.off()

    if state == 'off':
        led.on()


loop = uasyncio.get_event_loop()
loop.create_task(toggle_onboard_led()) # Schedule ASAP
loop.create_task(startup()) # Schedule ASAP
loop.run_forever()

# startup()

# uasyncio.run(toggle_onboard_led())

