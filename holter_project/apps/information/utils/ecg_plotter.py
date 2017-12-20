# This script helps to plot ECG signals. 

import pandas as pd
from plotly import graph_objs
from plotly.offline import plot
from django.conf import settings

from scipy import signal
from scipy.signal import find_peaks_cwt
from numpy import polyfit
import numpy as np

from detect_peaks import detect_peaks

def plot_ecg(file_name):

    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)
    x=df['x']
    y=df['y']

    #---------------- Processing Signal----------------
    ## Filtro Pasa-Bajas
    y=signal.savgol_filter(y,21,7)

    ## Detrend
    p = polyfit((np.arange(len(y))),y,6)
    f_y = np.polyval(p,(np.arange(len(y))))
    ecg_data = y - f_y
    y = ecg_data

    ## Normalizar
    ecg_data = ecg_data/max(abs(ecg_data))
    y = ecg_data

    ## Picos Bajos
    peaks_index = detect_peaks(-ecg_data, mph=0.6, mpd=0.150, show=True)
    ecg_peaks = -ecg_data[peaks_index]
    tm_peaks = x[peaks_index]
    tm_peaks = np.array(tm_peaks)
    print 'Indices: ', peaks_index
    print 'Picos Bajos: ', ecg_peaks
    
    ## Segundos entre intervalos
    rateBPM_values = []
    rateBPM_sum    = 0
    if len(peaks_index) > 9:  #minimo 10 ciclos
        for i in range(1,len(peaks_index)):
            t_dif = tm_peaks[i]-tm_peaks[i-1]
            rateBPM_values.append(t_dif) 
        rateBPM_sum = sum(rateBPM_values)
    
    ## BPM
    rateBPM = len(tm_peaks)*1.0 / (x[x.last_valid_index()]-x[0]) * 60.0
    print 'rateBPM: ', rateBPM

    ## Mean R-R Interval
    rrmean_values = []
    rr_mean       = 0
    for i in range(0,len(rateBPM_values)):
        rr_mean = 0.75 * rr_mean + 0.25 * rateBPM_values[i]
        rrmean_values.append(rr_mean)

    up_rr_mean = np.where(rateBPM_values>=(rr_mean*1.15))
    down_rr_mean = np.where(rateBPM_values<(rr_mean*0.85))
    print 'RR-MEAN: ', rr_mean
    print 'UP-rr-mean', up_rr_mean
    print 'DOWN-rr-mean', down_rr_mean

    ## Resultado
    values = {'FA': False}
    if np.any(up_rr_mean):
        values['FA'] = True
    if np.any(down_rr_mean):
        values['FA'] = True

    #--------------------------------------------------

    trace1 = graph_objs.Scatter(
                        x=x, y=y, # Data
                        mode='lines', name='signal' # Additional options
                        )

    layout = graph_objs.Layout(title='ECG ('+file_name+')',
                   plot_bgcolor='rgb(230, 230,230)')
                   
    data = [trace1]
    fig = graph_objs.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div, values