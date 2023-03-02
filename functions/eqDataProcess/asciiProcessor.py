from scipy.signal import butter, lfilter
import scipy.signal as signal
import numpy as np
    
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 100
lowcut = .05
highcut = 20.0

def filterFunction( acceleration , fs ) :
    acceleration_filtered = signal.detrend(acceleration, type='linear')
    lowcut, highcut , order  = 0.025 , 40 , 1
    acceleration_filtered = butter_bandpass_filter(acceleration, lowcut, highcut, fs, order )
    acceleration_filtered = signal.detrend(acceleration_filtered, type='linear')
    return( [x*0.0010197 for x in acceleration_filtered] )

def asciiReader(file):

    accList = []
    for line in file:

        if line[0:8].decode("utf-8") == 'VS30_M/S':
            vs30 = float(line[9:15])

        if line[0:23].decode("utf-8") == 'STATION_LATITUDE_DEGREE':
            latitude = float(line[24:34])

        if line[0:24].decode("utf-8") == 'STATION_LONGITUDE_DEGREE':
            longitude = float(line[25:34])

        if line[0:12].decode("utf-8") == 'STATION_CODE':
            stationCode = line[13:18].decode("utf-8")

        if line[0:8].decode("utf-8") == 'LOCATION':
            stationLocation = line[9:50].decode("utf-8")

        integers = [str(x) for x in list(range(0, 101, 1))]
            
        if line.decode("utf-8")[0] == '-' or line.decode("utf-8")[0] in integers:
            accList.append(float(line[:-2]))

        if line[0:19].decode("utf-8") == 'SAMPLING_INTERVAL_S':
            sampling = float(line[20:25])

    accTime = np.arange(0, len(accList)*sampling, sampling)

    filteredAcc = filterFunction(accList, fs)

    rawAccList = [x*0.0010197 for x in accList]

    asciiDict = {'vs30': vs30, 'latitude':latitude, 'longitude':longitude, 
                'stationCode':stationCode, 'stationLocation':stationLocation, 
                'sampling':sampling, 'filteredAccList': filteredAcc, 'accTime':accTime, 'rawAccList': rawAccList}
        
    return asciiDict