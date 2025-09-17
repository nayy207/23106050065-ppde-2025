# Ahmad Zidni Hidayat
# 23106050077
# Pemrograman Platform Desktop dan Embedded A

# Refactor code dari praktikum sebelumnya ke dalam paradigma OOP

import tkinter as tk
from tkinter import messagebox

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    def submit_data(self):
        # Cek checkbox
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        # Ambil data dari form
        nama = self.entry_nama.get()
        nim = self.entry_nim.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        # Cek field kosong
        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        # Tampilkan hasil
        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)

        # Tampilkan hasil di label
        self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()
    
    def simpan_hasil(self):
        hasil_tersimpan = self.label_hasil.cget("text")
        if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
            return

        with open("biodata_tersimpan.txt", "w") as file:
            file.write(hasil_tersimpan)
        messagebox.showinfo("Info", "Data berhasil disimpan ke file 'biodata_tersimpan.txt'.")

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.destroy()


    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()

        # Mengkonfigurasi window utama
        self.title("Aplikasi Biodata (Versi OOP) (23106050077)")
        self.geometry("500x600")
        self.resizable(True, True)

        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # --- Frame Utama ---
        self.main_frame = tk.Frame(master=self, padx=20, pady=20, bg="lavender")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(1, weight=1)

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # --- Judul ---
        self.label_judul = tk.Label(
            master=self.main_frame,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold"),
            bg="lavender"
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # --- Frame Input ---
        self.frame_input = tk.Frame(
            master=self.main_frame,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
        self.frame_input.columnconfigure(1, weight=1)

        # Input Nama
        self.label_nama = tk.Label(master=self.frame_input, text="Nama Lengkap:", font=("Arial", 12))
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2, sticky="EW")

        # Input NIM
        self.label_nim = tk.Label(master=self.frame_input, text="NIM:", font=("Arial", 12))
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2, sticky="EW")

        # Input Jurusan
        self.label_jurusan = tk.Label(master=self.frame_input, text="Jurusan:", font=("Arial", 12))
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(master=self.frame_input, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2, sticky="EW")

        # Input Alamat
        self.label_alamat = tk.Label(master=self.frame_input, text="Alamat:", font=("Arial", 12))
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

        self.frame_alamat = tk.Frame(master=self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.frame_alamat.grid(row=3, column=1, pady=2, sticky="EW")
        self.frame_alamat.columnconfigure(0, weight=1)

        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(master=self.frame_alamat, height=5, font=("Arial", 12), wrap="word")
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        # Jenis Kelamin
        self.label_jk = tk.Label(master=self.frame_input, text="Jenis Kelamin:", font=("Arial", 12))
        self.label_jk.grid(row=4, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=4, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(master=self.frame_jk, text="Pria", variable=self.var_jk, value="Pria")
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(master=self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita")
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox Persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

        # Tombol Submit
        self.btn_submit = tk.Button(
            master=self.main_frame,
            text="Submit Biodata",
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

        # Hover dan Shortcut
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label Hasil
        self.label_hasil = tk.Label(
            master=self.main_frame,
            text="",
            font=("Arial", 12, "italic"),
            justify=tk.LEFT,
            background="lavender"
        )
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)

        # Menu Bar
        self.menu_bar = tk.Menu(master=self)
        self.config(menu=self.menu_bar)

        # Membuat menu File
        self.file_menu = tk.Menu(master=self.menu_bar, tearoff=0)

        # Tambah item "Simpan Hasil"
        self.file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)

        # Separator
        self.file_menu.add_separator()

        # Tambah item "Keluar"
        self.file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        # Masukkan ke menu bar utama
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)


# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()
