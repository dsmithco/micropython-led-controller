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
gc.collect()
# gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ReThinkLED', password='Rethink44')
