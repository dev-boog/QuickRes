import tkinter
import os
import json
import ctypes

from tkinter import filedialog
from tkinter import messagebox 

class cod_settings:    
    home_directory = os.path.expanduser("~")
    cod_path = os.path.join(home_directory, "Documents", "Call of Duty", "players", "s.1.0.cod24.txt")
    
    aspectratio = "AspectRatio@0;19775;7764 = "
    displaymode = "DisplayMode@0;22564;11445 = "
    resolution = "Resolution@0;56178;35888 = "

# Application GUI
class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()

        with open("config.json", "r") as file:
            self.config = json.load(file)

        self.title("QuickRes") 
        self.frame = tkinter.Frame(self)
        self.frame.pack()

        # Resolution widgets
        self.resolution_frame = tkinter.LabelFrame(self.frame, text="Resolution")
        self.resolution_frame.grid(row=0, column=0, padx=20, pady=20)
        self.resolution_x_label = tkinter.Label(self.resolution_frame, text="X Resolution")
        self.resolution_x_label.grid(row=0, column=0)
        self.resolution_y_label = tkinter.Label(self.resolution_frame, text="Y Resolution")
        self.resolution_y_label.grid(row=0, column=1)
        self.resolution_x_input = tkinter.Entry(self.resolution_frame)
        self.resolution_y_input = tkinter.Entry(self.resolution_frame)
        self.resolution_x_input.grid(row=1, column=0)
        self.resolution_y_input.grid(row=1, column=1)    
        self.apply_resolution_btn = tkinter.Button(self.resolution_frame, text="Apply", command=self.set_cod_res)
        self.apply_resolution_btn.grid(row=1, column=2)
        for widget in self.resolution_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)
            
        # File path widgets
        self.filepath_frame = tkinter.LabelFrame(self.frame, text="File Path")
        self.filepath_frame.grid(row=0, column=1, padx=20, pady=5)
        self.filepath_location_label = tkinter.Label(self.filepath_frame, text="Call of Duty File Path")
        self.filepath_location_label.grid(row=0, column=0)
        self.filepath_location_input = tkinter.Entry(self.filepath_frame, width=50)
        self.filepath_location_input.grid(row=1, column=0)
        if self.config['file_path'] == "":
            if os.path.exists(cod_settings.cod_path):
                self.filepath_location_input.insert(0, f"{cod_settings.cod_path}")
            else:
                messagebox.showwarning("QuickRes", "We couldn't find the correct Call of Duty file path! Please enter it manually.")
        else:
            self.filepath_location_input.insert(0, f"{self.config['file_path']}")
        self.filepath_change_button = tkinter.Button(self.filepath_frame, text="Change", command= self.change_path)
        self.filepath_change_button.grid(row=1, column=1)
        for widget in self.filepath_frame.winfo_children():
            widget.grid_configure(padx=5, pady=5)

    def change_path(self):
        self.filepath_location_input.delete(0, "end") 
        new_file_path = filedialog.askopenfilename()
        self.config['file_path'] = new_file_path
        with open ("config.json", "w") as file:
            json.dump(self.config, file, indent=4)
            self.filepath_location_input.insert(0, f"{self.config['file_path']}")
        
    def set_cod_res(self):
        x = self.resolution_x_input.get()
        y = self.resolution_y_input.get()
        x = x.strip()
        y = y.strip()
        
        if x == "1920" and y == "1080": 
            aspect_ratio_text_replacement = cod_settings.aspectratio + "auto"
        else:
            aspect_ratio_text_replacement = cod_settings.aspectratio + "standard"
        resolution_text_replacement = cod_settings.resolution + x + "x" + y

        windows.edit_txt(cod_settings.cod_path, cod_settings.aspectratio, aspect_ratio_text_replacement)
        windows.edit_txt(cod_settings.cod_path, cod_settings.resolution, resolution_text_replacement)
        windows.set_monitor_res(int(x), int(y))

        messagebox.showinfo("QuickRes", f"Resolution has been changed to {x}x{y}!")

class windows:
    def set_monitor_res(width, height):
        class DEVMODE(ctypes.Structure):
            _fields_ = [
                ("dmDeviceName", ctypes.c_wchar * 32),
                ("dmSpecVersion", ctypes.c_ushort),
                ("dmDriverVersion", ctypes.c_ushort),
                ("dmSize", ctypes.c_ushort),
                ("dmDriverExtra", ctypes.c_ushort),
                ("dmFields", ctypes.c_ulong),
                ("dmPosition", ctypes.c_long * 2),
                ("dmDisplayOrientation", ctypes.c_ulong),
                ("dmDisplayFixedOutput", ctypes.c_ulong),
                ("dmColor", ctypes.c_short),
                ("dmDuplex", ctypes.c_short),
                ("dmYResolution", ctypes.c_short),
                ("dmTTOption", ctypes.c_short),
                ("dmCollate", ctypes.c_short),
                ("dmFormName", ctypes.c_wchar * 32),
                ("dmLogPixels", ctypes.c_ushort),
                ("dmBitsPerPel", ctypes.c_ulong),
                ("dmPelsWidth", ctypes.c_ulong),
                ("dmPelsHeight", ctypes.c_ulong),
                ("dmDisplayFlags", ctypes.c_ulong),
                ("dmDisplayFrequency", ctypes.c_ulong),
                ("dmICMMethod", ctypes.c_ulong),
                ("dmICMIntent", ctypes.c_ulong),
                ("dmMediaType", ctypes.c_ulong),
                ("dmDitherType", ctypes.c_ulong),
                ("dmReserved1", ctypes.c_ulong),
                ("dmReserved2", ctypes.c_ulong),
                ("dmPanningWidth", ctypes.c_ulong),
                ("dmPanningHeight", ctypes.c_ulong),
            ]

        CDS_UPDATEREGISTRY = 0x01
        CDS_TEST = 0x02
        DISP_CHANGE_SUCCESSFUL = 0

        dm = DEVMODE()
        dm.dmSize = ctypes.sizeof(DEVMODE)
        dm.dmPelsWidth = width
        dm.dmPelsHeight = height
        dm.dmFields = 0x00080000 | 0x00100000  # DM_PELSWIDTH | DM_PELSHEIGHT

        result = ctypes.windll.user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_TEST)
        if result == DISP_CHANGE_SUCCESSFUL:
            ctypes.windll.user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_UPDATEREGISTRY)
        else:
            messagebox.showerror("QuickRes", "We could not change your screeb resolution!")            

    def edit_txt(file_path, search_text, replacement_text):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            modified_lines = []
            for line in lines:
                if search_text in line:
                    modified_lines.append(replacement_text + '\n') 
                else:
                    modified_lines.append(line)
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)
        except FileNotFoundError:
            messagebox.showerror("QuickRes", "Could not find the file!")
        except Exception as e:
            messagebox.showerror("QuickRes", f"{e}")
    
if __name__ == "__main__":
    App = Application()
    App.mainloop()