import socket
from sys import platform as pf
import cpuinfo
import psutil
import time
import datetime
from datetime import timedelta
class GetData:
    def get_platform(self):
        return pf
    
    def get_arch(self):
        return cpuinfo.get_cpu_info()["arch"]

    def get_cpu(self):
        return cpuinfo.get_cpu_info()['brand_raw']

    def get_hostname(self):
        return socket.gethostname()
    
    def get_cpu_cores(self):
        return psutil.cpu_count()

class GetIndicators:

    # CPU

    def get_cpu_freq(self):
        freq = psutil.cpu_freq()
        return f"{round(freq[0])}/{round(freq[2])}"

    def get_cpu_load(self):
        load = psutil.cpu_percent(interval=0.1)
        return load

    # RAM

    def get_ram_percent(self):
        return psutil.virtual_memory()[2]

    def get_ram_total(self):
        mem = round(psutil.virtual_memory()[0] / 1024 /1024)
        return mem
    
    def get_ram_available(self):
        return round(psutil.virtual_memory()[1] / 1024 / 1024)

    def get_ram_used(self):
        return round(psutil.virtual_memory()[3] / 1024 / 1024)

    # SWAP

    def get_swap_total(self):
        try:
            swap = psutil.swap_memory()
            return round(swap[0] / 1024 / 1024)
        except:
            return 0

    def get_swap_used(self):
        try:
            swap = psutil.swap_memory()
            return round(swap[1] / 1024 / 1024)
        except:
            return 0
    
    def get_swap_percent(self):
        try:
            swap = psutil.swap_memory()
            return swap[3]
        except:
            return 0

    # DISK USAGE

    def get_disks_usage(self):
        use = psutil.disk_usage('/')
        total = use[0] / 1024 // 1024
        used = use[1] / 1024 // 1024
        return [round(total), round(used)]

def get_network():
    net_io = psutil.net_io_counters()
    disk_io_before = psutil.disk_io_counters()
   
    time.sleep(1)
   
    disk_io_after = psutil.disk_io_counters()
    read_speed = (disk_io_after.read_bytes - disk_io_before.read_bytes) / (1024 * 1024)  # в МБ/с
    write_speed = (disk_io_after.write_bytes - disk_io_before.write_bytes) / (1024 * 1024)  # в МБ/с
   
    net_io_new = psutil.net_io_counters()
    bytes_recv = round((net_io_new.bytes_recv - net_io.bytes_recv) / 1024)
    bytes_sent = round((net_io_new.bytes_sent - net_io.bytes_sent) /1024)

    return [bytes_recv, bytes_sent, read_speed, write_speed]


def dict_data():
    data = GetData()
    dictdat = {
        'platform': data.get_platform(),
        'arch': data.get_arch(),
        'cpu': data.get_cpu(),
        'hostname': data.get_hostname(),
        'cpu_cores': data.get_cpu_cores()
    }
    return dictdat



def dict_indi():
    uptime = psutil.boot_time()
    current_time = time.time()
    uptime_seconds = current_time - uptime
    uptime_str = str(timedelta(seconds=uptime_seconds))
    indi = GetIndicators()
    dictindi = {
        # CPU
        #'cpu_freq': indi.get_cpu_freq(),
        'cpu_load': indi.get_cpu_load(),
        # RAM
        'ram_percent': indi.get_ram_percent(),
        'ram_total': indi.get_ram_total(),
        'ram_available': indi.get_ram_available(),
        'ram_used': indi.get_ram_used(),
        # SWAP
        'swap_total': indi.get_swap_total(),
        'swap_used': indi.get_swap_used(),
        'swap_percent': indi.get_swap_percent(),
        '/': indi.get_disks_usage(),
        'uptime': uptime_str
    }
    return dictindi
