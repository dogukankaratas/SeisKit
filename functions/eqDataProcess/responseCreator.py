def ResponseSpectra(acceleration, sampling_interval, damping_ratio = 0.05, Tmax = 6, T_int = 0.05):

    '''      
    Response spectra using piecewise
    
    Input:
        T: vector with periods (s)
        s: acceleration time series
        zi: damping ratio
        dt: time steps for s
    
    Returns:
        T, SA
    
    '''

    import numpy as np
    T = np.arange(  T_int , Tmax + T_int , T_int)
    s = acceleration
    zi = damping_ratio
    dt = sampling_interval

    pi = np.pi
    
    nper = np.size(T)						      # number of natural periods
    n    = np.size(s)                             # length of record
    
    SD   = np.zeros(nper)				          # rel. displac. spectrum
    SV   = np.zeros(nper)				          # rel. vel. spectrum
    SA   = np.zeros(nper)				          # total acc. spectrum	
     
    
    for k in range(nper):
       wn = 2*pi/T[k]
       wd = wn*(1-zi**2)**(1/2)
       
       u = np.zeros((2,n))          # matrix with velocities and displacements
       
       ex = np.exp(-zi*wn*dt)
       cwd = np.cos(wd*dt)
       swd = np.sin(wd*dt)
       zisq = 1/(np.sqrt(1-(zi**2)))
    
       a11 = ex*(cwd+zi*zisq*swd)
       a12 = (ex/wd)*swd
       a21 = -wn*zisq*ex*swd
       a22 = ex*(cwd-zi*zisq*swd)
    
       b11 = ex*(((2*zi**2-1)/((wn**2)*dt)+zi/wn)*(1/wd)*np.sin(wd*dt)+
           (2*zi/((wn**3)*dt)+1/(wn**2))*np.cos(wd*dt))-2*zi/((wn**3)*dt)
       b12 = -ex*(((2*zi**2-1)/((wn**2)*dt))*(1/wd)*np.sin(wd*dt)+
           (2*zi/((wn**3)*dt))*np.cos(wd*dt))-(1/(wn**2))+2*zi/((wn**3)*dt)
       b21 = -((a11-1)/((wn**2)*dt))-a12
       b22 = -b21-a12
       
       A = np.array([[a11,a12],[a21,a22]])
       B = np.array([[b11,b12],[b21,b22]])
    
       for q in range(n-1):
          u[:,q+1] = np.dot(A,u[:,q]) + np.dot(B,np.array([s[q],s[q+1]]))
       
       at = -2*wn*zi*u[1,:]-(wn**2)*u[0,:]
       
       SD[k]   = np.max( np.abs(u[0,:]) )
       SV[k]   = np.max( np.abs(u[1,:]) )
       SA[k]   = np.max( np.abs(at) )
    
    PSV = (2*pi/T)*SD                    # pseudo-vel. spectrum
    PSA = (2*pi/T)**2 *SD  	             # pseudo-accel. spectrum
    
    return T , SA 