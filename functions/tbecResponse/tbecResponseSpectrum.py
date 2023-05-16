from dataclasses import asdict, dataclass, field
import math
import pandas as pd
import numpy as np
import scipy.interpolate as interp
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt

@dataclass
class SeismicInputs:
    """
    Args:
        lat       : latitude of location
        lon       : longitude of location
        soil      : soil class
        intensity : intensity level 
                        options: DD1, DD2, DD3, DD4
        R         : Yapi davranis katsayisi
        D         : Overstrength factor (Dayanim fazlalagi katsayisi)
        I         : Building important factor (Bina onem katsayisi)
        Ss        : Kisa periyot harita katsayisi
        S1        : 1 sn periyot harita katsayisi
        soil      : Zemin sinifi
        TL        : Spektrum hesabindaki en uç periyot
        PGA       : Peak ground acceleration
        PGV       : Peak ground acceleration
        Fs        : Kisa periyot harita spektral ivme katsayisi [boyutsuz]
        F1        : 1.0 saniye için harita spektral ivme katsayisi [boyutsuz]
        SDs       : Kisa periyot tasarim spektral ivme katsayisi [boyutsuz]
        SD1       : 1.0 saniye periyot için tasarim spektral ivme katsayisi [boyutsuz]
        TA        : Corner period in spectrum (Kose periyod)
        TB        : Corner period in spectrum (Kose periyod)
        TL        : Long period (Uzun periyod)
        
    """

    lat       : float= field(default_factory=float)
    lon       : float= field(default_factory=float)
    soil      : str= field(default_factory=str)
    intensity : str= field(default_factory=str)
    DTS       : int = field(default=1)
    R         : float = field(default=8.)
    D         : float = field(default=3.)
    I         : float = field(default=1.)
    Ss        : float = field(default=0.)
    S1        : float = field(default=0.)
    PGA       : float = field(default=0.)
    PGV       : float = field(default=0.)
    Fs        : float = field(default=0.)
    F1        : float = field(default=0.)
    SDs       : float = field(default=0.)
    SD1       : float = field(default=0.)
    TA        : float = field(default=0.)
    TB        : float = field(default=0.)
    TL        : float = field(default=6.)

    def __repr__(self) -> str:
        return f"Latitude :{self.lat}\nLongitude :{self.lon}\nSoil Class :{self.soil}\nIntensity:{self.intensity}\nR :{self.R}\nD :{self.D}\nI :{self.I}\nSs :{self.Ss}\nS1 :{self.S1}\nPGA :{self.PGA}\nPGV :{self.PGV}\nFs :{self.Fs}\nF1 :{self.F1 }\nSDs :{self.SDs}\nSD1 :{self.SD1}\nTA :{self.TA}\nTB :{self.TB}\nTL :{self.TL}"

    def dict(self) -> dict:
        return asdict(self)
    
    def convert_dataframe(self) -> pd.DataFrame:
        dumy = self.dict()
        dumy_df = pd.DataFrame([dumy])
        del dumy
        return dumy_df


@dataclass
class SeismicTSC:
    Variables : SeismicInputs = field(default_factory=SeismicInputs)


    def __post_init__(self) -> None:
        self.__GetSpectralMapCoefficient()
        self.__GetDTS()
        self.__Get_TA()
        self.__Get_TB()
        self.ElasticHorizontalSpectrum = self.__HorizontalElasticSpectrum()
        self.__HorizontalDisplacementSpectrum()
        self.__VerticalElasticSpektrum()
        self.__ReducedTargetSpectrum()
        

    def __GetSpectralMapCoefficient(self) -> None:
        """Spektrum haritasinda verilen koordinatlara göre spektral harita değerlerini bulur"""
        afad_spectra_params_df = pd.read_csv("data/eqDataProcess/AFAD_TDTH_parametre.csv")   

        # grid locattions
        x = afad_spectra_params_df["LAT"].to_list()
        y = afad_spectra_params_df["LON"].to_list()
        
        # spectral values dictionary
        spectral_value_dict = {}
        for column_name in ["Ss","S1","PGA","PGV"]:

            z = afad_spectra_params_df[ f"{column_name}-{self.Variables.intensity}"].to_list()

            interpolator = interp.CloughTocher2DInterpolator( np.array([x,y]).T , z)

            spectral_value = np.round( interpolator( self.Variables.lat, self.Variables.lon)  , 3 )
            spectral_value_dict[column_name] = spectral_value
        
        self.Variables.Ss = spectral_value_dict["Ss"]
        self.Variables.S1 = spectral_value_dict["S1"]
        self.Variables.PGA = spectral_value_dict["PGA"]
        self.Variables.PGV = spectral_value_dict["PGV"]

        del afad_spectra_params_df,spectral_value_dict

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
        if self.Variables.Ss < Ss_range[0]:
            self.Variables.Fs = FS_table[self.Variables.soil][0]
            self.Variables.SDs = self.Variables.Ss * self.Variables.Fs
        elif self.Variables.Ss > Ss_range[-1]:
            self.Variables.Fs = FS_table[self.Variables.soil][-1]
            self.Variables.SDs = self.Variables.Ss * self.Variables.Fs    
        else:
            FS_satir = interp1d(Ss_range, FS_table[self.Variables.soil], kind='linear')
            FS_katsayisi = FS_satir(self.Variables.Ss)
            self.Variables.Fs = round( float(FS_katsayisi) , 2) 
            self.Variables.SDs = self.Variables.Ss * self.Variables.Fs

        # 1sec period
        if self.Variables.S1 < S1_range[0] :
            self.Variables.F1 = F1_table[self.Variables.soil][0]
            self.Variables.SD1 = self.Variables.S1 * self.Variables.F1
        elif self.Variables.S1 > S1_range[-1]:
            self.Variables.F1 = F1_table[self.Variables.soil][-1]
            self.Variables.SD1 = self.Variables.S1 * self.Variables.F1
        else:    
            F1_satir = interp1d(S1_range, F1_table[self.Variables.soil], kind='linear')
            F1_katsayisi = F1_satir(self.Variables.S1)
            self.Variables.F1 = round(float(F1_katsayisi) , 2)
            self.Variables.SD1 = self.Variables.S1 * self.Variables.F1
        
        del Ss_range,FS_table,S1_range,F1_table

    def __GetDTS(self) -> None:
        """
        Get building seismic design classification
        """
        if self.Variables.SDs < .33 : 
            self.Variables.DTS = 4
        elif self.Variables.SDs >= 0.33 and self.Variables.SDs < 0.50 : 
            self.Variables.DTS = 3
        elif self.Variables.SDs >= 0.50 and self.Variables.SDs < 0.75 :
            self.Variables.DTS = 2 
        else : 
            self.Variables.DTS = 1
        pass

    def __Get_TA(self) -> float:
        """Yatay elastik tasarim spektrum sol köşe periyodu"""
        self.Variables.TA = 0.2 * self.Variables.SD1 / self.Variables.SDs
    
    def __Get_TB(self) -> float:
        """Yatay elastik tasarim elastik spektrum sağ köşe periyodu"""
        self.Variables.TB = self.Variables.SD1 / self.Variables.SDs
    
    def __HorizontalElasticSpectrum(self)-> pd.DataFrame:
        """TBDY yatay elastik tasarim spektrumu"""

        T_list = np.arange(0.0, self.Variables.TL,.005)
            
        Sa = []
        
        for i in T_list:
            
            if i <self.Variables.TA:
                Sa.append(round((0.4 + 0.6*(i/self.Variables.TA))*self.Variables.SDs, 4))
                
            elif i >= self.Variables.TA and i <= self.Variables.TB:
                Sa.append(round(self.Variables.SDs, 4))
                
            elif i>self.Variables.TB and i <= self.Variables.TL:
                Sa.append(round(self.Variables.SD1/i, 4))
                
            elif i> self.Variables.TL:
                Sa.append(round(self.Variables.SD1 * self.Variables.TL/(i**2), 4))
                
        target_spec = {"T" : T_list,"Sae" : Sa}

        target_spec_df = pd.DataFrame().from_dict(target_spec)
        del target_spec,Sa,T_list
        
        return target_spec_df

    def __HorizontalDisplacementSpectrum(self) -> None:
        """Tbdy elastik tasarim deplasman spektrumunun hesabi"""
        Sde = [(T**2/4*3.14**2)*9.81*Sae for T,Sae in zip(self.ElasticHorizontalSpectrum["T"],self.ElasticHorizontalSpectrum["Sae"])]
        self.ElasticHorizontalSpectrum["Sde"] = Sde

    def __VerticalElasticSpektrum(self) -> None:
        """Dusey elastik dizayn spektrumu"""
        TAD , TBD , TLD = self.Variables.TA / 3 , self.Variables.TB / 3 , self.Variables.TL / 2
        Sve = []
        for T in self.ElasticHorizontalSpectrum["T"] :
            if T < TAD :
                Sve.append(( 0.32 + 0.48*(T/TAD))* self.Variables.SDs)
                continue
            elif T >= TAD and T <= TBD:
                Sve.append(0.8 * self.Variables.SDs)
                continue
            elif T> TBD and T <= TLD:
                Sve.append( 0.8 * self.Variables.SDs * TBD / T)
                continue
            elif T> TLD:
                Sve.append( np.nan )
                continue
        self.ElasticHorizontalSpectrum["Sve"] = Sve

        del Sve
   
    def __Get_Ra(self,T : float) -> float:
        """Verilen doğal titreşim periyoduna göre deprem yükü azaltma katsayisini hesaplar"""
        if T > self.Variables.TB:
            Ra = self.Variables.R / self.Variables.I
        else:
            Ra = self.Variables.D + ((self.Variables.R/self.Variables.I)-self.Variables.D)*(T/self.Variables.TB)
        return Ra

    def __ReducedTargetSpectrum(self) -> None:
        """Azaltilmis elastik tasarim spektrumu"""
        Tw = self.ElasticHorizontalSpectrum["T"]
        RaT = [ self.__Get_Ra(T) for T in Tw ]
        SaR = [(Sa/Ra) for Sa,Ra in zip(self.ElasticHorizontalSpectrum["Sae"],RaT)]
        self.ElasticHorizontalSpectrum["RaT"] = RaT
        self.ElasticHorizontalSpectrum["SaR"] = SaR
        del SaR,RaT,Tw
   
    def __Get_Sae_Tp(self,T : float) -> float:
        """ Binanin doğal titreşim periyoduna denk gelen elastik spektrum değerini bulur. """

        if T < self.Variables.TA:
            Sae = round((0.4 + 0.6*(T/self.Variables.TA))*self.Variables.SDs, 4)
            
        elif T >= self.Variables.TA and T<=self.Variables.TB:
           Sae = round(self.Variables.SDs, 4)
            
        elif T > self.Variables.TB and T <= self.Variables.TL:
            Sae = round(self.Variables.SD1/T, 4)
            
        elif T>self.Variables.TL:
            Sae = round(self.Variables.SD1 * self.Variables.TL / (T**2), 4)
        
        return round(Sae,4)
    
    def Get_SaR_Tp(self,T : float) -> float:
        """Verilen periyoda göre azaltilmiş elastik tasarim spektrum ivmesini hesaplar"""
        Ra = self.__Get_Ra(T)
        Sae = self.__Get_Sae_Tp(T)
        return round(Sae / Ra,4)        

    # def plot_HorizontalElasticSpectrum(self) -> None:
    #     fig, ax = plt.subplots(figsize=(5,5))
    #     fig.dpi=200
    #     ax.grid()
    #     ax.axvline(c = "k");ax.axhline(c = "k")
    #     ax2 = ax.twinx()
    #     ax.plot(self.ElasticHorizontalSpectrum["T"] ,self.ElasticHorizontalSpectrum["Sae"],label="Response Acc. Spec.")
    #     ax2.plot(self.ElasticHorizontalSpectrum["T"],self.ElasticHorizontalSpectrum["Sde"],label="Response Disp. Spec.",color = 'g')

    #     ax.set_xlabel('Period (sn)',fontsize = 12)  # Add an x-label to the axes.
    #     ax.set_ylabel('Pseudo-Spectral Accelerations (g)',fontsize = 12)  # Add a y-label to the axes.
    #     ax2.set_ylabel('Pseudo-Spectral Displacements (m)',fontsize = 12)  # Add a y-label to the axes.
    #     ax.set_title("TSC-2018 Design Elastic Spectrum",fontsize = 16)  # Add a title to the axes.
    #     plt.show()


# if __name__ == "__main__":
#     ss = SeismicInputs(35.1,lon=35.2,soil='ZB',intensity='DD2')
#     target = SeismicTSC(Variables= ss)

#     print(target.Variables.asdict())

    # target.plot_HorizontalElasticSpectrum()






    

