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

#### Update Firmware
esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20191220-v1.12.bin

#### Connect
screen /dev/cu.SLAB_USBtoUART 115200

#### Connect to folder
rshell -p /dev/cu.SLAB_USBtoUART

#### Copy to board
cp ./main.py /pyboard/
