# Mengimpor library tkinter
import tkinter as tk

from tkinter import messagebox

def submit_data():
    # Cek checkbox
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return

    # Ambil data dari form
    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    alamat = text_alamat.get("1.0", tk.END).strip()  # Baris baru ini
    jenis_kelamin = var_jk.get()

    # Cek field kosong
    if not nama or not nim or not jurusan or not alamat:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    # Tampilkan hasil
    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}\nAlamat: {alamat}"
    # Tampilkan hasil di label
    label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")
    messagebox.showinfo("Data Tersimpan", hasil)

def validate_form(*args):
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    setuju_valid = var_setuju.get() == 1

    if nama_valid and nim_valid and jurusan_valid and setuju_valid:
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)

# Fungsi untuk efek hover saat mouse masuk
def on_enter(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg="lightblue")

# Fungsi untuk efek hover saat mouse keluar
def on_leave(event):
    btn_submit.config(bg="SystemButtonFace") # Warna default tombol

# Fungsi untuk shortcut tombol Enter
def submit_shortcut(event=None):
    # Memanggil fungsi submit_data jika tombol aktif
    if btn_submit['state'] == tk.NORMAL:
        submit_data()

# Fungsi untuk menu "Simpan Hasil"
def simpan_hasil():
    # Mengambil teks dari label_hasil (jika ada)
    hasil_tersimpan = label_hasil.cget("text")

    # Cek apakah ada hasil untuk disimpan
    if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
        messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
        return

    # Menyimpan ke file teks (simulasi)
    with open("biodata_tersimpan.txt", "w") as file:
        file.write(hasil_tersimpan)
    messagebox.showinfo("Info", "Data berhasil disimpan ke file 'biodata_tersimpan.txt'.")

# Fungsi untuk menu "Keluar"
def keluar_aplikasi():
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
        window.destroy()


# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela (lebar x tinggi)
window.geometry("500x600")

# Mencegah jendela dapat diubah ukurannya
window.resizable(True, True)

# Mengatur warna latar belakang jendela
window.configure(bg="skyblue")

# Membuat label judul
# label_judul = tk.Label(
#     master=window,
#     text="FORM BIODATA MAHASISWA",
#     font=("Arial", 16, "bold")
# )

# # Menampilkan label dengan pack
# label_judul.pack(pady=20)

# ganti ke frame
# Label untuk input nama
# label_nama = tk.Label(master=window, text="Nama Lengkap:", font=("Arial", 12))
# label_nama.pack(pady=5)

# # Entry untuk input nama
# entry_nama = tk.Entry(master=window, width=50)
# entry_nama.pack(pady=5)

# # Input NIM
# label_nim = tk.Label(master=window, text="NIM:", font=("Arial", 12))
# label_nim.pack(pady=5)
# entry_nim = tk.Entry(master=window, width=50)
# entry_nim.pack(pady=5)

# # Input Jurusan  
# label_jurusan = tk.Label(master=window, text="Jurusan:", font=("Arial", 12))
# label_jurusan.pack(pady=5)
# entry_jurusan = tk.Entry(master=window, width=50)
# entry_jurusan.pack(pady=5)

# Membuat frame utama
main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
# Konfigurasi responsive layout
main_frame.grid_columnconfigure(1, weight=1)
main_frame.columnconfigure(1, weight=1)

# Judul menggunakan grid
label_judul = tk.Label(master=main_frame, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"))
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# # Input nama dengan grid
# label_nama = tk.Label(master=main_frame, text="Nama Lengkap:", font=("Arial", 12))
# label_nama.grid(row=1, column=0, sticky="W", pady=5)

# entry_nama = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_nama.grid(row=1, column=1, pady=5)

# # Input NIM
# label_nim = tk.Label(master=main_frame, text="NIM:", font=("Arial", 12))
# label_nim.grid(row=2, column=0, sticky="W", pady=5)
# entry_nim = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_nim.grid(row=2, column=1, pady=5)

# # Input Jurusan
# label_jurusan = tk.Label(master=main_frame, text="Jurusan:", font=("Arial", 12))
# label_jurusan.grid(row=3, column=0, sticky="W", pady=5)
# entry_jurusan = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
# entry_jurusan.grid(row=3, column=1, pady=5)

# # Variabel untuk radiobutton jenis kelamin
# var_jk = tk.StringVar(value="Pria")

# # Label jenis kelamin
# label_jk = tk.Label(master=main_frame, text="Jenis Kelamin:", font=("Arial", 12))
# label_jk.grid(row=4, column=0, sticky="W", pady=5)

# # Frame untuk radiobutton
# frame_jk = tk.Frame(master=main_frame)
# frame_jk.grid(row=4, column=1, sticky="W")

# # Radiobutton pria dan wanita
# radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
# radio_pria.pack(side=tk.LEFT)

# radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
# radio_wanita.pack(side=tk.LEFT)

# # Variabel untuk checkbox
# var_setuju = tk.IntVar()

# # Checkbox persetujuan
# check_setuju = tk.Checkbutton(
#     master=main_frame,
#     text="Saya menyetujui pengumpulan data ini.",
#     variable=var_setuju,
#     font=("Arial", 10)
# )
# check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

# Frame khusus untuk input dengan border
frame_input = tk.Frame(master=main_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

# Variabel untuk real-time validation
var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()

# Aktifkan trace untuk validasi real-time
var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)


# Input nama di dalam frame_input
label_nama = tk.Label(master=frame_input, text="Nama Lengkap:", font=("Arial", 12))
label_nama.grid(row=0, column=0, sticky="W", pady=2)
entry_nama = tk.Entry(master=frame_input, width=30, font=("Arial", 12), textvariable=var_nama)
entry_nama.grid(row=0, column=1, pady=2)

# Input NIM di dalam frame_input
label_nim = tk.Label(master=frame_input, text="NIM:", font=("Arial", 12))
label_nim.grid(row=1, column=0, sticky="W", pady=2)
entry_nim = tk.Entry(master=frame_input, width=30, font=("Arial", 12), textvariable=var_nim)
entry_nim.grid(row=1, column=1, pady=2)

# Input Jurusan di dalam frame_input
label_jurusan = tk.Label(master=frame_input, text="Jurusan:", font=("Arial", 12))
label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
entry_jurusan = tk.Entry(master=frame_input, width=30, font=("Arial", 12), textvariable=var_jurusan)
entry_jurusan.grid(row=2, column=1, pady=2)

# Input alamat dengan Text widget
label_alamat = tk.Label(master=frame_input, text="Alamat:", font=("Arial", 12))
label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

# Frame untuk Text dan Scrollbar
frame_alamat = tk.Frame(master=frame_input, relief=tk.SUNKEN, borderwidth=1)
frame_alamat.grid(row=3, column=1, pady=2)

# Scrollbar untuk alamat
scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget untuk alamat
text_alamat = tk.Text(master=frame_alamat, height=5, width=28, font=("Arial", 12))
text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Hubungkan scrollbar dengan text
scrollbar_alamat.config(command=text_alamat.yview)
text_alamat.config(yscrollcommand=scrollbar_alamat.set)

var_jk = tk.StringVar(value="Pria")

# Jenis kelamin di dalam frame_input
label_jk = tk.Label(master=frame_input, text="Jenis Kelamin:", font=("Arial", 12))
label_jk.grid(row=4, column=0, sticky="W", pady=2)

frame_jk = tk.Frame(master=frame_input)
frame_jk.grid(row=4, column=1, sticky="W")

radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
radio_pria.pack(side=tk.LEFT)
radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
radio_wanita.pack(side=tk.LEFT)

var_setuju = tk.IntVar()


# Checkbox di dalam frame_input
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    command=validate_form
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

# Tombol submit
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit Biodata", 
    font=("Arial", 12, "bold"),
    command=submit_data,
    state=tk.DISABLED
)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

# Menghubungkan event Enter (mouse masuk) dan Leave (mouse keluar) ke button
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

label_hasil = tk.Label(master=main_frame, text="", font=("Arial", 12, "italic"), justify=tk.LEFT)
label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)


# Menghubungkan event <Return> (tombol Enter) ke fungsi shortcut
entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_jurusan.bind("<Return>", submit_shortcut)
text_alamat.bind("<Return>", submit_shortcut)

# Membuat menu bar utama
menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)

# Membuat menu "File"
file_menu = tk.Menu(master=menu_bar, tearoff=0)
# Menambahkan item-item ke dalam menu "File"
file_menu.add_command(label="Simpan Hasil", command=simpan_hasil)
file_menu.add_separator() # Menambahkan garis pemisah
file_menu.add_command(label="Keluar", command=keluar_aplikasi)


# Menambahkan menu "File" ke menu bar utama
menu_bar.add_cascade(label="File", menu=file_menu)


# Menjalankan event loop
window.mainloop()

