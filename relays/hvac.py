import time as t
import smbus
import sys

DEVICE_BUS = 1
DEVICE_ADDR = 0x10
bus = smbus.SMBus(DEVICE_BUS)

FAN = 1
COLD = 2
HEAT = 3
EM_HEAT = 4

def test_relays():
    for i in range(1,5):
        bus.write_byte_data(DEVICE_ADDR, i, 0xFF)
        t.sleep(1)
        bus.write_byte_data(DEVICE_ADDR, i, 0x00)
        t.sleep(1)
    return

def turn_on(relay: int):
    bus.write_byte_data(DEVICE_ADDR, relay, 0xFF)
    return

def turn_off(relay: int):
    bus.write_byte_data(DEVICE_ADDR, relay, 0x00)
    return

def switch_relay(status: int, relay: int):
    if status == 1:
        turn_on(relay)
    elif status == 0:
        turn_off(relay)
    else:
        return

def switch_relays(status: int, relays: list):
    for i in relays:
        switch_relay(status, i)

def set_relay_nums(temp_goal):
    global FAN
    global COLD
    global HEAT 
    global EM_HEAT 
    relay_num: int
    relay_nums: list = [FAN]

    # Check if fan is on already before adding to list

    if temp_goal == "COOL":
        relay_num = COLD
    elif temp_goal == "HEAT":
        relay_num = HEAT

    relay_nums.append(relay_num)
    
    return relay_nums

# while True:
#     try:
# for i in range(1,5):
#     bus.write_byte_data(DEVICE_ADDR, i, 0xFF)
#     t.sleep(1)
#     bus.write_byte_data(DEVICE_ADDR, i, 0x00)
#     t.sleep(1)
    # except KeyboardInterrupt as e:
    #     print("Quit the Loop")
    #     sys.exit()