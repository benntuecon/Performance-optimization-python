import psutil
import time

while True:
    print(f'CPU usage: {psutil.cpu_percent(interval=1.0)}%')
    time.sleep(5)  # delay for 5 seconds
