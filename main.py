import customtkinter
from customtkinter import filedialog
import ctypes
import os
from CTkMessagebox import CTkMessagebox

# Needed data
class cod_settings:
    home_directory = os.path.expanduser("~")
    cod_path = os.path.join(home_directory, "Documents", "Call of Duty", "players", "s.1.0.cod24.txt")
    
    aspectratio = "AspectRatio@0;19775;7764 = "
    displaymode = "DisplayMode@0;22564;11445 = "
    resolution = "Resolution@0;56178;35888 = "

# Application GUI
class App(customtkinter.CTk):
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green") 

    def __init__(self):
        super().__init__()

        self.title("QR")
        self.geometry(f"{310}x{240}")
        
        self.watermark_label = customtkinter.CTkLabel(master=self, text=cod_settings.cod_path, font=("Roboto", 9), text_color="#383838")
        self.watermark_label.place(relx=0.5, rely=0.05, anchor="center")

        self.title_label = customtkinter.CTkLabel(master=self, text="QuickRes", font=("Roboto", 20))
        self.title_label.place(relx=0.5, rely=0.2, anchor="center")

        self.title_label_desc = customtkinter.CTkLabel(master=self, text="Custom resolutions made easy", font=("Roboto", 10))
        self.title_label_desc.place(relx=0.5, rely=0.3, anchor="center")
        
        self.test = customtkinter.CTkLabel(master=self, text="X", font=("Roboto", 10))
        self.test.place(relx=0.5, rely=0.485, anchor="center")

        self.x_res_input = customtkinter.CTkTextbox(master=self, corner_radius=5, width=60, height=1)
        self.x_res_input.place(relx=0.37, rely=0.48, anchor="center")
        self.x_res_input.insert("0.0", "1920")

        self.y_res_input = customtkinter.CTkTextbox(master=self, corner_radius=5, width=60, height=1)
        self.y_res_input.place(relx=0.63, rely=0.48, anchor="center")
        self.y_res_input.insert("0.0", "1080")

        displaytype_var = customtkinter.StringVar(value="Fullscreen")
        self.displaytype_combo = customtkinter.CTkComboBox(master=self, values=["Fullscreen", "Fullscreen borderless window"], corner_radius=5, height=22, variable=displaytype_var)
        self.displaytype_combo.place(relx=0.5, rely=0.6, anchor="center")

        self.apply_res_btn = customtkinter.CTkButton(master=self, text="Apply", corner_radius=5, height=22, command = cod.apply_settings)
        self.apply_res_btn.place(relx = 0.5, rely = 0.71, anchor="center")

        self.watermark_label = customtkinter.CTkLabel(master=self, text="Developed by boog <3", font=("Roboto", 10), text_color="#383838")
        self.watermark_label.place(relx=0.17, rely=0.97, anchor="center")
        self.version_label = customtkinter.CTkLabel(master=self, text="v1.0.1", font=("Roboto", 10), text_color="#383838")
        self.version_label.place(relx=0.94, rely=0.97, anchor="center")

# COD settings functions
class cod:
    def apply_settings():
        cod.set_res()
        cod.set_displaytype()
        CTkMessagebox(message="Settings have been applied.", icon="check", option_1="Okay")

    def set_res():
        x = app.x_res_input.get("0.0", "end")
        y = app.y_res_input.get("0.0", "end")
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

    def set_displaytype():
        displaymode_text_replacement = cod_settings.displaymode + f" = {app.displaytype_combo.get()}"
        windows.edit_txt(cod_settings.cod_path, cod_settings.displaymode, displaymode_text_replacement)

# Windows functions (thank you chat-gpt for the monitor res function <3)
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
            CTkMessagebox(title="Error", message=f"Could not change screen resolution! ", icon="cancel")

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
            CTkMessagebox(title="Error", message="Could not find path.", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Their was an error! {e}", icon="cancel")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
