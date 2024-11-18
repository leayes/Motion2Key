from pynput.keyboard import Key, Controller
import asyncio
from bleak import BleakClient, BleakScanner
import struct
import time


pressedUp=False
pressedDown=False
pressedLeft=False
pressedRight=False


def key(x,y,c):
   
   x=x*-1
   
   
   global pressedUp
   global pressedDown
   global pressedLeft
   global pressedRight

   thresh=.4
   if y>thresh and not pressedDown and not pressedUp:
        print("Up")
        # c.press(Key.up)
        pressedUp=True

   if y>thresh and pressedDown:
       
        c.release(Key.down)
        pressedDown=False
        
   if y<-1*thresh and not pressedDown and not pressedUp:
        print("Down")
        # c.press(Key.down)
        pressedDown=True

   if y<-1*thresh and  pressedUp:
       
        c.release(Key.up)
        pressedUp=False
   if x>thresh and not pressedRight and not pressedLeft:
        print("Right")
        # c.press(Key.right)
        pressedRight=True
   if x>thresh and pressedLeft:
       
        # c.release(Key.left)
        pressedLeft=False
        
   if x<-1*thresh and not pressedLeft and not pressedRight:
        print("Left")
        # c.press(Key.left)
        pressedLeft=True

   if x<-1*thresh and  pressedRight:
       
        c.release(Key.right)
        pressedRight=False
    
   

   

   return


# UUIDs for the service and characteristic
SERVICE_UUID = "FFE0"  # Replace with your actual service UUID
CHARACTERISTIC_UUID = "FFE1"  # Replace with your actual characteristic UUID

def decode_gyro_data(data):
    """
    Decode the received gyroscope data from the Bluetooth stream.

    Parameters:
        data (bytes): The received data as bytes.

    Returns:
        tuple: A tuple containing the x and y gyroscope values as floats.
    """
    x, y = struct.unpack('ff', data)
    return x, y

async def notification_handler(sender, data):
    """
    Handle incoming notifications from the Bluetooth device.
    
    Parameters:
        sender (int): The handle of the characteristic that sent the notification.
        data (bytes): The data received from the characteristic.
    """
    x, y = decode_gyro_data(data)

    kb=Controller()
    key(x,y,kb)

    # print(f"Gyroscope X: {x}, Y: {y}")

async def run():
    
    # Scan for BLE devices
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)
    
    # Replace this with the address of your BLE device
    device_address = "03FAD061-EFD9-7704-09AE-8B13CA298A1D"  # Replace with the device's MAC address

    async with BleakClient(device_address) as client:
        # Check if the service is available
        services = await client.get_services()
        print(f"Connected to {device_address}")

        # Start receiving notifications from the characteristic
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Keep the connection open to receive notifications
        print("Listening for gyroscope data...")
        await asyncio.sleep(30000000000000)  # Keep the connection open for 30 seconds

        # # Stop notifications
        await client.stop_notify(CHARACTERISTIC_UUID)

# Run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(run())