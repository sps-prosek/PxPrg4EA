import serial
from serial.serialutil import SerialException
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

SERIAL_PORT = "/dev/cu.usbmodem21401"
BAUD_RATE = 115200

ser = None

while ser is None:
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
    except SerialException as e:
        ser = None

plotData = {}
tSeries = []


def read_data():
    global plotData, tSeries
    try:
        data = ser.readline().decode().strip().split(",")
        print(data)
        for data in data:
            name, value = data.split(":")
            name = name.strip()
            value = float(value.strip())
            if name == "Time":
                tSeries.append(value)
            else:
                if name not in plotData:
                    plotData[name] = [value]
                else:
                    plotData[name].append(value)
    except SerialException as e:
        try:
            plotData = {}
            tSeries = []
            ser.close()
            ser.open()
            read_data()
        except:
            pass
    except:
        pass


def update_plot(frame):
    global plotData, tSeries
    read_data()
    if plotData == {}:
        return
    df = pd.DataFrame(plotData, index=tSeries)
    ax.clear()
    df.plot(ax=ax)
    ax.legend(loc="upper left")
    ax.set_title("Real-time Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")


plt.ion()
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_plot, interval=1)
plt.show(block=True)
