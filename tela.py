
from time import sleep
import socket
import whatismyip
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import psutil
# Define valores da telinha LCD
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D21)
lcd_en = digitalio.DigitalInOut(board.D26)
lcd_d4 = digitalio.DigitalInOut(board.D19)
lcd_d5 = digitalio.DigitalInOut(board.D13)
lcd_d6 = digitalio.DigitalInOut(board.D6)
lcd_d7 = digitalio.DigitalInOut(board.D5)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)


# # find an active IP on the first LIVE network device
# def parse_ip():
#     find_ip = "ip addr show %s" % interface
#     find_ip = "ip addr show %s" % interface
#     ip_parse = run_cmd(find_ip)
#     for line in ip_parse.splitlines():
#         if "inet " in line:
#             ip = line.split(' ')[5]
#             ip = ip.split('/')[0]
#     return ip
# https://stackoverflow.com/a/28950776
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# wipe LCD screen before we start
lcd.clear()

# before we start the main loop - detect active network device and ip address
# sleep(2)
# interface = find_interface()
ip_local = getIP()
ip_modem = whatismyip.whatismyip()

while True:
    lcd.clear()
    sleep(0.1)
    lcd.message = "    IP local " + "\n  " + ip_local
    sleep(10)
    lcd.clear()
    sleep(0.1)
    # date and time
    # lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    lcd.message = "   IP externo " + "\n " + ip_modem
    sleep(9)

    # Uso de CPU/Memória  
    cpu_usage = str(psutil.cpu_percent(1))
    cpu_spped = str(int(psutil.cpu_freq().current))

    lcd.clear()
    sleep(0.1)

    if (float(psutil.virtual_memory().used/10**9) < 1.0):
        mem_usage = str(round(psutil.virtual_memory().used/10**6)) + "MB"
    else:
        mem_usage = "%0.2f" % float(psutil.virtual_memory().used/10**9) + "GB"
        
    mem_total = "%0.2f" % float(psutil.virtual_memory().total/10**9) + "GB"
    lcd.message = "CPU: " + cpu_usage + "% \nMem:" + mem_usage + "/" + mem_total
    sleep(10)
