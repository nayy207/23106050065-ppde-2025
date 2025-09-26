import tkinter as tk
from tkinter import messagebox, ttk
import re
from datetime import datetime, date

class RegistrasiApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Form Registrasi - Validasi Demo")
        self.window.geometry("600x700")
        self.window.configure(bg="lightgray")

        # Variabel kontrol
        self.nama_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.age_var = tk.IntVar()
        self.gender_var = tk.StringVar(value="Pria")
        self.agree_var = tk.BooleanVar()

        # Dictionary untuk menyimpan status validasi
        self.validation_status = {
            'nama': False,
            'email': False,
            'phone': False,
            'password': False,
            'confirm_password': False,
            'age': False,
            'agree': False
        }

        self.buat_interface()
        self.setup_validation()

    def buat_interface(self):
        # Judul
        title_label = tk.Label(
            self.window,
            text="FORM REGISTRASI PENGGUNA",
            font=("Arial", 18, "bold"),
            bg="lightgray",
            fg="darkblue"
        )
        title_label.pack(pady=20)

        # Main frame dengan scrollbar
        main_frame = tk.Frame(self.window, bg="lightgray")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Nama Lengkap
        self.buat_input_field(
            main_frame, "Nama Lengkap:", self.nama_var, 
            "nama", "Minimal 3 karakter, hanya huruf dan spasi"
        )

        # Email
        self.buat_input_field(
            main_frame, "Email:", self.email_var,
            "email", "Format: user@domain.com"
        )

        # Nomor Telepon
        self.buat_input_field(
            main_frame, "Nomor Telepon:", self.phone_var,
            "phone", "Format: 08xxxxxxxxxx (10-13 digit)"
        )

        # Password
        self.buat_input_field(
            main_frame, "Password:", self.password_var,
            "password", "Minimal 8 karakter, kombinasi huruf dan angka", show="*"
        )

        # Konfirmasi Password
        self.buat_input_field(
            main_frame, "Konfirmasi Password:", self.confirm_password_var,
            "confirm_password", "Harus sama dengan password", show="*"
        )

        # Umur dengan Spinbox
        age_frame = tk.Frame(main_frame, bg="lightgray")
        age_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            age_frame,
            text="Umur:",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT)

        age_spinbox = tk.Spinbox(
            age_frame,
            from_=13,
            to=100,
            textvariable=self.age_var,
            font=("Arial", 11),
            width=10
        )
        age_spinbox.pack(side=tk.LEFT, padx=5)

        self.age_indicator = tk.Label(
            age_frame,
            text="●",
            font=("Arial", 16),
            fg="red",
            bg="lightgray"
        )
        self.age_indicator.pack(side=tk.LEFT, padx=5)

        # Hint untuk umur
        tk.Label(
            main_frame,
            text="Minimal 13 tahun",
            font=("Arial", 9),
            fg="gray",
            bg="lightgray",
            anchor="w"
        ).pack(fill=tk.X, padx=25)

        # Gender dengan Radiobutton
        gender_frame = tk.Frame(main_frame, bg="lightgray")
        gender_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            gender_frame,
            text="Jenis Kelamin:",
            font=("Arial", 11, "bold"),
            bg="lightgray",
            width=20,
            anchor="w"
        ).pack(side=tk.LEFT)

        radio_frame = tk.Frame(gender_frame, bg="lightgray")
        radio_frame.pack(side=tk.LEFT)

        tk.Radiobutton(
            radio_frame,
            text="Pria",
            variable=self.gender_var,
            value="Pria",
            bg="lightgray",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(
            radio_frame,
            text="Wanita",
            variable=self.gender_var,
            value="Wanita",
            bg="lightgray",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)

        # Checkbox persetujuan
        self.agree_checkbox = tk.Checkbutton(
            main_frame,
            text="Saya menyetujui syarat dan ketentuan yang berlaku",
            variable=self.agree_var,
            font=("Arial", 11),
            bg="lightgray",
            command=self.validate_agreement
        )
        self.agree_checkbox.pack(pady=20)

        # Progress bar + label
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            main_frame,
            maximum=100,
            variable=self.progress_var,
            length=400
        )
        self.progress_bar.pack(pady=10)

        self.progress_label = tk.Label(
            main_frame,
            text="0% Complete (0/7 fields)",
            font=("Arial", 10),
            bg="lightgray"
        )
        self.progress_label.pack()

        # Tombol submit
        self.submit_btn = tk.Button(
            main_frame,
            text="DAFTAR SEKARANG",
            font=("Arial", 14, "bold"),
            bg="gray",
            fg="white",
            width=20,
            height=2,
            state=tk.DISABLED,
            command=self.submit_form
        )
        self.submit_btn.pack(pady=20)



    def buat_input_field(self, parent, label_text, variable, field_name, hint_text, show=None):
        """Method untuk membuat input field dengan validasi visual"""
        # Frame untuk field
        field_frame = tk.Frame(parent, bg="lightgray")
        field_frame.pack(fill=tk.X, pady=5)

        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Arial", 11, "bold"),
            bg="lightgray",
            width=20,
            anchor="w"
        )
        label.pack(side=tk.LEFT)

        # Frame untuk entry dan indikator
        entry_frame = tk.Frame(field_frame, bg="lightgray")
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Entry
        entry = tk.Entry(
            entry_frame,
            textvariable=variable,
            font=("Arial", 11),
            width=25,
            show=show
        )
        entry.pack(side=tk.LEFT, padx=5)

        # Indikator validasi
        indicator = tk.Label(
            entry_frame,
            text="●",
            font=("Arial", 16),
            fg="red",
            bg="lightgray"
        )
        indicator.pack(side=tk.LEFT, padx=5)

        # Hint text
        hint_label = tk.Label(
            parent,
            text=hint_text,
            font=("Arial", 9),
            fg="gray",
            bg="lightgray",
            anchor="w"
        )
        hint_label.pack(fill=tk.X, padx=25)

        # Simpan referensi untuk update nanti
        setattr(self, f"{field_name}_indicator", indicator)
        setattr(self, f"{field_name}_entry", entry)
        setattr(self, f"{field_name}_hint", hint_label)

        
    def setup_validation(self):
        """Setup validasi real-time untuk semua field"""
        self.nama_var.trace_add("write", lambda *args: self.validate_nama())
        self.email_var.trace_add("write", lambda *args: self.validate_email())
        self.phone_var.trace_add("write", lambda *args: self.validate_phone())
        self.password_var.trace_add("write", lambda *args: self.validate_password())
        self.confirm_password_var.trace_add("write", lambda *args: self.validate_confirm_password())
        self.age_var.trace_add("write", lambda *args: self.validate_age())

    def validate_nama(self):
        """Validasi nama lengkap"""
        nama = self.nama_var.get().strip()

        # Cek panjang minimal
        if len(nama) < 3:
            self.set_validation_status('nama', False, "Nama terlalu pendek")
            return False

        # Cek hanya huruf dan spasi
        if not re.match(r'^[a-zA-Z\s]+$', nama):
            self.set_validation_status('nama', False, "Hanya huruf dan spasi diperbolehkan")
            return False

        # Cek tidak boleh hanya spasi
        if nama.replace(' ', '') == '':
            self.set_validation_status('nama', False, "Nama tidak boleh kosong")
            return False

        self.set_validation_status('nama', True, "Nama valid")
        return True

    def validate_email(self):
        """Validasi format email"""
        email = self.email_var.get().strip()

        if not email:
            self.set_validation_status('email', False, "Email tidak boleh kosong")
            return False

        # Pattern regex untuk email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, email):
            self.set_validation_status('email', False, "Format email tidak valid")
            return False

        self.set_validation_status('email', True, "Email valid")
        return True

    def validate_phone(self):
        """Validasi nomor telepon"""
        phone = self.phone_var.get().strip()

        if not phone:
            self.set_validation_status('phone', False, "Nomor telepon tidak boleh kosong")
            return False

        # Cek format nomor Indonesia
        if not re.match(r'^08\d{8,11}$', phone):
            self.set_validation_status('phone', False, "Format: 08xxxxxxxxxx (10-13 digit)")
            return False

        self.set_validation_status('phone', True, "Nomor telepon valid")
        return True

    def validate_password(self):
        """Validasi password"""
        password = self.password_var.get()

        if len(password) < 8:
            self.set_validation_status('password', False, "Password minimal 8 karakter")
            return False

        # Cek kombinasi huruf dan angka
        if not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
            self.set_validation_status('password', False, "Harus kombinasi huruf dan angka")
            return False

        self.set_validation_status('password', True, "Password valid")
        # Validasi ulang confirm password jika sudah diisi
        if self.confirm_password_var.get():
            self.validate_confirm_password()
        return True

    def validate_confirm_password(self):
        """Validasi konfirmasi password"""
        password = self.password_var.get()
        confirm = self.confirm_password_var.get()

        if not confirm:
            self.set_validation_status('confirm_password', False, "Konfirmasi password tidak boleh kosong")
            return False

        if password != confirm:
            self.set_validation_status('confirm_password', False, "Password tidak sama")
            return False

        self.set_validation_status('confirm_password', True, "Password cocok")
        return True

    def validate_age(self):
        """Validasi umur"""
        try:
            age = self.age_var.get()
            if age < 13:
                self.set_validation_status('age', False, "Umur minimal 13 tahun")
                return False
            elif age > 100:
                self.set_validation_status('age', False, "Umur maksimal 100 tahun")
                return False

            self.set_validation_status('age', True, "Umur valid")
            return True
        except:
            self.set_validation_status('age', False, "Umur harus berupa angka")
            return False

    def validate_agreement(self):
        """Validasi checkbox persetujuan"""
        if self.agree_var.get():
            self.validation_status['agree'] = True
        else:
            self.validation_status['agree'] = False

        self.update_submit_button()

    def set_validation_status(self, field_name, is_valid, message):
        """Set status validasi dan update tampilan"""
        self.validation_status[field_name] = is_valid

        # Update indikator visual
        indicator = getattr(self, f"{field_name}_indicator")
        hint_label = getattr(self, f"{field_name}_hint")

        if is_valid:
            indicator.config(fg="green")
            hint_label.config(fg="green", text=f"✓ {message}")
        else:
            indicator.config(fg="red")
            hint_label.config(fg="red", text=f"✗ {message}")

        # Update tombol submit
        self.update_submit_button()

    def update_submit_button(self):
        """Update status tombol submit dan progress bar"""
        valid_count = sum(1 for status in self.validation_status.values() if status)
        total_fields = len(self.validation_status)
        progress_percentage = (valid_count / total_fields) * 100

        # Update progress bar
        self.progress_var.set(progress_percentage)
        self.progress_label.config(
            text=f"{progress_percentage:.0f}% Complete ({valid_count}/{total_fields} fields)")

        # Update tombol submit
        if progress_percentage == 100:
            self.submit_btn.config(state=tk.NORMAL, bg="green")
        else:
            self.submit_btn.config(state=tk.DISABLED, bg="gray")

    def submit_form(self):
        """Submit form dengan error handling lengkap"""
        try:
            # Validasi final semua field
            if not self.final_validation():
                return

            # Simulasi proses registrasi
            self.show_loading()

            # Kumpulkan data
            user_data = {
                'nama': self.nama_var.get().strip(),
                'email': self.email_var.get().strip(),
                'phone': self.phone_var.get().strip(),
                'age': self.age_var.get(),
                'gender': self.gender_var.get(),
                'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Simulasi delay proses
            self.window.after(2000, lambda: self.complete_registration(user_data))

        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def final_validation(self):
        """Validasi final sebelum submit"""
        errors = []

        # Validasi ulang semua field
        if not self.validate_nama():
            errors.append("Nama tidak valid")
        if not self.validate_email():
            errors.append("Email tidak valid")
        if not self.validate_phone():
            errors.append("Nomor telepon tidak valid")
        if not self.validate_password():
            errors.append("Password tidak valid")
        if not self.validate_confirm_password():
            errors.append("Konfirmasi password tidak valid")
        if not self.validate_age():
            errors.append("Umur tidak valid")
        if not self.agree_var.get():
            errors.append("Anda harus menyetujui syarat dan ketentuan")

        if errors:
            error_message = "Perbaiki kesalahan berikut:\n\n" + "\n".join(f"• {error}" for error in errors)
            messagebox.showerror("Validasi Gagal", error_message)
            return False

        return True

    def show_loading(self):
        """Tampilkan loading state"""
        self.submit_btn.config(text="MEMPROSES...", state=tk.DISABLED, bg="orange")

        # Disable semua input
        for widget_name in ['nama_entry', 'email_entry', 'phone_entry', 'password_entry', 'confirm_password_entry']:
            if hasattr(self, widget_name):
                getattr(self, widget_name).config(state=tk.DISABLED)

    def hide_loading(self):
        """Sembunyikan loading state"""
        self.submit_btn.config(text="DAFTAR SEKARANG", state=tk.NORMAL, bg="green")

        # Enable kembali semua input
        for widget_name in ['nama_entry', 'email_entry', 'phone_entry', 'password_entry', 'confirm_password_entry']:
            if hasattr(self, widget_name):
                getattr(self, widget_name).config(state=tk.NORMAL)

    def complete_registration(self, user_data):
        """Selesaikan proses registrasi"""
        self.hide_loading()

        # Tampilkan hasil registrasi
        success_message = f"""
REGISTRASI BERHASIL!

Data yang terdaftar:
• Nama: {user_data['nama']}
• Email: {user_data['email']}
• Telepon: {user_data['phone']}
• Umur: {user_data['age']} tahun
• Jenis Kelamin: {user_data['gender']}
• Tanggal Daftar: {user_data['registration_date']}

Selamat datang di aplikasi kami!
        """

        messagebox.showinfo("Registrasi Berhasil", success_message)

        # Reset form
        if messagebox.askyesno("Reset Form", "Ingin mendaftarkan pengguna lain?"):
            self.reset_form()
        else:
            self.window.quit()

    def reset_form(self):
        """Reset semua field form"""
        # Reset semua variabel
        self.nama_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")
        self.age_var.set(18)
        self.gender_var.set("Pria")
        self.agree_var.set(False)

        # Reset status validasi
        for key in self.validation_status:
            self.validation_status[key] = False

        # Reset tampilan indikator
        for field in ['nama', 'email', 'phone', 'password', 'confirm_password', 'age']:
            indicator = getattr(self, f"{field}_indicator")
            hint_label = getattr(self, f"{field}_hint")
            indicator.config(fg="red")
            hint_label.config(fg="gray")

        # Reset progress
        self.progress_var.set(0)
        self.progress_label.config(text="0% Complete (0/7 fields)")

        # Reset tombol
        self.submit_btn.config(state=tk.DISABLED, bg="gray")

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = RegistrasiApp()
    app.jalankan()