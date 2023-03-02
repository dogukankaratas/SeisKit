import math
import pandas as pd
import numpy as np
import scipy.interpolate as interp
from scipy.interpolate import interp1d

def tbecTargetSpectrum(lat, lon, vs30, intensity):
    """
    Creates TBEC-2018 Target Spectrum
    Args:
        lat (float): latitude of location
        lon (float): longitude of location
        vs30 (float): Vs30 value
        intensity (str): intensity level 
            options: DD1, DD2, DD3, DD4

    Returns:
        spectralValuesDict: dict of spectral values
    """
    afad_spectra_params_df = pd.read_csv("data/eqDataProcess/AFAD_TDTH_parametre.csv")   

    # grid locattions
    x = afad_spectra_params_df["LAT"].to_list()
    y = afad_spectra_params_df["LON"].to_list()
    
    # spectral values dictionary
    spectral_value_dict = {}
    for column_name in ["Ss","S1","PGA","PGV"]:

        z = afad_spectra_params_df[ f"{column_name}-{intensity}"].to_list()

        interpolator = interp.CloughTocher2DInterpolator( np.array([x,y]).T , z)

        spectral_value = np.round( interpolator( lat,lon)  , 3 )
        
        spectral_value_dict[column_name] = spectral_value

    # get soil class from Vs30
    vs30_values = [ 0 , 180 , 360 , 760 , 1_500 , 20_000 ]
    soil_class_list = [ "ZE" , "ZD" , "ZC" , "ZB" , "ZA" ]
    vs_limit , count = 0 , 0
    while vs30 >= vs_limit:
        soilClass =  soil_class_list[ count ]
        count += 1
        vs_limit = vs30_values[ count]

    # get short period and 1-sec period
    Ss = spectral_value_dict["Ss"] 
    S1 = spectral_value_dict["S1"] 

    # Spectral values
    Ss_range = [0.25 , 0.50 , 0.75, 1.00 , 1.25 , 1.50 ]

    FS_table = {"ZA": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZB": [0.9 , 0.9 , 0.9 , 0.9 , 0.9 , 0.9], 
                "ZC": [1.3 , 1.3 , 1.2 , 1.2 , 1.2 , 1.2],
                "ZD": [1.6 , 1.4 , 1.2 , 1.1 , 1.0 , 1.0],
                "ZE": [2.4 , 1.7 , 1.3 , 1.1 , 0.9 , 0.8]}

    S1_range = [0.10 , 0.20 , 0.30, 0.40 , 0.50 , 0.60 ]

    F1_table = {"ZA": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZB": [0.8 , 0.8 , 0.8 , 0.8 , 0.8 , 0.8], 
                "ZC": [1.5 , 1.5 , 1.5 , 1.5 , 1.5 , 1.4],
                "ZD": [2.4 , 2.2 , 2.0 , 1.9 , 1.8 , 1.7],
                "ZE": [4.2 , 3.3 , 2.8 , 2.4 , 2.2 , 2.0]}

    # Short period
    if Ss < Ss_range[0]:
        Fs = FS_table[soilClass][0]
        SDs = Ss * Fs
    elif Ss > Ss_range[-1]:
        Fs = FS_table[soilClass][-1]
        SDs = Ss * Fs    
    else:
        FS_satir = interp1d(Ss_range, FS_table[soilClass], kind='linear')
        FS_katsayisi = FS_satir(Ss)
        Fs = round( float(FS_katsayisi) , 2) 
        SDs = Ss * Fs
    # 1sec period
    if S1 < S1_range[0] :
        F1 = F1_table[soilClass][0]
        SD1 = S1 * F1
    elif S1 > S1_range[-1]:
        F1 = F1 = F1_table[soilClass][-1]
        SD1 = S1 * F1
    else:    
        F1_satir = interp1d(S1_range, F1_table[soilClass], kind='linear')
        F1_katsayisi = F1_satir(S1)
        F1 = round(float(F1_katsayisi) , 2)
        SD1 = S1 * F1

    # DTS
    if SDs < .33 : 
        DTS = 4
    elif SDs >= 0.33 and SDs < 0.50 : 
        DTS = 3
    elif SDs >= 0.50 and SDs < 0.75 :
        DTS = 2 
    else : 
        DTS = 1

    # Corner period values
    TA = 0.2 * SD1 / SDs
    TB = SD1 / SDs
    TL = 6

    # Function for lateral spectral values
    def spektraHorizontal(T,SDs,SD1, TA, TB , TL):  
        if T < TA :
            return((0.4 + 0.6*(T/TA))*SDs)
        elif T >= TA and T <= TB:
            return(SDs)
        elif T> TB and T <= TL:
            return(SD1 / T)
        elif T> TL:
            return(SD1*TL/(T**2))

   # Function for vertical spectral values

    def spektraVertical(T,SDs,SD1, TA, TB , TL):  
        TAD , TBD , TLD = TA / 3 , TB / 3 , TL / 2
        if T < TAD :
            return(( 0.32 + 0.48*(T/TAD))*SDs)
        elif T >= TAD and T <= TBD:
            return(0.8 * SDs)
        elif T> TBD and T <= TLD:
            return( 0.8 * SDs * TBD / T)
        elif T> TLD:
            return( np.nan )

    # Creating the spectrum
    period_list = np.linspace( 0.0 , 5.0 , 1001)

    spectral_horizontal_orbits = [ spektraHorizontal(period,SDs,SD1, TA, TB , TL) for period in period_list ]
    spectral_vertical_orbits = [ spektraVertical(period,SDs,SD1, TA, TB , TL) for period in period_list ]

    pga = spectral_value_dict["PGA"]
    pgv = spectral_value_dict["PGV"]

    spectralValuesDict = {"Ss":Ss , "S1":S1 , "PGA":pga, "PGV": pgv, "Fs":Fs, "F1":F1, "SDs":round(SDs, 3), 
                          "SD1":round(SD1, 3) , "TA":round(TA,2) ,"TB":round(TB,2), "TL":round(TL,2), 
                          "DTS" : DTS , "Soil Class" : soilClass, 'T': period_list, 'Sa': spectral_horizontal_orbits, 'Sad':spectral_vertical_orbits}

    return(spectralValuesDict)








    

