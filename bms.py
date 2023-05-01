import struct
import serial

ser = serial.Serial('COM7', 2500000, timeout=None)
print(ser.write(b'V\r'))
print(ser.read_until(b'\r'))
print('CANDAPTER VERSION PRINTED')

print(ser.write(b'S5\r'))    # CAN Baudrate set to 500k
print(ser.write(b'O\r'))     # Open CANdapter
print('CANDAPTER OPENED')

def decode(m_id, m_bytes):
    if int(m_id) == 101:
        temp_avg, temp_low, null = struct.unpack('<HHb',m_bytes[:5])
        high_cell_v, = struct.unpack('>H',m_bytes[-2:])
        #print('Avg temp: {:.1f} C\t Low temp: {:.1f} C\t Highest Voltage: {:.2f} V'.format(temp_avg,temp_low,high_cell_v*0.0001))
        return (temp_avg,temp_low,high_cell_v)
    elif int(m_id) == 100:
        pack_current, null, null, temp_high = struct.unpack('>Hbbb',m_bytes[:5])
        pack_voltage, = struct.unpack('<H',m_bytes[2:4])
        dtc_flags, = struct.unpack('<H',m_bytes[-2:])
        #print('Pack current: {:.2f} A\t Pack Voltage: {:.2f}V\t High Temp: {:.1f}C\t dtc flags: {}'.format(pack_current*0.1,pack_voltage*0.1,temp_high,dtc_flags))
        return (pack_current,temp_high,pack_voltage,dtc_flags)
    elif int(m_id) == 103:
        cell_id, m_bytes = ord(m_bytes[:1]), m_bytes[1:]
        cell_id = cell_id+1
        instant_voltage,internal_resistance,open_voltage = struct.unpack('>HHH',m_bytes)
        #print('Cell: {:2.0f}\t Voltage: {:.2f} mV\t Resistance: {:.2f} mOhm\t Open Volts: {:.2f} mV'.format(cell_id,instant_voltage*0.1,internal_resistance*0.01,open_voltage*0.1))
        
        if (instant_voltage*0.1 <= 3.4):
            print("ERROR: LOW VOLTAGE")
        else:
            print('Cell: {:2.0f}\t Voltage: {:.2f} mV'.format(cell_id,instant_voltage*0.1))
        return (cell_id,instant_voltage,internal_resistance,open_voltage)

def clean_data(string):
    j = 0
    for i in string:
        if i == 116: #binary t
            break
        j=j+1
    return string[j:]
def read_bms():
    cells = [0,0,0,0,0,0,0,0,0,0,0,0]
    output = {
        "temp_avg":"",
        "temp_low":"",
        "temp_high":"",
        "highest_cell_voltage":"",
        "pack_voltage":"",
        "pack_current":"",
        "dtc_flags":"",
        "cells":""
    }
    while 0 in cells:
        try:
            # Message format
            # tIIILDDDDDDDDTTTT
            # III = CAN ID
            # L = Message Length
            # D = Message data
            # T = Timestamp
            raw = ser.read_until(b'\r')
            message = str(clean_data(raw)[1:])
            m_id = message[2:5]
            m_message = message[4:-3]
            m_bytes = bytearray.fromhex(m_message[2:-2]) #cut off checksum and byte legnth
            data = decode(m_id,m_bytes)
            if m_id == '103':
                cells[data[0]-1] = data
            elif m_id == '100':
                output["temp_high"] = data[1]
                output["pack_voltage"] = data[2]
                output["pack_current"] = data[0]
                output["dtc_flags"] = data[3]
            elif m_id == '101':
                output["temp_avg"] = data[0]
                output["temp_low"] = data[1]
                output["highest_cell_voltage"] = data[2]
            else:
                 print("\n")
        except (serial.serialutil.SerialException):
            print(" !!!!")
    output["cells"] = cells
    return output

while True:
    read_bms()
