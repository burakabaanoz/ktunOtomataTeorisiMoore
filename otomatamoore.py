import tkinter as tk
from tkinter import ttk

def update_entries():
    for widget in frame.winfo_children():
        widget.destroy()

    row_count = row_scale.get()
    letters = letters_entry.get().strip().split(',')
    letters = [letter.strip() for letter in letters if letter]
    letter_count = len(letters)
    output_letters = output_letters_entry.get().strip().split(',')
    output_letters = [letter.strip() for letter in output_letters if letter]
    output_letters_count = len(output_letters)

    if letter_count == 0 or output_letters_count == 0:
        return

    column_count = letter_count + 2
    canvas.config(width=max(300, column_count * 80)) 

    if row_count > 0:
        tk.Label(frame, text="İlk Durum", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Dönüşüm Tablosu", font=("Arial", 10, "bold")).grid(row=0, column=1, columnspan=column_count - 2, padx=5, pady=5)
        tk.Label(frame, text="Çıktı", font=("Arial", 10, "bold")).grid(row=0, column=column_count - 1, padx=5, pady=5)

        for j, letter in enumerate(letters):
            tk.Label(frame, text=f"{letter} girişi", font=("Arial", 9)).grid(row=1, column=j + 1, padx=5, pady=5)

    for i in range(2, row_count + 2):
        for j in range(column_count):
            if j == 0:
                tk.Label(frame, text=f"q{(i - 2) % 10}", font=("Arial", 9)).grid(row=i, column=j, padx=5, pady=5)
            elif j == column_count - 1:
                output_combobox = ttk.Combobox(frame, values=output_letters, state="readonly", width=10)
                output_combobox.grid(row=i, column=j, padx=5, pady=5)
                output_combobox.set("Çıktı Seçin")
            else:
                entry = ttk.Combobox(frame, values=[f"q{k}" for k in range(row_count)], state="readonly", width=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.set("Durum Seçin")

def calculate_values():
    row_count = row_scale.get()
    letters = letters_entry.get().strip().split(',')
    letters = [letter.strip() for letter in letters if letter]
    output_letters = output_letters_entry.get().strip().split(',')
    output_letters = [letter.strip() for letter in output_letters if letter]
    outputs = []
    matris = [[0] * row_count for _ in range(row_count)]
    i, sayac, combobox_index = 0, 0, 0
    son = False

    for entry in frame.winfo_children():
        if isinstance(entry, ttk.Combobox):
            selected_value = entry.get()
            try:
                entry_value_index = entry['values'].index(selected_value)
                if son:
                    outputs.append(output_letters[entry_value_index])
                    break
                if combobox_index == len(letters):
                    outputs.append(output_letters[entry_value_index])
                    sayac, combobox_index = 0, 0
                    continue
                if i < row_count:
                    matris[i][entry_value_index] = letters[sayac]
                sayac += 1
                if sayac == len(letters):
                    i += 1
                if i >= row_count:
                    son = True
                    continue
                combobox_index += 1
            except ValueError:
                print(f"Invalid selection '{selected_value}' in combobox.")

    baslangic = "  " + "  ".join(input_entry.get())
    sonuc, states, secim, sayac = [], [], input_entry.get(), 0
    bulundu = False
    i = j = 0
    sonuc.append(outputs[0])
    states.append("q0")
    while i < row_count:
        if sayac >= len(secim):
            break
        while j < row_count:
            bulundu = False
            if sayac >= len(secim):
                break
            if secim[sayac] == matris[i][j]:
                sayac += 1
                i, j = j, 0
                sonuc.append(outputs[i])
                states.append(f"q{i}")
                bulundu = True
            if not bulundu:
                j += 1
        i += 1

    Baslangiclabel2.config(text="    " + baslangic)
    Sonuclabel2.config(text="  " + "  ".join(sonuc))
    Statelabel2.config(text=" " + " ".join(states))

# Main Window
root = tk.Tk()
root.title("Moore Makinası")

# UI Elements
Baslangiclabel = tk.Label(root, text="Input Metni : ")
Baslangiclabel.pack(side=tk.TOP, anchor='nw', padx=20,pady=30)

Baslangiclabel2 = tk.Label(root, text=" ", font=("Arial", 16))
Baslangiclabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

Sonuclabel = tk.Label(root, text="Çıkış Metni : ")
Sonuclabel.pack(side=tk.TOP, anchor='nw', padx=20, pady=0) 
Sonuclabel2 = tk.Label(root, text="", font=("Arial", 16))
Sonuclabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

Statelabel = tk.Label(root, text="State Metni : ")
Statelabel.pack(side=tk.TOP, anchor='nw', padx=20, pady=30)
Statelabel2 = tk.Label(root, text="", font=("Arial", 16))
Statelabel2.pack(side=tk.TOP, anchor='nw', padx=60, pady=0)

letters_entry_label = tk.Label(root, text="Harfleri (a, b, c, d) girin:")
letters_entry_label.pack(side=tk.TOP, anchor='e', padx=10)
letters_entry = tk.Entry(root, width=20)
letters_entry.pack(side=tk.TOP, anchor='e', padx=10)

output_letters_label = tk.Label(root, text="Çıktı alfabesini girin (örn. x, y, z):")
output_letters_label.pack(side=tk.TOP, anchor='e', padx=10)
output_letters_entry = tk.Entry(root, width=20)
output_letters_entry.pack(side=tk.TOP, anchor='e', padx=10)

input_entry_label = tk.Label(root, text="Input Stringi Giriniz:")
input_entry_label.pack(side=tk.TOP, anchor='e', padx=10)
input_entry = tk.Entry(root, width=20)  
input_entry.pack(side=tk.TOP, anchor='e', padx=10)

row_scale_label = tk.Label(root, text="State Sayısını Giriniz")
row_scale_label.pack(side=tk.TOP, anchor='e', padx=10)
row_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
row_scale.pack(side=tk.TOP, anchor='e', padx=10)

update_button = tk.Button(root, text="Tabloyu Güncelle", command=update_entries)
update_button.pack(side=tk.TOP, anchor='e', padx=10, pady=(5, 10)) 

calculate_button = tk.Button(root, text="Hesapla", command=calculate_values)
calculate_button.pack(side=tk.TOP, anchor='e', padx=10, pady=(5, 10))

# Scrollable Frame
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame = scrollable_frame
update_entries()

root.mainloop()
