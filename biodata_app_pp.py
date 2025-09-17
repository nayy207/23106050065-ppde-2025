import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import os
import re

logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Atribut untuk manajemen frame
        self.frame_aktif = None
        self.current_user = None
        self.show_password = False  # untuk toggle password

        # Remember Me state
        self.remember_me_file = "remember_me.txt"
        self.last_username = ""
        if os.path.exists(self.remember_me_file):
            try:
                with open(self.remember_me_file, "r", encoding="utf-8") as f:
                    self.last_username = f.read().strip()
            except Exception as e:
                logging.error(f"Failed to read remember_me file: {e}")
                self.last_username = ""
        
        # Inisialisasi variabel kontrol Tkinter di __init__
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tanggal = tk.StringVar()

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        
        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
            "nayra": "1304"
        }

        logging.info("Aplikasi dimulai")

    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
            self._hapus_menu()
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())
            self._buat_menu()

    def _coba_login(self, event=None):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            
            # Remember Me handling
            if self.var_remember.get() == 1:
                with open(self.remember_me_file, "w", encoding="utf-8") as f:
                    f.write(username)
            else:
                if os.path.exists(self.remember_me_file):
                    os.remove(self.remember_me_file)
            
            # Kosongkan password field setelah login berhasil
            self.entry_password.delete(0, tk.END)

        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()
            return # Tambahkan return di sini agar tidak melanjutkan proses

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tanggal.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.validate_form()

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login,
            text="HALAMAN LOGIN",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Username
        tk.Label(self.frame_login, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12), width=25)
        self.entry_username.grid(row=1, column=1, pady=5, sticky="W")

        # isi username terakhir jika ada
        if self.last_username:
            self.entry_username.insert(0, self.last_username)

        # Password + Show/Hide
        tk.Label(self.frame_login, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="W", pady=5)

        frame_pass = tk.Frame(self.frame_login)
        frame_pass.grid(row=2, column=1, sticky="W")

        self.entry_password = tk.Entry(frame_pass, font=("Arial", 12), show="*")
        self.entry_password.pack(side=tk.LEFT)

        self.btn_toggle_pass = tk.Button(
            frame_pass, text="👁", width=3, command=self._toggle_password
        )
        self.btn_toggle_pass.pack(side=tk.LEFT, padx=5)

        # Remember Me
        self.var_remember = tk.IntVar(value=1 if self.last_username else 0)
        self.check_remember = tk.Checkbutton(
            self.frame_login, text="Remember Me", variable=self.var_remember, font=("Arial", 10)
        )
        self.check_remember.grid(row=3, column=0, columnspan=2, sticky="W", pady=5)

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login, text="Login", font=("Arial", 12, "bold"), command=self._coba_login
        )
        self.btn_login.grid(row=4, column=0, columnspan=2, pady=20, sticky="EW")

        # Shortcut
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        self.label_info = tk.Label(
            self.frame_login,
            text="Info: Username tersedia:\nadmin (123)\nuser1 (password1)\nmahasiswa (123456)\nnayra (1304)",
            font=("Arial", 10),
            fg="blue"
        )
        self.label_info.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

    def _toggle_password(self):
        if self.show_password:
            self.entry_password.config(show="*")
            self.btn_toggle_pass.config(text="👁")
            self.show_password = False
        else:
            self.entry_password.config(show="")
            self.btn_toggle_pass.config(text="🙈")
            self.show_password = True

    def _buat_tampilan_biodata(self):
        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.grid_columnconfigure(0, weight=1)
        self.frame_biodata.grid_columnconfigure(1, weight=1)

        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Input Nama
        tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12)).grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        tk.Label(self.frame_input, text="NIM:", font=("Arial", 12)).grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2)

        # Input Jurusan
        tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12)).grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input Email
        tk.Label(self.frame_input, text="Email:", font=("Arial", 12)).grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_email)
        self.entry_email.grid(row=3, column=1, pady=2)

        # Input Telepon
        tk.Label(self.frame_input, text="Telepon:", font=("Arial", 12)).grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_telepon)
        self.entry_telepon.grid(row=4, column=1, pady=2)

        # Input Tanggal Lahir
        tk.Label(self.frame_input, text="Tanggal Lahir (DD-MM-YYYY):", font=("Arial", 12)).grid(row=5, column=0, sticky="W", pady=2)
        self.entry_tanggal = tk.Entry(self.frame_input, width=30, font=("Arial", 12), textvariable=self.var_tanggal)
        self.entry_tanggal.grid(row=5, column=1, pady=2)

        # Input alamat dengan Text widget
        tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12)).grid(row=6, column=0, sticky="NW", pady=2)

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.frame_alamat.grid(row=6, column=1, pady=2)
        
        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(self.frame_alamat, height=5, width=28, font=("Arial", 12))
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        # Jenis kelamin
        tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12)).grid(row=7, column=0, sticky="W", pady=2)
        self.frame_jk = tk.Frame(self.frame_input)
        self.frame_jk.grid(row=7, column=1, sticky="W")

        tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita").pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.frame_biodata,
            text="Submit",
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=2, column=0, pady=20, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.entry_email.bind("<Return>", self.submit_shortcut)
        self.entry_telepon.bind("<Return>", self.submit_shortcut)
        self.entry_tanggal.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Arial", 12, "italic"),
            justify=tk.LEFT
        )
        self.label_hasil.grid(row=3, column=0, columnspan=2, sticky="W", padx=10)

        # Tombol reset form
        self.btn_reset = tk.Button(
            master=self.frame_biodata,
            text="Reset Form",
            font=("Arial", 12),
            command=self._reset_form_biodata
        )
        self.btn_reset.grid(row=2, column=1, pady=20, sticky="EW")

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Ambil data dari form
            nama = self.var_nama.get().strip()
            nim = self.var_nim.get().strip()
            jurusan = self.var_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tanggal = self.var_tanggal.get().strip()
            
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Validasi field kosong
            if not nama or not nim or not jurusan or not email or not telepon or not tanggal:
                messagebox.showwarning("Input Kosong", "Nama, NIM, Jurusan, Email, Telepon, dan Tanggal Lahir harus diisi!")
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 11:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 12 digit!")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Validasi Email
            pola_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pola_email, email):
                messagebox.showwarning("Format Email Salah", "Masukkan email yang valid!")
                self.entry_email.focus_set()
                return

            # Validasi Telepon Indonesia
            pola_telp = r'^(?:\+62|62|0)8[1-9][0-9]{6,10}$'
            if not re.match(pola_telp, telepon):
                messagebox.showwarning("Format Telepon Salah", "Nomor telepon harus format Indonesia (contoh: 08123456789).")
                self.entry_telepon.focus_set()
                return

            # Validasi Tanggal Lahir
            try:
                datetime.datetime.strptime(tanggal, "%d/%m/%Y")
            except ValueError:
                messagebox.showwarning("Format Tanggal Salah", "Tanggal lahir harus format DD/MM/YYYY dan valid!")
                self.entry_tanggal.focus_set()
                return

            # Tampilkan hasil
            hasil_lengkap = (
                f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                f"Email: {email}\nTelepon: {telepon}\nTanggal Lahir: {tanggal}\n"
                f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            )
            self.label_hasil.config(text=hasil_lengkap)
            messagebox.showinfo("Data Tersimpan", "Data biodata berhasil disimpan.")
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        email_valid = self.var_email.get().strip() != ""
        telepon_valid = self.var_telepon.get().strip() != ""
        tanggal_valid = self.var_tanggal.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        # Cek semua field yang relevan untuk mengaktifkan tombol Submit
        if nama_valid and nim_valid and jurusan_valid and email_valid and telepon_valid and tanggal_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="pink")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            # Ambil data langsung dari variabel kontrol
            nama = self.var_nama.get().strip()
            nim = self.var_nim.get().strip()
            jurusan = self.var_jurusan.get().strip()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tanggal = self.var_tanggal.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Pastikan semua field terisi sebelum menyimpan
            if not (nama and nim and jurusan and email and telepon and tanggal and alamat):
                messagebox.showwarning("Peringatan", "Data biodata belum lengkap. Mohon isi semua field terlebih dahulu.")
                return

            # Buat string hasil lengkap
            hasil_tersimpan = (
                f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\n"
                f"Email: {email}\nTelepon: {telepon}\nTanggal Lahir: {tanggal}\n"
                f"Alamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            )
            
            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
            logging.info(f"Data for NIM {nim} saved to file '{filename}' by user '{self.current_user}'")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
            logging.error(f"Permission error when saving file by {self.current_user}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")
            logging.error(f"Error saving file by {self.current_user}: {e}")

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()