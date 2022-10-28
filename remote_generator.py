import os 
import cv2
import sys 
import glob 
import json 
import socket 
import serial.tools.list_ports
import requests
import sounddevice as sd
import subprocess
class Machine_data_processing(object):
           
                      
           def get_ip(self): 
                   loc = requests.request('GET', 'https://api.ipify.org')
                   ip = loc.text
                   return ip # Getting the ip data return this will return the public ip of the client machine 
           def get_serial_port(self):   # Getting the serial devices name 
               
               try:
                    devices_data = subprocess.check_output(" python3 -m serial.tools.list_ports -s",shell=True)
                    serial_port = devices_data.decode().split()
                    if '/dev/stlinkv2-1_1' in serial_port:
                           serial_port.remove('/dev/stlinkv2-1_1')
                    ports = serial.tools.list_ports.comports()
                    serial_devices_name = {}
                    for port, desc ,hid in sorted(ports):
                                 print("{}: {} [{}]".format(port, desc, hid))
                                 serial_devices_name[port] = desc                     
                    return serial_devices_name
               except:
                    print("No serial device found ")
                    return "No serial device found"
           def get_local_ip(self):
                     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     s.connect(("8.8.8.8",80))
                     return s.getsockname()[0]  

           def get_audio_device(self):
                    devices = list(sd.query_devices())
                    return devices 
           def get_camera_device(self):
                    index = 0
                    arr = []
                    i = 6
                    for i in range(0,i):
                        cap = cv2.VideoCapture(index)
                        if cap.read()[0]:
                            arr.append(index)
                            cap.release()
                        index += 1
                        i -= 1
                    return {"camera_array":arr}                          
           def get_devicehost(self):
                    return os.listdir("/home/")[0]                          
getdevice_data = Machine_data_processing()
cam_device = getdevice_data.get_camera_device()
audio_device = getdevice_data.get_audio_device()
serial_devices = getdevice_data.get_serial_port()
host_name = getdevice_data.get_devicehost() 
ip = getdevice_data.get_ip() 
localip = getdevice_data.get_local_ip()
data_host = {"serial_devices":serial_devices,"Vision_system":cam_device,"Audio_system":audio_device,"Host_name":host_name,"IP":ip,'Local_ip':localip}
print(data_host)