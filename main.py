import uasyncio as asyncio
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
    await run_steps(data)


def set_color(step1_color_arr):
    for n in range(np.n):
        np[n] = (step1_color_arr[0], step1_color_arr[1], step1_color_arr[2])
    np.write()

async def run_steps(data, count=0):
    # Loop through the steps in the data object
    while True:
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
            await asyncio.sleep_ms(step['pause_ms'])
            
            # Do the initial sleep only if this the very first time 
            if count == 0:
                await asyncio.sleep_ms(data['initial_pause_ms'])

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
                await asyncio.sleep_ms(frames_delay)
            count += 1


# toggle the board led on or off
async def toggle_onboard_led(state='on'):
    await asyncio.sleep(3)

    led = machine.Pin(16, machine.Pin.OUT)

    if state == 'on':
        led.off()

    if state == 'off':
        led.on()



@asyncio.coroutine
async def serve(reader, writer):
    print(reader, writer)
    print("================")
    # print((yield from reader.read()))

    res = yield from reader.read()
    res = str(res).replace("b'","")
    res = str(res).replace("'","")
    resArr = res.split(' ')
    method = resArr[0]
    path = resArr[1]
    yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello You. " + method + " " + str(path) + "\r\n")
    print("After response write")
    yield from writer.aclose()
    print("Finished processing request")


loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.create_task(toggle_onboard_led())
loop.create_task(asyncio.start_server(serve, "0.0.0.0", 80))
loop.run_forever()
loop.close()

