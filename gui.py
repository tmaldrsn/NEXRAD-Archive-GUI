import sys
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import radar
import colors

##### MENU BAR #####

class MenuBar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent)
        self.parent = parent

        # File Menu
        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Load File", underline=0, command=self.load_file)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

        # Messages Menu - for each message, pop up data table containing pertinant info
        messagesMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Messages", menu=messagesMenu)
        messagesMenu.add_command(label="Type 15: Clutter Filter Map")
        messagesMenu.add_command(label="Type 13: Clutter Filter Bypass Map")
        messagesMenu.add_command(label="Type 18: RDA Adaptation Data")
        messagesMenu.add_command(label="Type 3: Performance / Maintenance Data")
        messagesMenu.add_command(label="Type 5: Volume Coverage Pattern Data")
        messagesMenu.add_command(label="Type 2: RDA Status Data")
        messagesMenu.add_separator()
        messagesMenu.add_command(label="Type 31: Digital Radar Generic Format Blocks")

        # Help Menu - open browser to NOAA NEXRAD page or local documentation pdfs
        helpMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=helpMenu)
        helpMenu.add_command(label="NEXRAD Documentation")

    def load_file(self):
        rep = filedialog.askopenfilenames(parent=self, initialdir='raw/')[0]
        vol = radar.Volume(rep)
        self.parent.IS_FILE_LOADED = True
        self.parent.LOADED_FILE = rep
        self.parent.LOADED_VOLUME = vol
        self.parent.update_labels()
        self.parent.optionsframe.update_options_layout()
        self.parent.radarframe.update_plot()

    def quit(self):
        sys.exit(0)


##### FRAMES #####    

class RadarFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(height=600, width=600, bg='white')
        self.parent = parent

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111, projection='polar')
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def clear_figure(self):
        self.ax.clear()
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        if hasattr(self, 'cb'):
            self.cb.remove()

    def update_plot(self, *args):
        elev = self.parent.optionsframe.elevation.get()
        moment = self.parent.optionsframe.scan.get()
        data = self.parent.LOADED_VOLUME.elevation_data(elev, moment)
        self.clear_figure()

        colordict = colors.get_colordict(moment)
        cmap, norm = colors.get_cmap(colordict)
        self.im = self.ax.pcolormesh(data[0], data[1], data[2], cmap=cmap, norm=norm)    
        self.cb = self.fig.colorbar(self.im, ax=self.ax)
        self.fig.tight_layout()
        self.canvas.draw()


class OptionsFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(height=300, width=200)
        self.parent = parent

        self.elevation = tk.IntVar()
        self.elevation.set(1)

        self.num_elevations = 1
        self.elevation_selector = tk.OptionMenu(self, self.elevation, *list(range(1, self.num_elevations+1)))
        self.elevation_selector.configure(state='disabled')

        self.elevation.trace('w', self.update_options_layout)
        self.elevation_label = tk.Label(self, text="Elevation: ")
        self.elevation_label.grid(row=0, column=0)
        self.elevation_selector.grid(row=0, column=1)

        self.scan = tk.StringVar()
        self.scan.set("DREF")
        self.scan.trace('w', self.parent.radarframe.update_plot)
        self.REF_button = tk.Radiobutton(self, text="Reflectivity", variable=self.scan, value="DREF")
        self.VEL_button = tk.Radiobutton(self, text="Velocity", variable=self.scan, value="DVEL")
        self.SW_button = tk.Radiobutton(self, text="Spectrum Width", variable=self.scan, value="DSW")
        self.ZDR_button = tk.Radiobutton(self, text="Differential Reflectivity", variable=self.scan, value="DZDR")
        self.PHI_button = tk.Radiobutton(self, text="Differential Phase", variable=self.scan, value="DPHI")
        self.RHO_button = tk.Radiobutton(self, text="Correlation Coefficient", variable=self.scan, value="DRHO")

        self.REF_button.grid(row=3, sticky='w')
        self.VEL_button.grid(row=4, sticky='w')
        self.SW_button.grid(row=5, sticky='w')
        self.ZDR_button.grid(row=6, sticky='w')
        self.PHI_button.grid(row=7, sticky='w')
        self.RHO_button.grid(row=8, sticky='w')

        self.REF_button.config(state='disabled')
        self.VEL_button.config(state='disabled')
        self.SW_button.config(state='disabled')
        self.ZDR_button.config(state='disabled')
        self.PHI_button.config(state='disabled')
        self.RHO_button.config(state='disabled')


    def update_options_layout(self, *args):
        self.num_elevations = self.parent.LOADED_VOLUME.num_elevations()
        self.elevation_selector.configure(state='normal')        
        self.elevation_selector['menu'].delete(0, 'end')
        for i in range(1, self.num_elevations):
            self.elevation_selector['menu'].add_command(label=i, command=tk._setit(self.elevation, i))
        scans = self.parent.LOADED_VOLUME.available_scans()
        buttons = {
            'DREF': self.REF_button,
            'DVEL': self.VEL_button,
            'DSW': self.SW_button,
            'DZDR': self.ZDR_button,
            'DPHI': self.PHI_button,
            'DRHO': self.RHO_button
        }
        for button in buttons.values():
            button.configure(state='disabled')
        for scan in scans[self.elevation.get()]:
            buttons[scan].configure(state='normal')
            

class InfoBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.config(height=300, width=200)
        self.parent = parent

        self.setup_info_labels()

    def setup_info_labels(self):
        self.date_label = tk.Label(self, text="Date: ")
        self.time_label = tk.Label(self, text="Local Time: ")
        self.station_label = tk.Label(self, text="Station: ")

        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.station_var = tk.StringVar()

        self.date_var.set('N/A')
        self.time_var.set('N/A')
        self.station_var.set('N/A')

        self.date_label.grid(row=0, column=0, sticky='w')
        self.time_label.grid(row=1, column=0, sticky='w')
        self.station_label.grid(row=2, column=0, sticky='w')

        # come back and fix these, putting in static info
        self.date = tk.Label(self, textvariable=self.date_var)
        self.time = tk.Label(self, textvariable=self.time_var)
        self.station = tk.Label(self, textvariable=self.station_var)

        self.date.grid(row=0, column=1, sticky='w')
        self.time.grid(row=1, column=1, sticky='w')
        self.station.grid(row=2, column=1, sticky='w')


##### MAIN APPLICATION #####

class RadarApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        self.IS_FILE_LOADED = False
        self.LOADED_FILE = None
        self.LOADED_VOLUME = None

        self.configure_layout()

    def configure_layout(self):
        self.config(height=600, width=800)
        self.title("Radar Viewer!")

        menubar = MenuBar(self)
        self.config(menu=menubar)

        # configure main layout
        self.radarframe = RadarFrame(self)
        self.optionsframe = OptionsFrame(self)
        self.infobar = InfoBar(self)

        self.radarframe.grid(row=0, column=0, rowspan=2)
        self.optionsframe.grid(row=0, column=1)
        self.infobar.grid(row=1, column=1) 


    def update_labels(self):
        self.infobar.date_var.set(self.LOADED_VOLUME.HEADER["Date"])
        self.infobar.time_var.set(self.LOADED_VOLUME.HEADER["Time"])
        self.infobar.station_var.set(self.LOADED_VOLUME.HEADER["ICAO"])


if __name__=='__main__':
    root = RadarApplication()
    root.mainloop()
