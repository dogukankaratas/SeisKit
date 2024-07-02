from scipy import integrate
import numpy as np
def ariasIntensityCreator(filteredAcc, samplingInterval):
    ariasTime = samplingInterval * np.linspace(0, len(filteredAcc), num=len(filteredAcc))
    ariasIntensity = []
    durationAriasIntensity = []
    accSquare = [data**2 for data in filteredAcc]
    for counter, data in enumerate(filteredAcc):
        ariasIntensity = samplingInterval * integrate.cumtrapz(accSquare[:])

    # calculate the time
    arias05 = 0.05 * ariasIntensity[-1]
    arias95 = 0.95 * ariasIntensity[-1]

    timeAriasList = [index for index,value in enumerate(ariasIntensity) if value > 0.05*ariasIntensity[-1] and value < 0.95*ariasIntensity[-1] ]    
    durationAriasIntensity.append( ariasTime[timeAriasList[-1]] - ariasTime[timeAriasList[0]] )

    ariasDict = {'ariasIntesity': ariasIntensity, 
                 'arias05': arias05, 'arias95': arias95, 
                 'timeAriasList': timeAriasList, 
                 'ariasTime' : ariasTime,
                 'durationAriasIntensity': durationAriasIntensity}

    return ariasDict