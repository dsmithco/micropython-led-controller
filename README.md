# micropython-led-controller

### Documents
https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html

    ### Local Setup
    pip install esptool
    python3 -m pip install --user virtualenv
    python3 -m venv env
    source env/bin/activate

    ### Setup NodeMCU Board
    Download firmware http://micropython.org/download/esp8266/

    #### Plugin NodeMCU

    #### Get USB location
    ls /dev/cu.*

    #### Flash
    esptool.py --port /dev/cu.SLAB_USBtoUART erase_flash

    # OR

    esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART erase_flash


    #### Update Firmware
    esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20200911-v1.13.bin
    esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-512k-20200902-v1.13.bin

    esp8266-20190529-v1.11.bin
    esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20200421-v1.12-388-g388d419ba.bin

    # OR 

    esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash -z 0x1000 /Users/dsmith36/Downloads/esp32-idf4-20191220-v1.12.bin

    #### Connect
    screen /dev/cu.SLAB_USBtoUART 115200

    #### Connect to folder 
    rshell -p /dev/cu.SLAB_USBtoUART
    connect serial /dev/cu.SLAB_USBtoUART
    
    #### Download Tinyweb and put in /pyboard/tinyweb
    #### Download to project ./tinyweb https://github.com/belyalov/tinyweb/blob/master/tinyweb

#### Copy to board
cp ./main.py /pyboard/
cp ./data.json /pyboard/
cp ./boot.py /pyboard/
cp ./min.css /pyboard/
cp ./index.html /pyboard/

    #### View logs
    repl
    
## WiFi

- The ESSID is of the form MicroPython-xxxxxx where the x’s are replaced with part of the MAC address of your device (so will be the same everytime, and most likely different for all ESP8266 chips). 
- The password for the WiFi is micropythoN (note the upper-case N).
- Its IP address will be 192.168.4.1 once you connect to its network. WiFi configuration will be discussed in more detail later in the tutorial.
