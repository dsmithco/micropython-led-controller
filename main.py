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





# @asyncio.coroutine
# def serve(reader, writer):
#     print(reader, writer)
#     print("================")
#     print((yield from reader.read()))
#     yield from writer.awrite("HTTP/1.0 200 OK\r\n\r\nHello You. " + str(reader) + "\r\n")
#     print("After response write")
#     yield from writer.aclose()
#     print("Finished processing request")



def start_web():
    import tinyweb

    # Create web server application
    app = tinyweb.webserver()

    # Index page
    @app.route('/')
    async def index(request, response):
        # Start HTTP response with content-type text/html
        await response.start_html()
        # Send actual HTML page
        await response.send('<html><body><h1>Hello, world! (<a href="/table">table</a>)</h1></html>\n')

    # Another one, more complicated page
    @app.route('/table')
    async def table(request, response):
        # Start HTTP response with content-type text/html
        await response.start_html()
        await response.send('<html><body><h1>Simple table</h1>'
                            '<table border=1 width=400>'
                            '<tr><td>Name</td><td>Some Value</td></tr>')
        for i in range(10):
            await response.send('<tr><td>Name{}</td><td>Value{}</td></tr>'.format(i, i))
        await response.send('</table>'
                            '</html>')


    app.run(host='0.0.0.0', port=8081)






loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.create_task(toggle_onboard_led())
loop.create_task(start_web())
# loop.call_soon(asyncio.start_server(serve, "0.0.0.0", 80))
loop.run_forever()
loop.close()

