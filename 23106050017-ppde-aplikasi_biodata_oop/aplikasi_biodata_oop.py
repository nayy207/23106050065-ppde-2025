# NIM   : 23106050017
# NAMA  : AHMAD ZAMRONI TRIKARTA

import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import re
import os

logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

REMEMBER_FILE = "remember_username.txt"

class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)
        self.configure(bg="azure2")

        self.users_db = {
            "admin": "admin123",
            "user": "user123",
        }

        self.current_user = None
        self.frame_aktif = None

        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        self._load_remembered_username()

        self._pindah_ke(self.frame_login)
        self._hapus_menu()

        logging.info("Aplikasi dimulai")

    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=20)

        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="W", pady=5)

        self.entry_password = tk.Entry(
            self.frame_login, 
            font=("Arial", 12), 
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        self._password_shown = False
        self.btn_toggle_password = tk.Button(
            master=self.frame_login,
            text="Show",
            command=self.toggle_password,
            width=6
        )
        self.btn_toggle_password.grid(row=2, column=2, padx=5, sticky="W")

        self.var_remember = tk.IntVar()
        self.check_remember = tk.Checkbutton(
            master=self.frame_login,
            text="Remember Me",
            variable=self.var_remember
        )
        self.check_remember.grid(row=3, column=1, sticky="W", pady=(0, 10))

        self.btn_login = tk.Button(
            self.frame_login, 
            text="Login", 
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=4, column=0, columnspan=3, pady=20, sticky="EW")

        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        info_label = tk.Label(
            self.frame_login,
            text=("Info: Username yang tersedia:\n"
                  "admin (password: admin123)\n"
                  "user (password: user123)\n"),
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=10)

    def _buat_tampilan_biodata(self):
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl_lahir = tk.StringVar()

        self.var_nama.trace_add("write", lambda *args: self.validate_form())
        self.var_nim.trace_add("write", lambda *args: self.validate_form())
        self.var_jurusan.trace_add("write", lambda *args: self.validate_form())
        self.var_email.trace_add("write", lambda *args: self.validate_form())
        self.var_telepon.trace_add("write", lambda *args: self.validate_form())
        self.var_tgl_lahir.trace_add("write", lambda *args: self.validate_form())

        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)

        self.label_judul = tk.Label(
            master=self.frame_biodata, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        self.frame_input = tk.Frame(
            master=self.frame_biodata, 
            relief=tk.GROOVE, 
            borderwidth=2, 
            padx=10, 
            pady=10
        )

        self.label_nama = tk.Label(
            master=self.frame_input, 
            text="Nama Lengkap:", 
            font=("Arial", 12)
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        self.label_nim = tk.Label(
            master=self.frame_input, 
            text="NIM:", 
            font=("Arial", 12)
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, pady=2)

        self.label_jurusan = tk.Label(
            master=self.frame_input, 
            text="Jurusan:", 
            font=("Arial", 12)
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat:", 
            font=("Arial", 12)
        )
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

        self.frame_alamat = tk.Frame(
            master=self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=1
        )
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(
            master=self.frame_alamat, 
            height=5, 
            width=28, 
            font=("Arial", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=3, column=1, pady=2)

        self.label_email = tk.Label(
            master=self.frame_input, 
            text="Email:", 
            font=("Arial", 12)
        )
        self.label_email.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_email
        )
        self.entry_email.grid(row=4, column=1, pady=2)

        self.label_telepon = tk.Label(
            master=self.frame_input, 
            text="Telepon:", 
            font=("Arial", 12)
        )
        self.label_telepon.grid(row=5, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_telepon
        )
        self.entry_telepon.grid(row=5, column=1, pady=2)

        self.label_tgl = tk.Label(
            master=self.frame_input,
            text="Tanggal Lahir (YYYY-MM-DD):",
            font=("Arial", 12)
        )
        self.label_tgl.grid(row=6, column=0, sticky="W", pady=2)
        self.entry_tgl = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_tgl_lahir
        )
        self.entry_tgl.grid(row=6, column=1, pady=2)

        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=7, column=1, sticky="W")
        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="Pria", 
            variable=self.var_jk, 
            value="Pria"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(row=8, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        self.btn_submit = tk.Button(
            master=self.frame_biodata, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=9, column=0, columnspan=2, pady=10, sticky="EW")

        self.btn_reset = tk.Button(
            master=self.frame_biodata,
            text="Reset Form",
            font=("Arial", 10),
            command=self._reset_form_biodata
        )
        self.btn_reset.grid(row=10, column=0, columnspan=2, pady=5, sticky="EW")

        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        self.label_hasil = tk.Label(
            master=self.frame_biodata, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT
        )
        self.label_hasil.grid(row=11, column=0, columnspan=2, sticky="W", padx=10)

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")

            if self.var_remember.get() == 1:
                try:
                    with open(REMEMBER_FILE, 'w', encoding='utf-8') as f:
                        f.write(username)
                    logging.info(f"Remembered username: {username}")
                except Exception as e:
                    logging.error(f"Failed to save remembered username: {str(e)}")
            else:
                try:
                    if os.path.exists(REMEMBER_FILE):
                        os.remove(REMEMBER_FILE)
                        logging.info("Remember file removed")
                except Exception as e:
                    logging.error(f"Failed to remove remember file: {str(e)}")

            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            self._buat_menu()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _reset_form_biodata(self):
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl_lahir.set("")
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _buat_menu(self):
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
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def submit_data(self):
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tgl_lahir = self.var_tgl_lahir.get().strip()

            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            if not self._is_valid_email(email):
                messagebox.showwarning("Format Email Salah", "Email tidak valid. Contoh: user@example.com")
                self.entry_email.focus_set()
                return

            if not self._is_valid_indonesian_phone(telepon):
                messagebox.showwarning("Format Telepon Salah", "Telepon tidak valid. Format: 08xxxxxxxx atau +628xxxxxxxx")
                self.entry_telepon.focus_set()
                return

            if not self._is_valid_date_of_birth(tgl_lahir):
                messagebox.showwarning("Format Tanggal Lahir Salah", "Tanggal lahir tidak valid. Gunakan format YYYY-MM-DD dan pastikan nilai logis.")
                self.entry_tgl.focus_set()
                return

            hasil = (f"Nama: {nama}\n NIM: {nim}\n Jurusan: {jurusan}\n Alamat: {alamat}\n"
                     f"Jenis Kelamin: {jenis_kelamin}\nEmail: {email}\nTelepon: {telepon}\nTanggal Lahir: {tgl_lahir}")
            messagebox.showinfo("Data Tersimpan", hasil)

            hasil_lengkap = f"BIODATA TERSIMPAN:\n Diinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        email_valid = self._is_valid_email(self.var_email.get().strip())
        telepon_valid = self._is_valid_indonesian_phone(self.var_telepon.get().strip())
        tgl_valid = self._is_valid_date_of_birth(self.var_tgl_lahir.get().strip())

        if nama_valid and nim_valid and jurusan_valid and setuju_valid and email_valid and telepon_valid and tgl_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def _is_valid_email(self, email):
        if not email:
            return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.fullmatch(pattern, email) is not None

    def _is_valid_indonesian_phone(self, phone):
        if not phone:
            return False
        pattern = r'^(08[1-9][0-9]{6,11}|\+628[1-9][0-9]{6,11})$'
        return re.fullmatch(pattern, phone) is not None

    def _is_valid_date_of_birth(self, dob_str):
        if not dob_str:
            return False
        try:
            dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            today = datetime.date.today()
            age = (today - dob).days // 365
            return 0 <= age <= 120 and dob <= today
        except Exception:
            return False

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def simpan_hasil(self):
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_user = (self.current_user or "anon").replace(" ", "_")
            filename = f"biodata_{safe_user}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")
        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def _logout(self):
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def _load_remembered_username(self):
        try:
            if os.path.exists(REMEMBER_FILE):
                with open(REMEMBER_FILE, 'r', encoding='utf-8') as f:
                    last_user = f.read().strip()
                if last_user:
                    self.entry_username.insert(0, last_user)
                    self.var_remember.set(1)
        except Exception as e:
            logging.error(f"Failed to load remembered username: {str(e)}")

    def toggle_password(self):
        self._password_shown = not self._password_shown
        if self._password_shown:
            self.entry_password.config(show="")
            self.btn_toggle_password.config(text="Hide")
        else:
            self.entry_password.config(show="*")
            self.btn_toggle_password.config(text="Show")

if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()