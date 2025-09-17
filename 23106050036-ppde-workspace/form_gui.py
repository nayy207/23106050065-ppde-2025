import tkinter as tk
from tkinter import messagebox

def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data")
        return

    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    jenis_kelamin = var_jk.get()

    if not nama or not nim or not jurusan:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("Data Tersimpan", hasil)

def reset_form():
    entry_nama.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    entry_jurusan.delete(0, tk.END)
    var_jk.set("L")
    var_check.set(0)

def on_enter(event):
    if submit_button['state'] == tk.NORMAL:
        submit_button.config(bg="lightblue")

def on_leave(event):
    submit_button.config(bg="SystemButtonFace")


def submit_shortcut(event=None):
    if submit_button["state"] == tk.NORMAL:
        submit_data()

def validate_form(*args):
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_nim.get().strip() != ""
    setuju_valid = var_setuju.get() == 1
    if nama_valid and nim_valid and jurusan_valid and setuju_valid:
        submit_button.config(state=tk.NORMAL)
    else:
        submit_button.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Form Biodata Mahasiswa")
window.configure(bg="pink")

menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)


window.minsize(500, 400)

# var untuk entry
var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()
var_setuju = tk.IntVar()

file_menu = tk.Menu(master=menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)

current_font = "Consolas"
current_font_size = 15

main_frame = tk.Frame(window, padx=20, pady=20, bg="lightgreen")
main_frame.pack(fill=tk.BOTH, expand=True)

for i in range(2):
    main_frame.columnconfigure(i, weight=1)

frame_input = tk.Frame(main_frame, padx=10, pady=10, borderwidth=2, relief=tk.GROOVE)
frame_input.grid(row=1, column=0, columnspan=2, sticky="nsew")

for i in range(2):
    frame_input.columnconfigure(i, weight=1)

# Judul
label_judul = tk.Label(
    main_frame,
    text="Form Biodata Mahasiswa",
    font=(current_font, current_font_size, "bold"),
    bg="lightgreen"
)
label_judul.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

# Label + Entry Nama
label_nama = tk.Label(frame_input, text="Nama", font=(current_font, current_font_size, "bold"))
label_nama.grid(row=0, column=0, sticky="w", pady=5)

entry_nama = tk.Entry(frame_input, textvariable=var_nama, font=(current_font, current_font_size))
entry_nama.grid(row=0, column=1, sticky="ew", pady=5)

# Label + Entry NIM
label_nim = tk.Label(frame_input, text="NIM", font=(current_font, current_font_size, "bold"))
label_nim.grid(row=1, column=0, sticky="w", pady=5)

entry_nim = tk.Entry(frame_input, textvariable=var_nim, font=(current_font, current_font_size))
entry_nim.grid(row=1, column=1, sticky="ew", pady=5)

# Label + Entry Jurusan
label_jurusan = tk.Label(frame_input, text="Jurusan", font=(current_font, current_font_size, "bold"))
label_jurusan.grid(row=2, column=0, sticky="w", pady=5)

label_alamat = tk.Label(master=frame_input, text="Alamat:", font=(current_font,current_font_size))
label_alamat.grid(row=3,column=0,sticky="NW",pady=2)

entry_jurusan = tk.Entry(frame_input, textvariable=var_jurusan, font=(current_font, current_font_size))
entry_jurusan.grid(row=2, column=1, sticky="ew", pady=5)

# Jenis Kelamin
label_jk = tk.Label(frame_input, text="Jenis Kelamin", font=(current_font, current_font_size, "bold"))
label_jk.grid(row=4, column=0, sticky="w", pady=5)

# frame untuk jenis kelamin

frame_jk = tk.Frame(frame_input)
frame_jk.grid(row=4, column=1, sticky="w")

# frame untuk alamat

frame_alamat = tk.Frame(frame_input)
frame_alamat.grid(row=3,column=1,pady=2)

var_jk = tk.StringVar(value="L")
tk.Radiobutton(frame_jk, text="L", variable=var_jk, value="L").pack(side=tk.LEFT)
tk.Radiobutton(frame_jk, text="P", variable=var_jk, value="P").pack(side=tk.LEFT)

var_check = tk.IntVar()
checkbutton = tk.Checkbutton(
    frame_input,
    text="Saya setuju atas term and service",
    variable=var_setuju,
    onvalue=1, offvalue=0,
    command=validate_form
)
checkbutton.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

# scrollbar untuk alamat
scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

# isi richtextbox
text_alamat = tk.Text(master=frame_alamat,height=5,width=28,font=(current_font,current_font_size))
text_alamat.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
scrollbar_alamat.config(command=text_alamat.yview)


# Tombol
button_frame = tk.Frame(frame_input)
button_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

submit_button = tk.Button(button_frame, text="Kirim Data", font=(current_font, current_font_size), command=submit_data)
submit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

submit_button.config(state=tk.DISABLED)

reset_button = tk.Button(button_frame, text="Reset", font=(current_font, current_font_size), command=reset_form)
reset_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)

submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_jurusan.bind("<Return>", submit_shortcut)



window.mainloop()
