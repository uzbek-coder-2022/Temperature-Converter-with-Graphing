import os
import customtkinter as Ctk
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import pandas as pd
import matplotlib.pyplot as plt

selsiy, kelvin, farangeyt = None, None, None

root = Ctk.CTk()
root.geometry("520x400")
root.resizable(False, False)
root.title("Temperature Converter with Graphing")

dropdown = Ctk.CTkComboBox(root, values=['Selsiy', 'Farangeyt', 'Kelvin'])
dropdown.grid(row=1, column=1, padx=20, pady=20)

enter_value = Ctk.CTkEntry(root, placeholder_text="Haroratni kiriting:")
enter_value.grid(row=2, column=1, padx=20)

textbox1 = Ctk.CTkEntry(root)
textbox1.grid(row=2, column=2, padx=10)

textbox2 = Ctk.CTkEntry(root)
textbox2.grid(row=2, column=3, padx=20)


def temperature_save():
    file_path = "yillik_harorat_qaydnomasi.xlsx"
    
    if not os.path.exists(file_path):
        data = {
            'Sana': [],
            'Selsiy': [],
            'Kelvin': [],
            'Farangeyt': []
        }
        
        df = pd.DataFrame(data)
        
        df.to_excel(file_path, index=False)
    
    df = pd.read_excel(file_path)
    
    day_note = {
        'Sana': datetime.datetime.today().strftime('%d.%m.%Y'),
        'Selsiy': selsiy,
        'Kelvin': kelvin,
        "Farangeyt": farangeyt
        }
    
    df = pd.concat([df, pd.DataFrame([day_note])], ignore_index=True)
    df.to_excel('yillik_harorat_qaydnomasi.xlsx', index=False)
    
    for item in tree.get_children():
            tree.delete(item)
        
    for index, row in df.iterrows():
        tree.insert("", "end", text=list(row)[0], values=list(row)[1:]) 


save_button = Ctk.CTkButton(root, text="Saqlash", state="disabled", command=temperature_save)
save_button.grid(row=3, column=2, pady=20)

def draw_graphic():
    shkalalar = ['Selsiy', 'Kelvin', 'Farangeyt']
    file_path = "yillik_harorat_qaydnomasi.xlsx"
    
    if not os.path.exists(file_path):
        messagebox.showerror("Ogohlantirish", "Saqlangan harorat aniqlanmadi!")     
    
    df = pd.read_excel(file_path)

    harorat = [[row[1] for index, row in df.iterrows()], [row[2] for index, row in df.iterrows()], [row[3] for index, row in df.iterrows()]]

    plt.figure(figsize=(15, 10))

    for i in range(len(shkalalar)):
        plt.plot(range(1, df.shape[0]+1), harorat[i], marker='o', label=shkalalar[i])

    plt.title("Haroratning yillik o'zgarishi")
    plt.xlabel("Kun")
    plt.ylabel("Harorat")
    plt.xticks(range(1, df.shape[0]+1))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()    


draw_graphic_button = Ctk.CTkButton(root, text="Grafigini chizish")
draw_graphic_button.grid(row=3, column=3)

counter = 0

def convert():
    global selsiy, kelvin, farangeyt
    
    file_path = "yillik_harorat_qaydnomasi.xlsx"
    if not os.path.exists(file_path):
        data = {
            'Sana': [],
            'Selsiy': [],
            'Kelvin': [],
            'Farangeyt': []
        }
        
        df = pd.DataFrame(data)
        
        df.to_excel(file_path, index=False)
    
    df = pd.read_excel(file_path)
    if counter == 0:
        for index, row in df.iterrows():
            tree.insert("", "end", text=list(row)[0], values=list(row)[1:]) 
        return
          
    try:
        if len(enter_value.get()) == 0:
            messagebox.showerror("Ogohlantirish", "Siz harorat qiymatini kiritmadingiz!")
            return 
        temperature = float(enter_value.get())
        
        if dropdown.get() == 'Selsiy':
            selsiy = temperature
            farangeyt = temperature * 1.8 + 32
            textbox1.delete(0, 'end')
            textbox1.insert(0, "Farangeyt " + str(temperature * 1.8 + 32))
            kelvin = temperature + 273.15
            textbox2.delete(0, 'end')
            textbox2.insert(0, "Kelvin " + str(temperature + 273.15))
        elif dropdown.get() == 'Farangeyt':
            farangeyt = temperature
            selsiy = (temperature - 32) / 1.8
            textbox1.delete(0, 'end')
            textbox1.insert(0, "Selsiy " + str((temperature - 32) / 1.8))
            kelvin = (temperature - 32) / 1.8 + 273.15
            textbox2.delete(0, 'end')
            textbox2.insert(0, "Kelvin " + str((temperature - 32) / 1.8 + 273.15))
        elif dropdown.get() == 'Kelvin':
            kelvin = temperature
            selsiy = temperature - 273.15
            textbox1.delete(0, 'end')
            textbox1.insert(0, "Selsiy " + str(temperature - 273.15))
            farangeyt = (temperature - 273.15) * 1.8 + 32
            textbox2.delete(0, 'end')
            textbox2.insert(0, "Farangeyt " + str((temperature - 273.15) * 1.8 + 32))
        
        save_button.configure(state="normal")
                 
    except:
        messagebox.showerror("Ogohlantirish", "Siz harorat qiymatini to'g'ri kiritmadingiz!")


calc_button = Ctk.CTkButton(root, text="Hisoblash", command=convert)
calc_button.grid(row=3, column=1)

tree = ttk.Treeview(root)

tree['columns'] = ('one', 'two', 'three')
tree.column('#0', width=100)
tree.column('one', width=120)
tree.column('two', width=120)
tree.column('three', width=120)

tree.heading('#0', text='Sana', anchor=tk.W)
tree.heading('one', text='Selsiy', anchor=tk.W)
tree.heading('two', text='Kelvin', anchor=tk.W)
tree.heading('three', text='Farangeyt', anchor=tk.W)

tree.grid(row=4, column=1, columnspan=6, padx=20)

if counter == 0:
    convert()
    counter += 1

root.mainloop()