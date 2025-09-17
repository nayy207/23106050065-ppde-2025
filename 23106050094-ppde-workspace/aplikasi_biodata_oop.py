# Nama : Syafiq Rustiawanto
# NIM : 23106050094
# Matkul : Pemrograman Platform Desktop dan Embedded
# Materi : OOP GUI

import tkinter as tk
from tkinter import messagebox


class AplikasiBiodata(tk.Tk):
	"""Aplikasi Biodata Mahasiswa (Versi OOP) - Hanya Bagian 1 (tanpa login)."""

	def __init__(self):
		super().__init__()

		# Konfigurasi window utama
		self.title("Aplikasi Biodata (Versi OOP)")
		self.geometry("600x700")
		self.resizable(True, True)
		self.configure(bg="lightblue")

		# --- Variabel Kontrol Tkinter ---
		self.var_nama = tk.StringVar()
		self.var_nim = tk.StringVar()
		self.var_jurusan = tk.StringVar()
		self.var_jk = tk.StringVar(value="Pria")
		self.var_setuju = tk.IntVar()

		# --- Frame Utama ---
		self.main_frame = tk.Frame(master=self, padx=20, pady=20, bg=self["bg"])
		self.main_frame.pack(fill=tk.BOTH, expand=True)
		self.main_frame.columnconfigure(0, weight=1)
		self.main_frame.columnconfigure(1, weight=1)

		# Aktifkan trace untuk validasi real-time
		self.var_nama.trace_add("write", self.validate_form)
		self.var_nim.trace_add("write", self.validate_form)
		self.var_jurusan.trace_add("write", self.validate_form)

		# --- Membuat dan Menempatkan Widget ---
		# Judul
		self.label_judul = tk.Label(
			master=self.main_frame,
			text="FORM BIODATA MAHASISWA",
			font=("Arial", 18, "bold"),
			bg=self["bg"],
		)
		self.label_judul.grid(row=0, column=0, columnspan=2, pady=(10, 20))

		# Frame khusus untuk input dengan border
		self.frame_input = tk.Frame(
			master=self.main_frame,
			relief=tk.GROOVE,
			borderwidth=2,
			padx=12,
			pady=12,
		)
		self.frame_input.grid(row=1, column=0, columnspan=2, sticky="NSEW")
		# Lebarkan kolom kedua agar entry melar
		self.frame_input.columnconfigure(1, weight=1)

		# Input Nama
		self.label_nama = tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12))
		self.label_nama.grid(row=0, column=0, sticky="W", pady=4)
		self.entry_nama = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_nama)
		self.entry_nama.grid(row=0, column=1, pady=4, sticky="EW")

		# Input NIM
		self.label_nim = tk.Label(self.frame_input, text="NIM:", font=("Arial", 12))
		self.label_nim.grid(row=1, column=0, sticky="W", pady=4)
		self.entry_nim = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_nim)
		self.entry_nim.grid(row=1, column=1, pady=4, sticky="EW")

		# Input Jurusan
		self.label_jurusan = tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12))
		self.label_jurusan.grid(row=2, column=0, sticky="W", pady=4)
		self.entry_jurusan = tk.Entry(self.frame_input, width=35, font=("Arial", 12), textvariable=self.var_jurusan)
		self.entry_jurusan.grid(row=2, column=1, pady=4, sticky="EW")

		# Input alamat dengan Text + Scrollbar
		self.label_alamat = tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12))
		self.label_alamat.grid(row=3, column=0, sticky="NW", pady=4)

		self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1)
		self.frame_alamat.grid(row=3, column=1, pady=4, sticky="NSEW")
		self.frame_input.rowconfigure(3, weight=1)

		self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
		self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

		self.text_alamat = tk.Text(master=self.frame_alamat, height=5, width=32, font=("Arial", 12))
		self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.scrollbar_alamat.config(command=self.text_alamat.yview)
		self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

		# Jenis Kelamin (Radio)
		self.label_jk = tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12))
		self.label_jk.grid(row=4, column=0, sticky="W", pady=4)
		self.frame_jk = tk.Frame(self.frame_input)
		self.frame_jk.grid(row=4, column=1, sticky="W")
		self.radio_pria = tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria")
		self.radio_pria.pack(side=tk.LEFT, padx=(0, 10))
		self.radio_wanita = tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita")
		self.radio_wanita.pack(side=tk.LEFT)

		# Checkbox persetujuan
		self.check_setuju = tk.Checkbutton(
			master=self.frame_input,
			text="Saya menyetujui pengumpulan data ini.",
			variable=self.var_setuju,
			font=("Arial", 10),
			command=self.validate_form,
		)
		self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

		# Tombol submit
		self.btn_submit = tk.Button(
			master=self.main_frame,
			text="Submit Biodata",
			font=("Arial", 12, "bold"),
			command=self.submit_data,
			state=tk.DISABLED,
		)
		self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

		# Event bindings: hover dan enter
		self.btn_submit.bind("<Enter>", self.on_enter)
		self.btn_submit.bind("<Leave>", self.on_leave)
		self.entry_nama.bind("<Return>", self.submit_shortcut)
		self.entry_nim.bind("<Return>", self.submit_shortcut)
		self.entry_jurusan.bind("<Return>", self.submit_shortcut)
		self.text_alamat.bind("<Return>", self.submit_shortcut)

		# Label hasil
		self.label_hasil = tk.Label(
			master=self.main_frame,
			text="",
			font=("Arial", 12, "italic"),
			justify=tk.LEFT,
			bg=self["bg"],
		)
		self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=5)

		# Fokus awal
		self.after(100, lambda: self.entry_nama.focus_set())

	# --- Method Callback ---
	def validate_form(self, *args):
		nama_valid = self.var_nama.get().strip() != ""
		nim_valid = self.var_nim.get().strip() != ""
		jurusan_valid = self.var_jurusan.get().strip() != ""
		setuju_valid = self.var_setuju.get() == 1
		if nama_valid and nim_valid and jurusan_valid and setuju_valid:
			self.btn_submit.config(state=tk.NORMAL)
		else:
			self.btn_submit.config(state=tk.DISABLED)

	def submit_data(self):
		# Pastikan persetujuan dicentang
		if self.var_setuju.get() == 0:
			messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
			return

		# Ambil data
		nama = self.entry_nama.get().strip()
		nim = self.entry_nim.get().strip()
		jurusan = self.entry_jurusan.get().strip()
		alamat = self.text_alamat.get("1.0", tk.END).strip()
		jenis_kelamin = self.var_jk.get()

		# Validasi dasar
		if not nama or not nim or not jurusan:
			messagebox.showwarning("Input Kosong", "Semua field wajib diisi (Nama, NIM, Jurusan)!")
			return

		hasil = (
			f"Nama: {nama}\n"
			f"NIM: {nim}\n"
			f"Jurusan: {jurusan}\n"
			f"Alamat: {alamat}\n"
			f"Jenis Kelamin: {jenis_kelamin}"
		)
		messagebox.showinfo("Data Tersimpan", hasil)
		self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

	def on_enter(self, event):
		if self.btn_submit["state"] == tk.NORMAL:
			self.btn_submit.config(bg="lightblue")

	def on_leave(self, event):
		# Kembalikan ke warna default OS
		self.btn_submit.config(bg="SystemButtonFace")

	def submit_shortcut(self, event=None):
		if self.btn_submit["state"] == tk.NORMAL:
			self.submit_data()


if __name__ == "__main__":
	app = AplikasiBiodata()
	app.mainloop()

