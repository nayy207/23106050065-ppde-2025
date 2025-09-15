import tkinter as tk
from tkinter import messagebox
import datetime
import logging

# Logging setup
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class appBio(tk.Tk):
    def __init__(self):
        # Constructur from main class
        super().__init__()
        
        # Main window config
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("550x600")
        self.resizable(True, True)
        
        self.frame_aktif = None
        
        # Temporary Database
        self.users_db = {
            "admin" : "123",
            "mhs1" : "12345"
        }
        
        # Make display
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()
        
        # Switch display
        self._pindah_ke(self.frame_login)
        
        # Input Frame
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10
        )
        self.frame_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Nama, NIM, Jurusan, alamat
        # Label
        self.label_nama = tk.Label(
            master=self.frame_input,
            text="Nama Lengkap: ",
            font=("Courier New", 12)
        )
        self.label_nim = tk.Label(
            master=self.frame_input,
            text="NIM: ",
            font=("Courier New", 12)
        )
        self.label_jurusan = tk.Label(
            master=self.frame_input,
            text="Jurusan: ",
            font=("Courier New", 12)
        )
        self.label_alamat = tk.Label(
            master=self.frame_input,
            text="Alamat: ",
            font=("Courier New", 12)
        )
        self.label_jk = tk.Label(
            master=self.frame_input,
            text="Jenis Kelamin: ",
            font=("Courier New", 12)
        )
        
        # Entry
        self.entry_nama = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Courier New", 12),
            textvariable=self.var_nama
        )
        self.entry_nim = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Courier New", 12),
            textvariable=self.var_nim
        )
        self.entry_jurusan = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Courier New", 12),
            textvariable=self.var_jurusan
        )
        # Alamat
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
            font=("Courier New", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # ScrollBar + Text alamat
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        
        # Jenis Kelamin
        self.frame_jk = tk.Frame(master=self.frame_input)
        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk,
            text="Pria",
            variable=self.var_jk,
            value="Pria"
        )
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita.pack(side=tk.LEFT)
        
        
        # Cek Setuju
        self.checkSetuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini",
            variable=self.var_setuju,
            command=self.validate_form
        )
        
        # Submit button
        self.btn_submit = tk.Button(
            master=self.frame_biodata,
            text="Submit Biodata",
            font=("Courier New", 12),
            command=self.submit_data,
            state=tk.DISABLED
        )
        # label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Courier New", 12, "italic"),
            justify=tk.LEFT
        )
        
        # Grid - Label & Entry
        #----------------LABEL GRID---------------------
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)
        self.label_jk.grid(row=4, column=0, sticky="W", pady=2)
        self.checkSetuju.grid(row=5, column=0, columnspan=2, sticky="W", pady=2)
        self.btn_submit.grid(row=6, column=0, columnspan=2, sticky="W", pady=2)
        self.label_hasil.grid(row=7, column=0, columnspan=2, sticky="W", padx=10)
        #----------------ENTRY GRID---------------------
        self.entry_nama.grid(row=0, column=1, sticky="EW", pady=2)
        self.entry_nim.grid(row=1, column=1, sticky="EW", pady=2)
        self.entry_jurusan.grid(row=2, column=1, sticky="EW", pady=2)
        self.frame_alamat.grid(row=3, column=1, sticky="EW", pady=2)
        self.frame_jk.grid(row=4, column=1, sticky="W", pady=2)
        
        # Event Bind
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Log Start
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
        
            if not nama or not nim or not jurusan or not alamat:
                messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
                return
            # Validasi NIM
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM salah", "NIM harus berupa angka minimal 8")
                self.entry_nim.focus_set()
                return
            if nama.isdigit():
                messagebox.showwarning("Format Nama salah", "Nama tidak boleh diisi hanya berupa angka!")
                self.entry_nama.focus_set()
                return
            # Hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"    
            messagebox.showinfo("Data tersimpan", hasil)
            logging.info(f"Data submitted by user: {self.current_user}")
            
            hasil_lengkap = f"Nama : {nama}\nNIM : {nim}\nJurusan : {jurusan}\nAlamat : {alamat}\nJenis kelamin : {jenis_kelamin}"
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
    
    # Widget 
    def _buat_tampilan_biodata(self):
        # GUI config starts here
        # Control variable Tkinter
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        
        # Main Frame
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)
        
        # Trace 
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        
        # Widget configure starts here
        # Title
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Courier New", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)
    
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)
        
        # grid config
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)
        
        # Title
        tk.Label(
            self.frame_login,
            text="HALAMAN LOGIN",
            font=("Courier New", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # User name
        tk.Label(
            self.frame_login,
            text="User name: ",
            font=("Courier New", 12, "bold")
        ).grid(row=1, column=0, sticky="W", pady=5)
        
        self.entry_username = tk.Entry(self.frame_login, font=("Courier New", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")
        # Password
        tk.Label(
            self.frame_login,
            text="Password: ",
            font=("Courier new", 12, "bold"),
        ).grid(row=2, column=0, sticky="W", pady=5)
        
        self.entry_password = tk.Entry(
            self.frame_login,
            font=("Courier New", 12),
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")
        
        # Login button
        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Courier New", 12),
            command=self._coba_login
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")
        
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())
        
        # Info for user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia: \nadmin (pass:123)",
            font=("Courier New", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)
        
    def _pindah_ke(self, frame_tujuan):
        # Method to change between display
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()
        
        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)
        
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())
    
    def _coba_login(self):
        # Login attempt
        username = self.entry_username.get().strip()   
        password = self.entry_password.get()
        
        # Log attempt
        logging.info(f"Login attempt for username: {username}")
        
        # validate empty input
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login gagal!", "Username dan password tidak boleh kosong")
            self.entry_username.focus_set()
            return
        
        # validate minimum length
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login gagal!", "Username minimal 3 karakter")
            self.entry_username.focus_set()
            return
        
        # credential check in database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo("Login berhasil", f"Selamat datang, {username}")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._buat_menu()
            self._pindah_ke(self.frame_biodata)
            
            # field cleaning
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login gagal", "Username atau password salah")
            self.entry_username.delete(0, tk.END)
            self.entry_username.focus_set()
    
    # Helper method
    def _reset_form_biodata(self):
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
    
    def _update_title_with_user(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")
    
    def _logout(self):
        # Method to go back to login screen
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin keluar?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset user status
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            
            # Login entry cleaning
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END) 
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()
    
    def _buat_menu(self):
        # Make menu for app
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        
        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="keluar", command=self.keluar_aplikasi)
        
        menu_bar.add_cascade(label="File", menu=file_menu)
    
    def _hapus_menu(self):
        # delete menu from window
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)
    
    # Save data
    def _simpan_hasil(self):
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            
            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon Submit data terlebih dahulu")
                return
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"
            
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
    
    def keluar_aplikasi(self):
        # Exit app with confirmation
        if messagebox.askokcancel("Keluar", "Apakah anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

if __name__ == "__main__":
    # instance init from appBio class
    app = appBio()
    app.mainloop()