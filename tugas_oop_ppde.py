import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import re

# Logging setup
logging.basicConfig(
    filename='biodata_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

class appBio(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window config
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("550x650")
        self.resizable(True, True)

        self.frame_aktif = None

        # Temporary Database
        self.users_db = {
            "admin": "123",
            "mhs1": "12345"
        }

        # Make display
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Switch display
        self._pindah_ke(self.frame_login)

        # Load Remember Me
        self._load_remember_me()

        logging.info("Aplikasi Dimulai")

    def submit_data(self):
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # get data from form
            nama = self.entry_nama.get()
            nim = self.entry_nim.get()
            jurusan = self.entry_jurusan.get()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tgl_lahir = self.var_tanggal_lahir.get().strip()

            # Validasi
            if not nama or not nim or not jurusan or not alamat:
                messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
                return
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM salah", "NIM harus berupa angka minimal 8")
                self.entry_nim.focus_set()
                return
            if nama.isdigit():
                messagebox.showwarning("Format Nama salah", "Nama tidak boleh hanya angka!")
                self.entry_nama.focus_set()
                return
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showwarning("Format Email salah", "Masukkan email yang valid!")
                self.entry_email.focus_set()
                return
            if not (telepon.isdigit() and telepon.startswith("08") and 10 <= len(telepon) <= 13):
                messagebox.showwarning("Format Telepon salah", "Telepon harus angka 10-13 digit dan mulai dengan 08")
                self.entry_telepon.focus_set()
                return
            try:
                datetime.datetime.strptime(tgl_lahir, "%d-%m-%Y")
            except ValueError:
                messagebox.showwarning("Format Tanggal salah", "Gunakan format DD-MM-YYYY untuk Tanggal Lahir")
                self.entry_tanggal_lahir.focus_set()
                return

            # Hasil
            hasil = (
                f"Nama: {nama}\n"
                f"NIM: {nim}\n"
                f"Jurusan: {jurusan}\n"
                f"Alamat: {alamat}\n"
                f"Jenis Kelamin: {jenis_kelamin}\n"
                f"Email: {email}\n"
                f"Telepon: {telepon}\n"
                f"Tanggal Lahir: {tgl_lahir}"
            )
            messagebox.showinfo("Data tersimpan", hasil)
            logging.info(f"Data submitted by user: {self.current_user}")

            hasil_lengkap = (
                f"Nama : {nama}\nNIM : {nim}\nJurusan : {jurusan}\nAlamat : {alamat}\n"
                f"Jenis kelamin : {jenis_kelamin}\nEmail : {email}\nTelepon : {telepon}\nTanggal lahir : {tgl_lahir}"
            )
            self.label_hasil.config(text=f"BIODATA TERSIMPAN :\n\n{hasil_lengkap}")
            self._simpan_hasil()
        except Exception as e:
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    # Event handlers
    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def add_hover(self, button, color_hover, color_normal):
        button.bind("<Enter>", lambda e: button.config(bg=color_hover))
        button.bind("<Leave>", lambda e: button.config(bg=color_normal))

    # Widget
    def _buat_tampilan_biodata(self):
        # GUI config starts here
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tanggal_lahir = tk.StringVar()

        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20, bg="oldlace")
        self.frame_biodata.columnconfigure(1, weight=1)

        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Courier New", 16, "bold"),
            bg="oldlace"
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # Input Frame
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10,
            bg="beige"
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, pady=5)

        # Label
        tk.Label(self.frame_input, text="Nama Lengkap:", font=("Courier New", 12), bg="beige").grid(row=0, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="NIM:", font=("Courier New", 12), bg="beige").grid(row=1, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="Jurusan:", font=("Courier New", 12), bg="beige").grid(row=2, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="Alamat:", font=("Courier New", 12), bg="beige").grid(row=3, column=0, sticky="NW", pady=2)
        tk.Label(self.frame_input, text="Jenis Kelamin:", font=("Courier New", 12), bg="beige").grid(row=4, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="Email:", font=("Courier New", 12), bg="beige").grid(row=5, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="Telepon:", font=("Courier New", 12), bg="beige").grid(row=6, column=0, sticky="W", pady=2)
        tk.Label(self.frame_input, text="Tanggal Lahir:\nDD-MM-YYYY", font=("Courier New", 12), bg="beige").grid(row=7, column=0, sticky="NW", pady=2)

        # Entry
        self.entry_nama = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_nama)
        self.entry_nim = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_nim)
        self.entry_jurusan = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_jurusan)
        self.entry_email = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_email)
        self.entry_telepon = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_telepon)
        self.entry_tanggal_lahir = tk.Entry(self.frame_input, width=30, font=("Courier New", 12), textvariable=self.var_tanggal_lahir)

        self.frame_alamat = tk.Frame(self.frame_input, relief=tk.SUNKEN, borderwidth=1)
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_alamat = tk.Text(master=self.frame_alamat, height=3, width=28, font=("Courier New", 12))
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        self.frame_jk = tk.Frame(master=self.frame_input, bg="beige")
        self.radio_pria = tk.Radiobutton(master=self.frame_jk, text="Pria", variable=self.var_jk, value="Pria", bg="beige")
        self.radio_wanita = tk.Radiobutton(master=self.frame_jk, text="Wanita", variable=self.var_jk, value="Wanita", bg="beige")
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita.pack(side=tk.LEFT)

        self.checkSetuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini",
            variable=self.var_setuju,
            command=self.validate_form,
            bg="beige"
        )

        self.btn_submit = tk.Button(
            master=self.frame_biodata,
            text="Submit Biodata",
            font=("Courier New", 12),
            command=self.submit_data,
            state=tk.DISABLED,
            bg="beige"
        )

        self.btn_reset = tk.Button(
            master=self.frame_biodata,
            text="Reset Form",
            font=("Courier New", 12),
            command=self._reset_form_biodata,
            bg="beige"
        )

        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Courier New", 12, "italic"),
            justify=tk.LEFT,
            bg="oldlace"
        )

        # Grid
        self.entry_nama.grid(row=0, column=1, sticky="EW", pady=2)
        self.entry_nim.grid(row=1, column=1, sticky="EW", pady=2)
        self.entry_jurusan.grid(row=2, column=1, sticky="EW", pady=2)
        self.frame_alamat.grid(row=3, column=1, sticky="EW", pady=2)
        self.frame_jk.grid(row=4, column=1, sticky="W", pady=2)
        self.entry_email.grid(row=5, column=1, sticky="EW", pady=2)
        self.entry_telepon.grid(row=6, column=1, sticky="EW", pady=2)
        self.entry_tanggal_lahir.grid(row=7, column=1, sticky="EW", pady=2)

        self.checkSetuju.grid(row=8, column=0, columnspan=2, sticky="W", pady=2)
        self.btn_submit.grid(row=9, column=0, sticky="W", pady=2)
        self.btn_reset.grid(row=9, column=1, sticky="E", pady=2)
        self.label_hasil.grid(row=10, column=0, columnspan=2, sticky="W", padx=10)

        # Event Bind
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)
        self.add_hover(self.btn_submit, "peachpuff", "beige")
        self.add_hover(self.btn_reset, "peachpuff", "beige")


    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=40,bg="oldlace")
        self.frame_login.grid_columnconfigure(0, weight=1)

        tk.Label(self.frame_login, text="HALAMAN LOGIN", font=("Courier New", 16, "bold"), bg="oldlace").grid(row=0, column=0, columnspan=2, pady=20)
        
        self.frame_login_box = tk.Frame(master=self.frame_login, relief=tk.GROOVE, borderwidth=2, padx=15, pady=15, bg="beige")
        self.frame_login_box.grid(row=1, column=0, columnspan=3, pady=10, sticky="N")

        tk.Label(self.frame_login_box, text="Username:", font=("Courier New", 12, "bold"), bg="beige").grid(row=1, column=0, sticky="E", padx=0, pady=5)
        self.entry_username = tk.Entry(self.frame_login_box, font=("Courier New", 12))
        self.entry_username.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_login_box, text="Password:", font=("Courier New", 12, "bold"), bg="beige").grid(row=2, column=0, sticky="W", pady=5)
        self.entry_password = tk.Entry(self.frame_login_box, font=("Courier New", 12), show="*")
        self.entry_password.grid(row=2, column=1, padx=5, pady=5, sticky="E")

        self.show_password = False
        self.btn_show_pass = tk.Button(self.frame_login_box, text="Show", font=("Courier New", 9), command=self._toggle_password, width=6, bg="oldlace")
        self.btn_show_pass.grid(row=2, column=2, padx=5, pady=5)

        self.btn_login = tk.Button(self.frame_login_box, text="Login", font=("Courier New", 12), command=self._coba_login, width=15, bg="oldlace")
        self.btn_login.grid(row=3, column=0, columnspan=3, pady=15)

        self.var_remember = tk.IntVar()
        self.check_remember = tk.Checkbutton(self.frame_login_box, text="Remember Me", variable=self.var_remember, bg="beige")
        self.check_remember.grid(row=4, column=0, columnspan=2, sticky="W")

        info_label = tk.Label(self.frame_login, text="Info: Username yang tersedia:\nadmin (pass:123) \nmhs1 (pass:12345)", font=("Courier New", 9), fg="gray", justify=tk.LEFT, bg="oldlace")
        info_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())
        self.add_hover(self.btn_show_pass, "peachpuff", "oldlace")
        self.add_hover(self.btn_login, "peachpuff", "oldlace")


    def _toggle_password(self):
        if self.show_password:
            self.entry_password.config(show="*")
            self.btn_show_pass.config(text="Show")
        else:
            self.entry_password.config(show="")
            self.btn_show_pass.config(text="Hide")
        self.show_password = not self.show_password

    def _load_remember_me(self):
        try:
            with open("remember_me.txt", "r", encoding="utf-8") as f:
                username = f.read().strip()
                if username:
                    self.entry_username.insert(0, username)
                    self.var_remember.set(1)
        except FileNotFoundError:
            pass

    def _pindah_ke(self, frame_tujuan):
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

    def _coba_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        logging.info(f"Login attempt for username: {username}")

        if not username or not password:
            messagebox.showwarning("Login gagal!", "Username dan password tidak boleh kosong")
            return
        if len(username) < 3:
            messagebox.showwarning("Login gagal!", "Username minimal 3 karakter")
            return
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Login berhasil", f"Selamat datang, {username}")
            if self.var_remember.get() == 1:
                with open("remember_me.txt", "w", encoding="utf-8") as f:
                    f.write(username)
            else:
                open("remember_me.txt", "w").close()
            self._reset_form_biodata()
            self._update_title_with_user()
            self._buat_menu()
            self._pindah_ke(self.frame_biodata)
        else:
            messagebox.showerror("Login gagal", "Username atau password salah")
            self.entry_username.delete(0, tk.END)
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
        self.var_tanggal_lahir.set("")
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _logout(self):
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin keluar?"):
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)

    def _buat_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _simpan_hasil(self):
        try:
            with open("simpan_biodata.txt", "a", encoding="utf-8") as f:
                f.write(self.label_hasil.cget("text"))
                f.write("\n" + "="*40 + "\n")
            logging.info(f"Hasil biodata disimpan oleh {self.current_user}")
        except Exception as e:
            logging.error(f"Gagal menyimpan hasil oleh {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Gagal menyimpan data ke file:\n{str(e)}")

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah anda yakin ingin keluar?"):
            logging.info("Aplikasi ditutup oleh user")
            self.destroy()

if __name__ == "__main__":
    app = appBio()
    app.mainloop()
