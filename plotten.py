import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

def convert_date(date_bytes):
    return mdates.strpdate2num("%d.%m.%Y %H:%M")(date_bytes.decode('ascii'))

def lf():
    Zeit = np.loadtxt('luftfeuchtelog.txt', delimiter=';',converters={0:convert_date}, usecols=(0), unpack=True) #läd die zugehörigen Datumswerte
    data = np.genfromtxt('luftfeuchtelog.txt', delimiter=';') #läd die Daten ein
    anzahl=len(data)
    anzahl_messungen=6*24*30#6messungen/h * Stunden * Tage;  wird zu 0 wenn gesamter Zeitraum betrachtet wird
    zeitraum=anzahl-anzahl_messungen #ende Messzeitraum abzüglich der angegebenen Messungen
    def versatz(v):
        return v[zeitraum:anzahl]

    #für zweite achse nötig
    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    ax1 = host.twinx()
    ax2 = host.twinx()


    #Gleitender Mittelwert
    gleitwert = int(round(0.1*anzahl_messungen)) # 6messungen/h * Stunden * Tage; je größer desto verschmierter
    Ti=pd.rolling_mean(data[:,1], gleitwert)
    rFi=pd.rolling_mean(data[:,2], gleitwert)
    aFi=pd.rolling_mean(data[:,3], gleitwert)
    Ta=pd.rolling_mean(data[:,4], gleitwert)
    rFa=pd.rolling_mean(data[:,5], gleitwert)
    aFa=pd.rolling_mean(data[:,6], gleitwert)


    #definition für Hauptachse links
    host.set_xlabel('Zeit')
    host.set_ylabel('Temperatur [°C]')
    #definition für nebenachsen rechts
    ax1.set_ylabel('absolute Luftfeuchte [g/m^3]')
    ax2.set_ylabel('relative Luftfeuchte [%]')
    host.plot_date(versatz(Zeit), versatz(Ti), color='tab:red', label='iTmp', fmt="r-")# fmt verbindet datenpunkte der funktion plot_date zu einer Linie
    host.plot_date(versatz(Zeit), versatz(Ta), color='tab:blue', label='aTmp', fmt="r-")
    ax1.plot_date(versatz(Zeit), versatz(aFi),linestyle='--', color='tab:red', label='iF ABS', fmt="r-")
    ax1.plot_date(versatz(Zeit), versatz(aFa),linestyle='--', color='tab:blue', label='aF ABS', fmt="r-")
    ax2.plot_date(versatz(Zeit), versatz(rFi), linestyle=':', color='tab:red', label='iF REL', fmt="r-")
    ax2.plot_date(versatz(Zeit), versatz(rFa), linestyle=':', color='tab:blue', label='aF REL', fmt="r-")

    #formatieren des plots
    #zweite und dritte achse verschieben
    offset = 60
    new_fixed_axis = ax2.get_grid_helper().new_fixed_axis
    ax2.axis["right"] = new_fixed_axis(loc="right",axes=ax2,offset=(offset, 0))
    offset = 0
    new_fixed_axis = ax1.get_grid_helper().new_fixed_axis
    ax1.axis["right"] = new_fixed_axis(loc="right",axes=ax1,offset=(offset, 0))
    ax2.axis["right"].toggle(all=True)
    #Zeitachse formatieren
    host.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    host.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #Titel und Legende
    plt.title("Luftfeuchteverlauf im Keller")
    host.legend(loc='upper center', ncol=3, fontsize=5)
    #plt.show()
    plt.plot()
    plt.savefig('luftfeuchtelog.png', dpi=300)

def temp():
    Zeit = np.loadtxt('templog.txt', delimiter=';',converters={0:convert_date}, usecols=(0), unpack=True) #läd die zugehörigen Datumswerte
    data = np.genfromtxt('templog.txt', delimiter=';') #läd die Daten ein
    anzahl=len(data)
    anzahl_messungen=6*24*30#6messungen/h * Stunden * Tage;  wird zu 0 wenn gesamter Zeitraum betrachtet wird
    zeitraum=anzahl-anzahl_messungen #ende Messzeitraum abzüglich der angegebenen Messungen
    def versatz(v):
        return v[zeitraum:anzahl]

    #für zweite achse nötig
    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    ax1 = host.twinx()
    ax2 = host.twinx()


    #Gleitender Mittelwert
    gleitwert = int(round(0.1*anzahl_messungen)) # 6messungen/h * Stunden * Tage; je größer desto verschmierter
    Ti=pd.rolling_mean(data[:,1], gleitwert)
    rFi=pd.rolling_mean(data[:,2], gleitwert)
    aFi=pd.rolling_mean(data[:,3], gleitwert)
    #Ta=pd.rolling_mean(data[:,4], gleitwert)
    #rFa=pd.rolling_mean(data[:,5], gleitwert)
    #aFa=pd.rolling_mean(data[:,6], gleitwert)


    #definition für Hauptachse links
    host.set_xlabel('Zeit')
    host.set_ylabel('Temperatur [°C]')
    #definition für nebenachsen rechts
    ax1.set_ylabel('absolute Luftfeuchte [g/m^3]')
    ax2.set_ylabel('relative Luftfeuchte [%]')
    host.plot_date(versatz(Zeit), versatz(Ti), color='tab:red', label='iTmp', fmt="r-")# fmt verbindet datenpunkte der funktion plot_date zu einer Linie
    #host.plot_date(versatz(Zeit), versatz(Ta), color='tab:blue', label='aTmp', fmt="r-")
    ax1.plot_date(versatz(Zeit), versatz(aFi),linestyle='--', color='tab:red', label='iF ABS', fmt="r-")
    #ax1.plot_date(versatz(Zeit), versatz(aFa),linestyle='--', color='tab:blue', label='aF ABS', fmt="r-")
    ax2.plot_date(versatz(Zeit), versatz(rFi), linestyle=':', color='tab:red', label='iF REL', fmt="r-")
    #ax2.plot_date(versatz(Zeit), versatz(rFa), linestyle=':', color='tab:blue', label='aF REL', fmt="r-")

    #formatieren des plots
    #zweite und dritte achse verschieben
    offset = 60
    new_fixed_axis = ax2.get_grid_helper().new_fixed_axis
    ax2.axis["right"] = new_fixed_axis(loc="right",axes=ax2,offset=(offset, 0))
    offset = 0
    new_fixed_axis = ax1.get_grid_helper().new_fixed_axis
    ax1.axis["right"] = new_fixed_axis(loc="right",axes=ax1,offset=(offset, 0))
    ax2.axis["right"].toggle(all=True)
    #Zeitachse formatieren
    host.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    host.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    #Titel und Legende
    plt.title("Temperaturverlauf")
    host.legend(loc='upper center', ncol=3, fontsize=5)
    #plt.show()
    plt.plot()
    plt.savefig('templog.png', dpi=300)
