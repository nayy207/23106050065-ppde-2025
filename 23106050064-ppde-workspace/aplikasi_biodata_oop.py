import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import os
import re

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()

        # Konfigurasi window utama 
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)
        self.configure(bg="LightSkyBlue")  # warna utama window

        # Database user sederhana
        self.users_db = {
            "admin": "123",
            "Bintang": "23106050064",
            "mahasiswa": "123456",
        }

        # Status dan manajemen frame
        self.current_user = None
        self.frame_aktif = None

        # Buat tampilan (login & biodata) — jangan panggil menu di sini supaya tidak muncul saat login
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        logging.info("Aplikasi dimulai")

    # ----------------- LOGIN -----------------
    def _buat_tampilan_login(self):
        # warna frame login berbeda
        self.frame_login = tk.Frame(master=self, padx=20, pady=100, bg="LightCyan")
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        tk.Label(self.frame_login, text="HALAMAN LOGIN", font=("Arial", 16, "bold"), bg="LightCyan").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.frame_login, text="Username:", font=("Arial", 12), bg="LightCyan").grid(row=1, column=0, sticky="W", pady=5)
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        tk.Label(self.frame_login, text="Password:", font=("Arial", 12), bg="LightCyan").grid(row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        self.btn_login = tk.Button(self.frame_login, text="Login", font=("Arial", 12, "bold"), command=self._coba_login)
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        # Shortcut enter di login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

    # ----------------- BIODATA -----------------
    def _buat_tampilan_biodata(self):
        # Variabel kontrol
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # trace untuk validasi realtime
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # Frame biodata (warna berbeda)
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="MintCream")
        # konfigurasi grid di frame_biodata untuk responsif
        self.frame_biodata.columnconfigure(0, weight=1)
        self.frame_biodata.columnconfigure(1, weight=1)
        self.frame_biodata.rowconfigure(1, weight=1)

        # Judul
        tk.Label(self.frame_biodata, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"), bg="MintCream").grid(row=0, column=0, columnspan=2, pady=20)

        # Frame input (form) dengan warna kontras
        self.frame_input = tk.Frame(master=self.frame_biodata, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, bg="AliceBlue")
        # konfigurasi grid di frame_input agar kolom input melebar
        self.frame_input.columnconfigure(0, weight=0)
        self.frame_input.columnconfigure(1, weight=1)
        # baris alamat dibuat fleksibel agar Text bisa tumbuh
        for i in range(6):
            self.frame_input.rowconfigure(i, weight=0)
        self.frame_input.rowconfigure(3, weight=1)

        # Input Nama
        tk.Label(self.frame_input, text="Nama Lengkap:", font=("Arial", 12), bg="AliceBlue").grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(self.frame_input, font=("Arial", 12), textvariable=self.var_nama)
        self.entry_nama.grid(row=0, column=1, pady=2, sticky="EW")

        # Input NIM
        tk.Label(self.frame_input, text="NIM:", font=("Arial", 12), bg="AliceBlue").grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(self.frame_input, font=("Arial", 12), textvariable=self.var_nim)
        self.entry_nim.grid(row=1, column=1, pady=2, sticky="EW")

        # Input Jurusan
        tk.Label(self.frame_input, text="Jurusan:", font=("Arial", 12), bg="AliceBlue").grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(self.frame_input, font=("Arial", 12), textvariable=self.var_jurusan)
        self.entry_jurusan.grid(row=2, column=1, pady=2, sticky="EW")

        # Input Alamat (Text + scrollbar)
        tk.Label(self.frame_input, text="Alamat:", font=("Arial", 12), bg="AliceBlue").grid(row=3, column=0, sticky="NW", pady=2)
        self.frame_alamat = tk.Frame(master=self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(master=self.frame_alamat, height=5, font=("Arial", 12))
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=3, column=1, pady=2, sticky="NSEW")

        # Jenis kelamin (radio)
        tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Arial", 12), bg="AliceBlue").grid(row=4, column=0, sticky="W", pady=2)
        self.frame_jk = tk.Frame(master=self.frame_input, bg="AliceBlue")
        self.frame_jk.grid(row=4, column=1, sticky="W")
        tk.Radiobutton(self.frame_jk, text="Pria", variable=self.var_jk, value="Pria", bg="AliceBlue").pack(side=tk.LEFT)
        tk.Radiobutton(self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita", bg="AliceBlue").pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form,
            bg="AliceBlue"
        )
        self.check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

        # letakkan frame_input di frame_biodata
        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)

        # Tombol submit
        self.btn_submit = tk.Button(master=self.frame_biodata, text="Submit Biodata", font=("Arial", 12, "bold"), command=self.submit_data, state=tk.DISABLED)
        self.btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW", padx=5)

        # Event binding hover / shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label hasil
        self.label_hasil = tk.Label(master=self.frame_biodata, text="", font=("Arial", 12, "italic"), justify=tk.LEFT, bg="MintCream")
        self.label_hasil.grid(row=3, column=0, columnspan=2, sticky="W", padx=10, pady=(0,10))

    # ----------------- MENU -----------------
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
        # mengganti menu dengan menu kosong
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    # ----------------- NAVIGASI -----------------
    def _pindah_ke(self, frame_tujuan):
        # sembunyikan frame aktif (jika ada)
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        # tampilkan frame baru
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # jika pindah ke login -> sembunyikan menu; jika pindah ke biodata -> buat menu
        if frame_tujuan == self.frame_login:
            self._hapus_menu()
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self._buat_menu()  # pastikan menu muncul saat biodata
            self.after(100, lambda: self.entry_nama.focus_set())

    # ----------------- LOGIN LOGIC -----------------
    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            logging.warning("Empty credentials")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        if len(username) < 3:
            logging.warning("Username too short")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login: {username}")
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._pindah_ke(self.frame_biodata)
            # bersihkan credential fields
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt: {username}")
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
        self.label_hasil.config(text="")
        self.btn_submit.config(state=tk.DISABLED)

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    # ----------------- LOGOUT -----------------
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

    # ----------------- VALIDASI & SUBMIT -----------------
    def submit_data(self):
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        nama = self.entry_nama.get().strip()
        nim = self.entry_nim.get().strip()
        jurusan = self.entry_jurusan.get().strip()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
            return

        # Validasi NIM sederhana
        if not nim.isdigit() or len(nim) < 8:
            messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
            self.entry_nim.focus_set()
            return

        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)
        hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
        self.label_hasil.config(text=hasil_lengkap)
        logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

    def validate_form(self, *args):
        if (
            self.var_nama.get().strip()
            and self.var_nim.get().strip()
            and self.var_jurusan.get().strip()
            and self.var_setuju.get() == 1
        ):
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        try:
            self.btn_submit.config(bg="SystemButtonFace")
        except Exception:
            pass

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()
            return "break"

    # ----------------- SIMPAN -----------------
    def simpan_hasil(self):
        hasil_tersimpan = self.label_hasil.cget("text")
        if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan.")
            return
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_user = re.sub(r'[^A-Za-z0-9_-]', '_', str(self.current_user))
        filename = f"biodata_{safe_user}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(hasil_tersimpan)
            messagebox.showinfo("Info", f"Data disimpan ke '{os.path.abspath(filename)}'.")
            logging.info(f"Saved biodata to file: {filename} by user: {self.current_user}")
        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
            logging.error("PermissionError while saving file")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")
            logging.error(f"Error saving file: {str(e)}")

    # ----------------- KELUAR -----------------
    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()
