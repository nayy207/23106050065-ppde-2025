import tkinter as tk
from tkinter import messagebox


class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Database user
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        self.current_user = None
        self.frame_aktif = None

        # Buat semua tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Awalnya ke login
        self._pindah_ke(self.frame_login)

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.frame_login,
            text="HALAMAN LOGIN",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(self.frame_login, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        # Password
        tk.Label(self.frame_login, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        # Info akun
        info_label = tk.Label(
            self.frame_login,
            text="Info: admin/123 | user1/password1 | mahasiswa/123456",
            font=("Arial", 9),
            fg="gray"
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)

    def _buat_tampilan_biodata(self):
        # Variabel
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)

        tk.Label(self.frame_biodata, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        # Input
        tk.Label(self.frame_biodata, text="Nama Lengkap:", font=("Arial", 12)).grid(row=1, column=0, sticky="W")
        self.entry_nama = tk.Entry(self.frame_biodata, textvariable=self.var_nama, font=("Arial", 12))
        self.entry_nama.grid(row=1, column=1, sticky="EW")

        tk.Label(self.frame_biodata, text="NIM:", font=("Arial", 12)).grid(row=2, column=0, sticky="W")
        self.entry_nim = tk.Entry(self.frame_biodata, textvariable=self.var_nim, font=("Arial", 12))
        self.entry_nim.grid(row=2, column=1, sticky="EW")

        tk.Label(self.frame_biodata, text="Jurusan:", font=("Arial", 12)).grid(row=3, column=0, sticky="W")
        self.entry_jurusan = tk.Entry(self.frame_biodata, textvariable=self.var_jurusan, font=("Arial", 12))
        self.entry_jurusan.grid(row=3, column=1, sticky="EW")

        tk.Label(self.frame_biodata, text="Jenis Kelamin:", font=("Arial", 12)).grid(row=4, column=0, sticky="W")
        frame_jk = tk.Frame(self.frame_biodata)
        frame_jk.grid(row=4, column=1, sticky="W")
        tk.Radiobutton(frame_jk, text="Pria", variable=self.var_jk, value="Pria").pack(side=tk.LEFT)
        tk.Radiobutton(frame_jk, text="Wanita", variable=self.var_jk, value="Wanita").pack(side=tk.LEFT)

        self.checkbutton = tk.Checkbutton(
            self.frame_biodata,
            text="Saya menyetujui pengumpulan data",
            variable=self.var_setuju
        )
        self.checkbutton.grid(row=5, column=0, columnspan=2, pady=5, sticky="W")

        self.btn_submit = tk.Button(
            self.frame_biodata,
            text="Submit Biodata",
            font=("Arial", 12, "bold"),
            command=self.submit_data
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")

        self.label_hasil = tk.Label(self.frame_biodata, text="", font=("Arial", 12, "italic"))
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W")

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            self._pindah_ke(self.frame_biodata)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

    def submit_data(self):
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        nama = self.var_nama.get().strip()
        nim = self.var_nim.get().strip()
        jurusan = self.var_jurusan.get().strip()
        jenis_kelamin = self.var_jk.get()

        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)
        self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()
