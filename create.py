import tkinter as tk
from tkinter import ttk
import logging
import os
import shutil
import re
from datetime import datetime
import json
import xlwings as xw

# Konfiguration für das Logging
logging.basicConfig(
    level=logging.INFO,
    filename="create.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.basicConfig(
    level=logging.DEBUG,
    filename="debug_create.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


#config openypxl
#os.startfile("Hardware-structur and testing protocol.xlsx")
workbook = xw.Book("Hardware-structur and testing protocol.xlsx")
worksheet = workbook.sheets['Hardware-concept']
worksheet["C15"].value = "test"
# Funktionen
def log_message(message):
    logging.info(message)
    print(f"{message}")


def log_message_debug(message):
    logging.debug(message)
    print(f"log: {message}")


def kopiere_ordner(quelle, ziel):
    logging.debug(f"kopiere {quelle} zu {ziel}")
    if not os.path.exists(ziel):
        os.makedirs(ziel)
    for item in os.listdir(quelle):
        quellpfad = os.path.join(quelle, item)
        zielpfad = os.path.join(ziel, item)
        if os.path.isdir(quellpfad):
            kopiere_ordner(quellpfad, zielpfad)
        else:
            shutil.copy2(quellpfad, zielpfad)


def replace_text(file_path, old_text, new_text):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        new_content = content.replace(old_text, new_text)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        log_message_debug(
            f" '{old_text}' successfully replaced with '{new_text}' in '{file_path}'."
        )
    except Exception as e:
        log_message_debug(f"Error by replace text in {file_path}: {e}")


def delete_text(file_path, text_to_delete):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        new_content = content.replace(text_to_delete, "")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        log_message_debug(f"'{text_to_delete}' successfully deleted in {file_path}.")
    except Exception as e:
        log_message_debug(f"Error by deleting text in {file_path}: {e}")


def delete_text_block(file_path, pattern):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Verwende einen regulären Ausdruck, um den gesamten Block zu finden und zu löschen
        new_content = re.sub(pattern, "", content, flags=re.DOTALL)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        log_message_debug(
            f"Block matching '{pattern}' successfully deleted in {file_path}."
        )
    except Exception as e:
        log_message_debug(f"Error by deleting text block in {file_path}: {e}")


# Hauptklasse
class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Editor")
        self.tab_control = ttk.Notebook(root)

        self.buttons_tab = ttk.Frame(self.tab_control)
        self.led_tab = ttk.Frame(self.tab_control)
        self.status_tab = ttk.Frame(self.tab_control)
        self.user_info_tab = ttk.Frame(self.tab_control)
        self.zyklus_tab = ttk.Frame(self.tab_control)
        self.blink_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.user_info_tab, text="Benutzer Info")
        self.tab_control.add(self.buttons_tab, text="Buttons")
        self.tab_control.add(self.led_tab, text="LEDs")
        self.tab_control.add(self.status_tab, text="Status")
        self.tab_control.add(self.zyklus_tab, text="Zyklus")
        self.tab_control.add(self.blink_tab, text="Blink")

        self.tab_control.pack(expand=1, fill="both")

        self.create_buttons()
        self.create_leds()
        self.create_buttons_tab()
        self.create_led_tab()
        self.create_status_tab()
        self.create_user_info_tab()
        self.create_zyklus_tab()
        self.create_blink_tab()

    def create_buttons(self):
        for i in range(8):
            setattr(self, f"check_var_posedge_s{i}", tk.IntVar(value=0))
            setattr(self, f"check_var_static_s{i}", tk.IntVar(value=0))
            setattr(self, f"check_var_negedge_s{i}", tk.IntVar(value=0))
            setattr(self, f"var_name_entry_s{i}", tk.Entry(self.buttons_tab))
        
        

    def create_leds(self):
        self.LED_status_vars = [tk.IntVar(value=0) for _ in range(8)]
        self.var_name_LED_entries = [tk.Entry(self.led_tab) for _ in range(8)]

    def create_buttons_tab(self):
        headings = ["Button", "Variablenname", "PosEdge", "Static", "NegEdge"]
        for col, heading in enumerate(headings):
            tk.Label(self.buttons_tab, text=heading).grid(row=0, column=col)
        for i in range(8):
            self.create_row_button(
                f"S{i}",
                i + 1,
                getattr(self, f"check_var_posedge_s{i}"),
                getattr(self, f"check_var_static_s{i}"),
                getattr(self, f"check_var_negedge_s{i}"),
                getattr(self, f"var_name_entry_s{i}"),
            )

    def create_led_tab(self):
        headings = ["LED", "Variablenname", "Status"]
        for col, heading in enumerate(headings):
            tk.Label(self.led_tab, text=heading).grid(row=0, column=col)
        for i in range(8):
            self.create_row_led(
                f"LED{i}", i + 1, self.LED_status_vars[i], self.var_name_LED_entries[i]
            )

    def create_status_tab(self):
        self.status_vars = [tk.StringVar() for _ in range(9)]
        self.status_entries = [
            tk.Entry(self.status_tab, textvariable=var) for var in self.status_vars
        ]
        self.start_status_var = tk.StringVar(value=1)
        tk.Label(self.status_tab, text="Status Name").grid(
            row=0, column=0, padx=5, pady=5
        )
        tk.Label(self.status_tab, text="Startstatus").grid(
            row=0, column=1, padx=5, pady=5
        )
        for i in range(9):
            self.status_entries[i].grid(row=i + 1, column=0, padx=5, pady=5)
            tk.Radiobutton(
                self.status_tab,
                text=f"Status {i+1}",
                variable=self.start_status_var,
                value=f"Status {i+1}",
            ).grid(row=i + 1, column=1, padx=5, pady=5)

    def create_row_button(
        self, label_text, row, var_posedge, var_static, var_negedge, var_name_entry
    ):
        tk.Label(self.buttons_tab, text=label_text).grid(row=row, column=0)
        var_name_entry.grid(row=row, column=1)
        tk.Checkbutton(self.buttons_tab, variable=var_posedge).grid(row=row, column=2)
        tk.Checkbutton(self.buttons_tab, variable=var_static).grid(row=row, column=3)
        tk.Checkbutton(self.buttons_tab, variable=var_negedge).grid(row=row, column=4)
    
    def create_row_led(self, label_text, row, led_status_var, var_name_entry):
        tk.Label(self.led_tab, text=label_text).grid(row=row, column=0)
        var_name_entry.grid(row=row, column=1)
        tk.Checkbutton(self.led_tab, variable=led_status_var, text="On").grid(
            row=row, column=2
        )

    def create_user_info_tab(self):
        # Erstelle die Beschriftungen und Eingabefelder
        labels = ["Vorname:", "Nachname:", "Datum:", "Kandidatennummer:"]
        self.user_info_vars = [tk.StringVar() for _ in range(4)]
        
        heutiges_datum = datetime.now().strftime("%d.%m.%Y")
        self.user_info_vars[2].set(heutiges_datum)

        for i, label in enumerate(labels):
            tk.Label(self.user_info_tab, text=label).grid(row=i, column=0, sticky="e")
            tk.Entry(self.user_info_tab, textvariable=self.user_info_vars[i]).grid(
                row=i, column=1
            )

    def create_zyklus_tab(self):
        labels = ["Zyklus", "Zyklus1:", "Zyklus2"]
        self.user_zyklus_vars = [tk.StringVar() for _ in range(3)]
        self.user_zyklus_vars_used = [tk.StringVar() for _ in range(3)]
        
        tk.Label(self.zyklus_tab, text="Name:").grid(row=0, column=1)
        tk.Label(self.zyklus_tab, text="Used for:").grid(row=0, column=2)
        
        for i, label in enumerate(labels):
            tk.Label(self.zyklus_tab, text=label).grid(row=i+1, column=0, sticky="e")
            tk.Entry(self.zyklus_tab, textvariable=self.user_zyklus_vars[i]).grid(
                row=i+1, column=1
            )
            tk.Entry(self.zyklus_tab, textvariable=self.user_zyklus_vars_used[i]).grid(
                row=i+1, column=2
            )

    def create_blink_tab(self):

        # Titel für die Spalten
        tk.Label(self.blink_tab, text="Name").grid(row=0, column=1, sticky="e")
        tk.Label(self.blink_tab, text="Hz").grid(row=0, column=2, sticky="e")
        tk.Label(self.blink_tab, text="verh.").grid(row=0, column=3, sticky="e")

        labels = ["Blink", "Blink1", "Blink2"]
        self.user_blink_vars = [tk.StringVar() for _ in range(3)]
        self.user_hz_vars = [tk.StringVar() for _ in range(3)]
        self.user_toff_vars = [tk.StringVar() for _ in range(3)]
        self.user_ton_vars = [tk.StringVar() for _ in range(3)]

        for i, label in enumerate(labels):
            
            tk.Label(self.blink_tab, text=label).grid(row=i + 1, column=0, sticky="e")
            tk.Entry(
                self.blink_tab, textvariable=self.user_blink_vars[i], width=20
            ).grid(row=i + 1, column=1)

            tk.Entry(self.blink_tab, textvariable=self.user_hz_vars[i], width=5).grid(
                row=i + 1, column=2
            )

            tk.Entry(self.blink_tab, textvariable=self.user_toff_vars[i], width=5).grid(
                row=i + 1, column=3
            )
            
            tk.Label(self.blink_tab, text="  :").grid(row=i + 1, column=4)
            tk.Entry(self.blink_tab, textvariable=self.user_ton_vars[i], width=5).grid(
                row=i + 1, column=5
            )

        create_button = tk.Button(
            self.blink_tab,
            text="Create",
            bg="blue",
            fg="white",
            command=self.on_create_click,
        )
        create_button.grid(row=9, column=5, pady=10, padx=10)
        
        
        save_button = tk.Button(
            self.blink_tab,
            text="Save",
            bg="blue",
            fg="white",
            command=self.save,
        )
        save_button.grid(row=10, column=4, pady=10, padx=10)
        
        load_button = tk.Button(
            self.blink_tab,
            text="Load",
            bg="blue",
            fg="white",
            command=self.save,
        )
        load_button.grid(row=10, column=5, pady=10, padx=10)

    def save(self):
        self.user_info_vars[0].set("Thomas")
        



    def on_create_click(self):
        # copy folder
        kopiere_ordner("Code_example", "Code")
        kopiere_ordner("Structogram_example", "Structogram")

        # Buttons
        log_message("Creating")
        self.create_button()

        # Verarbeite LEDs
        self.create_LED()

        # Verarbeite Status
        self.create_status()
        
        #editing for user info
        self.create_user_info()
        
        #verarbeite Zyklus
        self.create_zyklus()
        
        # Blink-Konfigurationen verarbeiten
        self.create_blink()
        
        #save excel
        workbook.save()
        log_message("Erstellung abgeschlossen")
        
    def create_LED(self):
        for i in range(8):
            led_status = self.LED_status_vars[i].get()
            led_name_entry = self.var_name_LED_entries[i].get()
            if led_name_entry:
                worksheet.range(f'N{20-i}').value = led_name_entry
                if led_status:
                    replace_text(
                        "Code/main.c", f"led_{i}_init", f"{led_name_entry}"
                    )
                    replace_text("Code/main.c", f"statled{i}", "ON")
                    replace_text("Structogram/1_main.nsd", f"statled_{i}", "ON")
                else:
                    replace_text(
                        "Code/main.c", f"led_{i};", f"{led_name_entry}"
                    )
                    replace_text("Code/main.c", f"statled{i}", "OFF")
                    replace_text("Structogram/1_main.nsd", f"statled_{i}", "OFF")
                
                replace_text("Structogram/1_main.nsd", f"led_{i}", f"{led_name_entry}")
                if not (i == 0 or i == 7):
                    replace_text(
                        "Code/main.c",
                        f"copyOutput = copyOutput | (led_{i}<<{i});	//LED {i}",
                        f"copyOutput = copyOutput | ({led_name_entry}<<{i});	//LED {i}",
                    )
                elif(i == 0):
                    replace_text(
                        "Code/main.c",
                        f"copyOutput = copyOutput | led_0;	//LED 0",
                        f"copyOutput = copyOutput | {led_name_entry};	//LED 0",
                    )
                else:
                    replace_text(
                        "Code/main.c",
                        f"copyOutput = led_7<<7;	//LED 7",
                        f"copyOutput = {led_name_entry}<<7;	//LED 7",
                    )
                if(led_status):
                    var_led_status_over = "ON"
                else:
                    var_led_status_over = "OFF"
                replace_text(
                    "Structogram/1_main.nsd",
                    f",&#34;led_{i} := statled{i}  //LED{i}&#34;",
                    f",&#34;{led_name_entry} := {var_led_status_over}  //LED{i}&#34;",
                )

                replace_text(
                    "Structogram/4_process.nsd",
                    f",&#34;led_{i} := OFF&#34;",
                    f",&#34;{led_name_entry} := {var_led_status_over}&#34;",
                )
                
                if i == 7:
                    replace_text(
                        "Structogram/5_writeOutput.nsd",
                        f",&#34;copyOutput := led_{i} &#60;&#60; bit{i}  //LED {i}&#34;",
                        f",&#34;copyOutput := {led_name_entry} &#60;&#60; bit{i}  //LED {i}&#34;",
                    )
                elif(i == 0):
                    replace_text(
                        "Structogram/5_writeOutput.nsd",
                        f",&#34;copyOutput := copyOutput bitweise or led_0            //LED 0&#34;",
                        f",&#34;copyOutput := copyOutput bitweise or {led_name_entry}            //LED 0&#34;",
                    )
                else:
                    replace_text(
                        "Structogram/5_writeOutput.nsd",
                        f",&#34;copyOutput := copyOutput bitweise or (led_{i} &#60;&#60; bit{i})  //LED {i}&#34;",
                        f",&#34;copyOutput := copyOutput bitweise or ({led_name_entry} &#60;&#60; bit{i})  //LED {i}&#34;",
                    )
                replace_text("Code/main.c", "led_{i}", f"{led_name_entry}")
            else:
                delete_text("Structogram/1_main.nsd", f",&#34;led_{i} := statled_{i}  //LED{i}&#34;")
                delete_text("Code/main.c", f"uint8_t led_{i}_init = statled{i};	//LED{i}")
                delete_text("Code/main.c", f"led_{i} = statled{i};")
                delete_text("Code/main.c", f"uint8_t led_{i} = statled{i};	//LED{i}")
                delete_text("Structogram/1_main.nsd", f",&#34;led_{i} := statled{i}  //LED{i}&#34;")
                delete_text("Structogram/4_process.nsd", f",&#34;led_{i} := OFF&#34;")
                if i == 7:
                    delete_text(
                        "Structogram/5_writeOutput.nsd",
                        f",&#34;copyOutput := led_{i} &#60;&#60; bit{i}  //LED {i}&#34;",
                    )
                else:
                    if i == 0:
                        delete_text("Structogram/5_writeOutput.nsd", f",&#34;copyOutput := copyOutput bitweise or led_0            //LED 0&#34;",)
                    else:
                        delete_text("Structogram/5_writeOutput.nsd",f",&#34;copyOutput := copyOutput bitweise or (led_{i} &#60;&#60; bit{i})  //LED {i}&#34;")

                if i == 0:
                    delete_text("Code/main.c", f"copyOutput = copyOutput | led_0;	//LED 0")
                elif(i == 7):
                    delete_text("Code/main.c", f"copyOutput = led_7<<7;	//LED 7")
                else:
                    delete_text("Code/main.c", f"copyOutput = copyOutput | (led_{i}<<{i});	//LED {i}")

    def create_user_info(self):
        log_message("Erstellung user info")
        vorname = self.user_info_vars[0].get()
        nachname = self.user_info_vars[1].get()
        datum = self.user_info_vars[2].get()
        kandidatennummer = self.user_info_vars[3].get()
        
        # Excel
        
        worksheet.range(f'E5').value = vorname
        worksheet.range(f'C5').value = nachname
        worksheet.range(f'P5').value = kandidatennummer
        
        
        replace_text("Code/main.c", "vorname", vorname)
        replace_text("Code/main.c", "nachname", nachname)
        replace_text("Code/main.c", "xx.xx.20xx", datum)
        replace_text("Code/main.c", "kannum", kandidatennummer)
        
        
        replace_text("Structogram/1_main.nsd", "vorname", vorname)
        replace_text("Structogram/1_main.nsd", "nachname", nachname)
        replace_text("Structogram/1_main.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/1_main.nsd", "kannum", kandidatennummer)
        
        
        replace_text("Structogram/2_initializing.nsd", "vorname", vorname)
        replace_text("Structogram/2_initializing.nsd", "nachname", nachname)
        replace_text("Structogram/2_initializing.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/2_initializing.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/3_readInput.nsd", "vorname", vorname)
        replace_text("Structogram/3_readInput.nsd", "nachname", nachname)
        replace_text("Structogram/3_readInput.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/3_readInput.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/4_process.nsd", "vorname", vorname)
        replace_text("Structogram/4_process.nsd", "nachname", nachname)
        replace_text("Structogram/4_process.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/4_process.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/5_writeOutput.nsd", "vorname", vorname)
        replace_text("Structogram/5_writeOutput.nsd", "nachname", nachname)
        replace_text("Structogram/5_writeOutput.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/5_writeOutput.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/6_blink.nsd", "vorname", vorname)
        replace_text("Structogram/6_blink.nsd", "nachname", nachname)
        replace_text("Structogram/6_blink.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/6_blink.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/7_blink1.nsd", "vorname", vorname)
        replace_text("Structogram/7_blink1.nsd", "nachname", nachname)
        replace_text("Structogram/7_blink1.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/7_blink1.nsd", "kannum", kandidatennummer)
        
        
        
        replace_text("Structogram/8_blink2.nsd", "vorname", vorname)
        replace_text("Structogram/8_blink2.nsd", "nachname", nachname)
        replace_text("Structogram/8_blink2.nsd", "xx.xx.20xx", datum)
        replace_text("Structogram/8_blink2.nsd", "kannum", kandidatennummer)

    def create_status(self):
        start_status_name = self.start_status_var.get()
        log_message(f"Startstatus: {start_status_name}")
        for i, status_var in enumerate(self.status_vars):
            status_name = status_var.get()
            if status_name:
                log_message(f"Status {i+1}: {status_name}")
                replace_text("Code/main.c", f"device_states{i+1}", status_name)
                replace_text(
                    "Structogram/1_main.nsd", f"device_states{i+1}", status_name
                )
                replace_text(
                    "Structogram/4_process.nsd", f"device_states{i+1}", status_name
                )
            else:
                delete_text("Code/main.c", f"#define device_states{i+1} {i+1}")
                delete_text_block("Code/main.c", f"case device_states{i+1}:.*?break;")
                delete_text("Structogram/1_main.nsd", f",&#34;device_states{i+1} {i+1}&#34;")
                delete_text("Structogram/4_process.nsd", f",&#34;device_states{i+1}&#34;")
                
                
    

        # Markiere den Startstatus speziell
        # Finde den Namen des Startstatus
        start_status_index = int(self.start_status_var.get().split(" ")[-1]) - 1
        start_status_name = self.status_vars[start_status_index].get()

        # Ersetze den Startstatus in den Dateien
        replace_text("Code/main.c", "start_state", start_status_name)
        replace_text("Structogram/1_main.nsd", "state_start", start_status_name)

        log_message(f"Startstatus: {start_status_name}")

    def create_zyklus(self):
        if(self.user_zyklus_vars[0].get()):
            replace_text("Code/main.c", f"get_Zyklus_name", f"get_{self.user_zyklus_vars[0].get()}")
            replace_text("Code/main.c", f"reset_Zyklus_name", f"reset_{self.user_zyklus_vars[0].get()}")
            replace_text("Code/main.c", f"use_case_Zyklus0", f"{self.user_zyklus_vars_used[0].get()}")

            replace_text("Structogram/1_main.nsd", f"get_Zyklus_name", f"get_{self.user_zyklus_vars[0].get()}")
            replace_text("Structogram/1_main.nsd", f"reset_Zyklus_name", f"reset_{self.user_zyklus_vars[0].get()}")
            replace_text("Structogram/1_main.nsd", f"use_case_Zyklus0", f"{self.user_zyklus_vars_used[0].get()}")

        else:
            delete_text("Code/main.c", f"#define get_Zyklus_name() get_Zyklus()         //use_case_Zyklus0")
            delete_text("Code/main.c", f"#define reset_Zyklus_name()  reset_Zyklus()	 //use_case_Zyklus0")

            delete_text("Structogram/1_main.nsd", ",&#34;get_Zyklus_Name() get_Zyklus() //use_case_Zyklus0&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;reset_Zyklus_Name() reset_Zyklus() //use_case_Zyklus0&#34;")


        if(self.user_zyklus_vars[1].get()):
            replace_text("Code/main.c", f"get_Zyklus1_name", f"get_{self.user_zyklus_vars[1].get()}")
            replace_text("Code/main.c", f"reset_Zyklus1_name", f"reset_{self.user_zyklus_vars[1].get()}")
            replace_text("Code/main.c", f"use_case_Zyklus1", f"{self.user_zyklus_vars_used[1].get()}")

            replace_text("Structogram/1_main.nsd", f"get_Zyklus1_name", f"get_{self.user_zyklus_vars[1].get()}")
            replace_text("Structogram/1_main.nsd", f"reset_Zyklus1_name", f"reset_{self.user_zyklus_vars[1].get()}")
            replace_text("Structogram/1_main.nsd", f"use_case_Zyklus1", f"{self.user_zyklus_vars_used[1].get()}")
            

        else:
            delete_text("Code/main.c", f"#define get_Zyklus1_name() get_Zyklus1()		//use_case_Zyklus1")
            delete_text("Code/main.c", f"#define reset_Zyklus1_name() reset_Zyklus1()	//use_case_Zyklus1")

            delete_text("Structogram/1_main.nsd", ",&#34;get_Zyklus1_Name() get_Zyklus1() //use_case_Zyklus1&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;reset_Zyklus1_Name() reset_Zyklus1() //use_case_Zyklus1&#34;")


        if(self.user_zyklus_vars[2].get()):
            replace_text("Code/main.c", f"get_Zyklus2_name", f"get_{self.user_zyklus_vars[2].get()}")
            replace_text("Code/main.c", f"reset_Zyklus2_name", f"reset_{self.user_zyklus_vars[2].get()}")
            replace_text("Code/main.c", f"use_case_Zyklus2", f"{self.user_zyklus_vars_used[2].get()}")

            replace_text("Structogram/1_main.nsd", f"get_Zyklus2_name", f"get_{self.user_zyklus_vars[2].get()}")
            replace_text("Structogram/1_main.nsd", f"reset_Zyklus2_name", f"reset_{self.user_zyklus_vars[2].get()}")
            replace_text("Structogram/1_main.nsd", f"use_case_Zyklus2", f"{self.user_zyklus_vars_used[2].get()}")

        else:
            delete_text("Code/main.c", f"#define get_Zyklus2_name() get_Zyklus2()		//use_case_Zyklus2")
            delete_text("Code/main.c", f"#define reset_Zyklus2_name() reset_Zyklus2()	//use_case_Zyklus2")

            delete_text("Structogram/1_main.nsd", ",&#34;get_Zyklus2_Name() get_Zyklus2() //use_case_Zyklus2&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;reset_Zyklus2_Name() reset_Zyklus2() //use_case_Zyklus2&#34;")

    def create_blink(self):
        log_message("Blink verarbeitung")
        if(self.user_blink_vars[0].get()):

            toff = int(round((1 / float(self.user_hz_vars[0].get()) * 1000) / (float(self.user_ton_vars[0].get()) + float(self.user_toff_vars[0].get())) * float(self.user_ton_vars[0].get()), 0))
            ton =int(round( (1 / float(self.user_hz_vars[0].get()) * 1000) / (float(self.user_ton_vars[0].get()) + float(self.user_toff_vars[0].get())) * float(self.user_toff_vars[0].get()), 0))

            replace_text("Code/main.c", f"#define name1_blink() blink(NewValueTon,NewValueToff) //in ms, Hz , :", f"#define {self.user_blink_vars[0].get()}() blink({ton},{toff}) //in ms, {self.user_hz_vars[0].get()}Hz , {self.user_toff_vars[0].get()}:{self.user_ton_vars[0].get()}")
            replace_text("Structogram/1_main.nsd", f"name1_blink() blink(NewValueTon,NewValueToff) //in ms, Hz , :", f"{self.user_blink_vars[0].get()}() blink({ton},{toff}) //in ms, {self.user_hz_vars[0].get()}Hz , {self.user_toff_vars[0].get()}:{self.user_ton_vars[0].get()}")

        else:
            delete_text("Code/main.c", f"#define name1_blink() blink(NewValueTon,NewValueToff) //in ms, Hz , :")
            delete_text("Code/main.c", f"#define getBlink() get_Zyklus()               //Used for blink")
            delete_text("Code/main.c", f"#define resetBlink() reset_Zyklus()           //Used for blink")
            delete_text("Code/main.c", "uint8_t blink(unsigned int tOn, unsigned int tOff);")

            delete_text("Structogram/1_main.nsd", ",&#34;name1_blink() blink(NewValueTon,NewValueToff) //in ms, Hz , :&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;getBlink() get_Zyklus()    //Used for blink&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;resetBlink() reset_Zyklus()  //Used for blink&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;blink(tOn, tOff)&#34;")
            
            delete_text_block("Code/main.c", "uint8_t blink *\([a-zA-Z_, ]+\)[ \t\n]*\{.*return[a-zA-Z _;\n\t]*\}")
            os.remove(r"Structogram/6_Blink.nsd")


        if(self.user_blink_vars[1].get()):

            toff = int(round((1 / float(self.user_hz_vars[1].get()) * 1000) / (float(self.user_ton_vars[1].get()) + float(self.user_toff_vars[1].get())) * float(self.user_ton_vars[1].get()), 0))
            ton =int(round( (1 / float(self.user_hz_vars[1].get()) * 1000) / (float(self.user_ton_vars[1].get()) + float(self.user_toff_vars[1].get())) * float(self.user_toff_vars[1].get()), 0))

            replace_text("Code/main.c", f"#define name2_blink() blink1(NewValueTon,NewValueToff) //in ms, Hz , :", f"#define {self.user_blink_vars[1].get()}() blink1({ton},{toff}) //in ms, {self.user_hz_vars[1].get()}Hz , {self.user_toff_vars[1].get()}:{self.user_ton_vars[1].get()}")
            replace_text("Structogram/1_main.nsd", f"name2_blink() blink1(NewValueTon,NewValueToff) //in ms, Hz , :", f"{self.user_blink_vars[1].get()}() blink1({ton},{toff}) //in ms, {self.user_hz_vars[1].get()}Hz , {self.user_toff_vars[1].get()}:{self.user_ton_vars[1].get()}")

        else:
            delete_text("Code/main.c", f"#define name2_blink() blink1(NewValueTon,NewValueToff) //in ms, Hz , :")
            delete_text("Code/main.c", f"#define getBlink1() get_Zyklus1()             //Used for blink 1")
            delete_text("Code/main.c", f"#define resetBlink1() reset_Zyklus1()         //Used for blink 1")
            delete_text("Code/main.c", "uint8_t blink1(unsigned int tOn, unsigned int tOff);")

            delete_text("Structogram/1_main.nsd", ",&#34;name2_blink() blink1(NewValueTon,NewValueToff) //in ms, Hz , :&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;getBlink1() get_Zyklus1()   //Used for blink1&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;resetBlink1() reset_Zyklus1()  //Used for blink1&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;blink1(tOn, tOff)&#34;")
            
            delete_text_block("Code/main.c", "uint8_t blink1 *\([a-zA-Z_, ]+\)[ \t\n]*\{.*return[a-zA-Z _;\n\t]*\}")
            os.remove(r"Structogram/7_Blink1.nsd")


        if(self.user_blink_vars[2].get()):
            toff = int(round((1 / float(self.user_hz_vars[2].get()) * 1000) / (float(self.user_ton_vars[2].get()) + float(self.user_toff_vars[2].get())) * float(self.user_ton_vars[2].get()), 0))
            ton =int(round( (1 / float(self.user_hz_vars[2].get()) * 1000) / (float(self.user_ton_vars[2].get()) + float(self.user_toff_vars[2].get())) * float(self.user_toff_vars[2].get()), 0))


            replace_text("Code/main.c", f"#define name3_blink() blink2(NewValueTon,NewValueToff) //in ms, Hz , :", f"#define {self.user_blink_vars[2].get()}() blink2({ton},{toff}) //in ms, {self.user_hz_vars[2].get()}Hz , {self.user_toff_vars[2].get()}:{self.user_ton_vars[2].get()}")
            replace_text("Structogram/1_main.nsd", f"name3_blink() blink2(NewValueTon,NewValueToff) //in ms, Hz , :", f"{self.user_blink_vars[2].get()}() blink2({ton},{toff}) //in ms, {self.user_hz_vars[2].get()}Hz , {self.user_toff_vars[2].get()}:{self.user_ton_vars[2].get()}")

        else:
            delete_text("Code/main.c", f"#define name3_blink() blink2(NewValueTon,NewValueToff) //in ms, Hz , :")
            delete_text("Code/main.c", f"#define resetBlink2() reset_Zyklus2() 		//Used for blink 2")
            delete_text("Code/main.c", f"#define getBlink2() get_Zyklus2()             //Used for blink 2")
            delete_text("Code/main.c", f"uint8_t blink2(unsigned int tOn, unsigned int tOff);")

            delete_text("Structogram/1_main.nsd", ",&#34;name3_blink() blink2(NewValueTon,NewValueToff) //in ms, Hz , :&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;getBlink2() get_Zyklus2()   //Used for blink2&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;resetBlink2() reset_Zyklus2()  //Used for blink2&#34;")
            delete_text("Structogram/1_main.nsd", ",&#34;blink2(tOn, tOff)&#34;")
            
            delete_text_block("Code/main.c", "uint8_t blink2 *\([a-zA-Z_, ]+\)[ \t\n]*\{.*return[a-zA-Z _;\n\t]*\}")
            os.remove(r"Structogram/8_Blink2.nsd")

    def create_button(self):
        
        
        
        
        
        for i in range(8):
            log_message("Buttons")
            # Zugriff auf die Zustände und den Namen für jede Reihe
            posedge_var = getattr(self, f"check_var_posedge_s{i}").get()
            negedge_var = getattr(self, f"check_var_negedge_s{i}").get()
            static_var = getattr(self, f"check_var_static_s{i}").get()
            var_name_entry = getattr(self, f"var_name_entry_s{i}").get()

            # Ausgabe der Konfiguration für jede Schaltfläche
            log_message(f"Konfiguration für Schaltfläche S{i}:")
            worksheet.range(f'C{20-i}').value = var_name_entry
            if posedge_var:
                log_message(f"  PosEdge Name: {var_name_entry}_PosEdge")
                replace_text(
                    "Structogram/3_readInput.nsd",
                    f"button_{i}_PosEdge",
                    f"{var_name_entry}_PosEdge",
                )
                replace_text(
                    "Structogram/1_main.nsd",
                    f"button_{i}_PosEdge",
                    f"{var_name_entry}_PosEdge",
                )
                replace_text(
                    "Code/main.c", f"button_{i}_PosEdge", f"{var_name_entry}_PosEdge"
                )
            else:
                if i == 0:
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;button_0_PosEdge := posEdge bitweise and MASK0            //button S0 PosEdge&#34;",
                    )
                else:
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;button_{i}_PosEdge := (posEdge bitweise and MASK{i}) &#62;&#62; bit0  //button S{i} PosEdge&#34;",
                    )
                delete_text(
                    "Structogram/1_main.nsd",
                    f",&#34;button_{i}_PosEdge := 0  //S{i}&#34;",
                )
                delete_text(
                    "Code/main.c", f"uint8_t button_{i}_PosEdge = 0;	//S{i}"
                )
                if i == 0:
                    delete_text(
                        "Code/main.c",
                        f"button_0_PosEdge = posEdge & MASK0;		//button S0 PosEdge",
                    )
                if i == 1:
                    delete_text(
                        "Code/main.c",
                        f"button_1_PosEdge = (posEdge & MASK1) >> 1;	//button S1 PosEdge",
                    )
                if i == 2:
                    delete_text(
                        "Code/main.c",
                        f"button_2_PosEdge = (posEdge & MASK2) >> 2;	//button S2 PosEdge",
                    )
                if i == 3:
                    delete_text(
                        "Code/main.c",
                        f"button_3_PosEdge = (posEdge & MASK3) >> 3;	//button S3 PosEdge",
                    )
                if i == 4:
                    delete_text(
                        "Code/main.c",
                        f"button_4_PosEdge = (posEdge & MASK4) >> 4;	//button S4 PosEdge",
                    )
                if i == 5:
                    delete_text(
                        "Code/main.c",
                        f"button_5_PosEdge = (posEdge & MASK5) >> 5;	//button S5 PosEdge",
                    )
                if i == 6:
                    delete_text(
                        "Code/main.c",
                        f"button_6_PosEdge = (posEdge & MASK6) >> 6;	//button S6 PosEdge",
                    )
                if i == 7:
                    delete_text(
                        "Code/main.c",
                        f"button_7_PosEdge = (posEdge & MASK7) >> 7;	//button S7 PosEdge",
                    )

            if negedge_var:
                log_message(f"  NegEdge Name: {var_name_entry}_NegEdge")
                replace_text(
                    "Structogram/3_readInp$ut.nsd",
                    f"button_{i}_NegEdge",
                    f"{var_name_entry}_NegEdge",
                )
                replace_text(
                    "Structogram/1_main.nsd",
                    f"button_{i}_NegEdge",
                    f"{var_name_entry}_NegEdge",
                )
                replace_text(
                    "Code/main.c", f"button_{i}_NegEdge", f"{var_name_entry}_NegEdge"
                )
            else:
                if i == 0:
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;button_0_NegEdge := negEdge bitweise and MASK0            //button S0 NegEdge&#34;",
                    )
                else:
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;button_{i}_NegEdge := (negEdge bitweise and MASK{i}) &#62;&#62; bit0  //button S{i} NegEdge&#34;",
                    )
                delete_text(
                    "Structogram/1_main.nsd",
                    f",&#34;button_{i}_NegEdge := 0  //S{i}&#34;",
                )
                delete_text(
                    "Code/main.c", f"uint8_t button_{i}_NegEdge = 0;	//S{i}"
                )
                if i == 0:
                    delete_text(
                        "Code/main.c",
                        f"button_0_NegEdge = negEdge & MASK0;		//button S0 NegEdge",
                    )
                if i == 1:
                    delete_text(
                        "Code/main.c",
                        f"button_1_NegEdge = (negEdge & MASK1) >> 1;	//button S1 NegEdge",
                    )
                if i == 2:
                    delete_text(
                        "Code/main.c",
                        "button_2_NegEdge = (negEdge & MASK2) >> 2;	//button S2 NegEdge",
                    )
                if i == 3:
                    delete_text(
                        "Code/main.c",
                        f"button_3_NegEdge = (negEdge & MASK3) >> 3;	//button S3 NegEdge",
                    )
                if i == 4:
                    delete_text(
                        "Code/main.c",
                        f"button_4_NegEdge = (negEdge & MASK4) >> 4;	//button S4 NegEdge",
                    )
                if i == 5:
                    delete_text(
                        "Code/main.c",
                        f"button_5_NegEdge = (negEdge & MASK5) >> 5;	//button S5 NegEdge",
                    )
                if i == 6:
                    delete_text(
                        "Code/main.c",
                        f"button_6_NegEdge = (negEdge & MASK6) >> 6;	//button S6 NegEdge",
                    )
                if i == 7:
                    delete_text(
                        "Code/main.c",
                        f"button_7_NegEdge = (negEdge & MASK7) >> 7;	//button S7 NegEdge",
                    )
            if static_var:
                log_message(f"  Static Name: {var_name_entry}")
                replace_text(
                    "Structogram/1_main.nsd", f"switch_{i}", f"{var_name_entry}"
                )
                replace_text(
                    "Structogram/3_readInput.nsd", f"switch_{i}", f"{var_name_entry}"
                )
                replace_text("Code/main.c", f"switch_{i}", f"{var_name_entry}")
            else:
                delete_text(
                    "Structogram/1_main.nsd", f",&#34;switch_{i} := 0  //S{i}&#34;"
                )
                if(i== 0):
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;switch_0 := copyInput bitweise and MASK0           //button S0&#34;",
                    )
                else:
                    delete_text(
                        "Structogram/3_readInput.nsd",
                        f",&#34;switch_{i} := (copyInput bitweise and MASK{i}) &#62;&#62; bit0  //button S{i}&#34;",
                    )
                delete_text("Code/main.c", f"uint8_t switch_{i} = 0;	//S{i}")
                if i == 0:
                    delete_text(
                        "Code/main.c", f"switch_0 = copyInput & MASK0;	   //button S0"
                    )
                if i == 1:
                    delete_text(
                        "Code/main.c",
                        f"switch_1 = (copyInput & MASK1) >> 1;   //button S1",
                    )
                if i == 2:
                    delete_text(
                        "Code/main.c",
                        "switch_2 = (copyInput & MASK2) >> 2;   //button S2",
                    )
                if i == 3:
                    delete_text(
                        "Code/main.c",
                        f"switch_3 = (copyInput & MASK3) >> 3;   //button S3",
                    )
                if i == 4:
                    delete_text(
                        "Code/main.c",
                        f"switch_4 = (copyInput & MASK4) >> 4;   //button S4",
                    )
                if i == 5:
                    delete_text(
                        "Code/main.c",
                        f"switch_5 = (copyInput & MASK5) >> 5;   //button S5",
                    )
                if i == 6:
                    delete_text(
                        "Code/main.c",
                        f"switch_6 = (copyInput & MASK6) >> 6;   //button S6",
                    )
                if i == 7:
                    delete_text(
                        "Code/main.c",
                        f"switch_7 = (copyInput & MASK7) >> 7;   //button S7",
                    )
            log_message("-" * 50)
        # end button


if (__name__ == "__main__"):
    root = tk.Tk()
    app = FileEditorApp(root)
    root.mainloop()
