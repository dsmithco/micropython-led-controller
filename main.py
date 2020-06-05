import uasyncio
import machine, neopixel, time
import ujson


def get_data(data_file='data.json'):
    f = open(data_file, "r")
    data = ujson.loads(f.read())
    return data

data = get_data()
np = neopixel.NeoPixel(machine.Pin(4), data['led_length'])

# Make some colors show up
async def startup():
    keep_going = 1
    while keep_going:
        keep_going = run_steps(data)

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
        
        frames = 30
        frames_delay = int(step['transition_ms']//frames) or 1
        for r in range(1, frames):
            set_color([from_g + (r * (to_g - from_g)//frames), from_r + (r * (to_r - from_r)//frames), from_b + (r * (to_b - from_b)//frames)])
            time.sleep_ms(frames_delay)
        count += 1

    if data['loop_mode'] == 'continuous':
        return 1


# toggle the board led on or off
async def toggle_onboard_led(state='on'):
    led = machine.Pin(16, machine.Pin.OUT)

    if state == 'on':
        led.off()

    if state == 'off':
        led.on()


loop = uasyncio.get_event_loop()
loop.create_task(startup())
loop.create_task(toggle_onboard_led())

loop.run_forever()


try:
    import usocket as socket
except:
    import socket

led = machine.Pin(2, machine.Pin.OUT)

def web_page():
    if led.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"
    
    file = open("index.html", "r")
    html = file.read()
    file.close
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print('TESTING!')
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    if led_on == 6:
        print('LED ON')
        led.value(1)
    if led_off == 6:
        print('LED OFF')
        led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()