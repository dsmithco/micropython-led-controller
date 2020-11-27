import uasyncio as asyncio
import machine, neopixel, time
import ujson


def get_data(data_file='data.json'):
    f = open(data_file, "r")
    data = ujson.loads(f.read())
    f.close()
    return data

data = get_data()
np = neopixel.NeoPixel(machine.Pin(0), data['led_length'])

# Make some colors show up
async def startup():
    await run_steps(data)


def set_color(step1_color_arr):
    for n in range(np.n):
        np[n] = (int(step1_color_arr[0]), int(step1_color_arr[1]), int(step1_color_arr[2]))
    np.write()

async def run_steps(data, count=0):
    # Set initial color to black 
    set_color([0,0,0])

    # Loop through the steps in the data object
    while True:
        data = get_data()
        steps = data['steps']
        for i, step in enumerate(steps):

            this_colors = []
            try:
                color = step['color'].replace('#','')
                this_colors.append(eval('0x'+color[0:-5]+color[1:-4]))
                this_colors.append(eval('0x'+color[2:-3]+color[3:-2]))
                this_colors.append(eval('0x'+color[4:-1]+color[5:]))
            except:
                this_colors = [40,40,40]

            last = len(steps) == i+1

            if last:
                next_step = steps[0]
            else:
                next_step = steps[i+1]

            color = next_step['color'].replace('#','')
            next_colors = []
            try:
                next_colors.append(eval('0x'+color[0:-5]+color[1:-4]))
                next_colors.append(eval('0x'+color[2:-3]+color[3:-2]))
                next_colors.append(eval('0x'+color[4:-1]+color[5:]))
            except:
                next_colors = [90,90,90]



            # Loop through the colors in the array of rgb colors
            set_color(this_colors)

            # Do the step pause
            await asyncio.sleep_ms(step['pause_ms'])
            
            # Do the initial sleep only if this the very first time 
            if count == 0:
                await asyncio.sleep_ms(data['initial_pause_ms'])

            from_g = int(this_colors[0])
            from_r = int(this_colors[1])
            from_b = int(this_colors[2])

            to_g = int(next_colors[0])
            to_r = int(next_colors[1])
            to_b = int(next_colors[2])
            
            frames = 255
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



# @asyncio.coroutine
async def serve(reader, writer):
    while True:
        r = await reader.read(2048)
        res = r.decode('latin-1')

        if 'POST /' in res:
            error = False
            data = res.split('\n')[-1]

            try:
                res_json = ujson.loads(data)
                if 'steps' not in res_json:
                    error = True
            except Exception as e:
                print(data)
                print(e)
                error = True
                res_json = ujson.dumps({})
                continue

            if error == False and res_json and 'steps' in res_json:
                f = open('data.json', "w")
                f.write(ujson.dumps(res_json))
                f.close()

            await writer.awrite("HTTP/1.0 201 OK\r\n\r\n" + ujson.dumps(res_json) + "\r\n")
            await writer.aclose()
            if error == False:
                # machine.softreset()
                break
            return

        if 'GET /data.json ' in res:
            f = open('data.json', "r")
            content = f.read()
            f.close()
            await writer.awrite("HTTP/1.0 200 OK\r\n\r\n" + content + "\r\n")
            await writer.aclose()
            return

        if 'GET /min.css ' in res:
            f = open('min.css', "r")
            content = f.read()
            f.close()
            await writer.awrite("HTTP/1.0 200 OK\r\n\r\n" + content + "\r\n")
            await writer.aclose()
            return

        if 'GET /main.js ' in res:
            f = open('main.js', "r")
            content = f.read()
            f.close()
            await writer.awrite("HTTP/1.0 200 OK\r\n\r\n" + content + "\r\n")
            await writer.aclose()
            return

        if 'GET / ' in res:
            f = open('index.html', "r")
            content = f.read()
            f.close()
            await writer.awrite("HTTP/1.0 200 OK\r\n\r\n" + content + "\r\n")
            await writer.aclose()
            return


loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.create_task(toggle_onboard_led())
loop.create_task(asyncio.start_server(serve, "0.0.0.0", 80))
loop.run_forever()
loop.close()

