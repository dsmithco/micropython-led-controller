# This file is executed on every boot (including wake-boot from deepsleep)
import esp, network
esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ReThinkLED', password='Rethink44')