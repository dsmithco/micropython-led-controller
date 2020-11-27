# This file is executed on every boot (including wake-boot from deepsleep)
try:
    import usocket as socket
except:
    import socket
import esp, network
esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import ujson

#import webrepl
#webrepl.start()
gc.collect()

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ReThinkLED', password='Rethink44')
