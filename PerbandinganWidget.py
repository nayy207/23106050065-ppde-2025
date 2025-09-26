import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class PerbandinganWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Perbandingan Widget Tkinter vs ttk")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Variabel untuk menyimpan data
        self.nama_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Laki-laki")
        self.hobi_vars = {
            'membaca': tk.BooleanVar(),
            'olahraga': tk.BooleanVar(),
            'musik': tk.BooleanVar()
        }

        self._buat_interface()

    def _buat_interface(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10,5))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Perbandingan Widget Tkinter vs ttk",
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)

        # Frame untuk widget Tkinter standar
        tk_frame = tk.LabelFrame(self.root, text="Widget Tkinter Standar",
                                font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        tk_frame.pack(side='left', fill='both', expand=True, padx=(10,5), pady=5)

        # Input nama dengan Tkinter standar
        tk.Label(tk_frame, text="Nama:", font=('Arial', 10), bg='#f0f0f0').pack(anchor='w', padx=10, pady=(10,0))
        self.tk_entry = tk.Entry(tk_frame, textvariable=self.nama_var, font=('Arial', 10))
        self.tk_entry.pack(fill='x', padx=10, pady=(0,10))

        # Combobox dengan Tkinter standar (menggunakan OptionMenu)
        tk.Label(tk_frame, text="Gender:", font=('Arial', 10), bg='#f0f0f0').pack(anchor='w', padx=10)
        self.tk_option = tk.OptionMenu(tk_frame, self.gender_var, "Laki-laki", "Perempuan")
        self.tk_option.pack(fill='x', padx=10, pady=(0,10))

        # Checkbutton dengan Tkinter standar
        tk.Label(tk_frame, text="Hobi:", font=('Arial', 10), bg='#f0f0f0').pack(anchor='w', padx=10)
        for hobi, var in self.hobi_vars.items():
            tk.Checkbutton(tk_frame, text=hobi.capitalize(), variable=var,
                          font=('Arial', 9), bg='#f0f0f0').pack(anchor='w', padx=20)

        # Button dengan Tkinter standar
        tk.Button(tk_frame, text="Submit (Tkinter)", command=self.submit_tk,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(pady=20, padx=10)
        
        # Frame untuk widget ttk
        ttk_frame = tk.LabelFrame(self.root, text="Widget ttk (Themed)",
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        ttk_frame.pack(side='right', fill='both', expand=True, padx=(5,10), pady=5)

        # Input nama dengan ttk
        ttk.Label(ttk_frame, text="Nama:", font=('Arial', 10)).pack(anchor='w', padx=10, pady=(10,0))
        self.ttk_entry = ttk.Entry(ttk_frame, textvariable=self.nama_var, font=('Arial', 10))
        self.ttk_entry.pack(fill='x', padx=10, pady=(0,10))

        # Combobox dengan ttk
        ttk.Label(ttk_frame, text="Gender:", font=('Arial', 10)).pack(anchor='w', padx=10)
        self.ttk_combo = ttk.Combobox(ttk_frame, textvariable=self.gender_var,
                                     values=["Laki-laki", "Perempuan"], state="readonly")
        self.ttk_combo.pack(fill='x', padx=10, pady=(0,10))

        # Checkbutton dengan ttk
        ttk.Label(ttk_frame, text="Hobi:", font=('Arial', 10)).pack(anchor='w', padx=10)
        for hobi, var in self.hobi_vars.items():
            ttk.Checkbutton(ttk_frame, text=hobi.capitalize(), variable=var).pack(anchor='w', padx=20)

        # Button dengan ttk
        ttk.Button(ttk_frame, text="Submit (ttk)", command=self.submit_ttk).pack(pady=20, padx=10)

    def submit_tk(self):
        hobi_terpilih = [hobi for hobi, var in self.hobi_vars.items() if var.get()]
        print(f"Tkinter Submit - Nama: {self.nama_var.get()}, Gender: {self.gender_var.get()}, Hobi: {hobi_terpilih}")

    def submit_ttk(self):
        hobi_terpilih = [hobi for hobi, var in self.hobi_vars.items() if var.get()]
        print(f"ttk Submit - Nama: {self.nama_var.get()}, Gender: {self.gender_var.get()}, Hobi: {hobi_terpilih}")

    def run(self):
        self.root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    app = PerbandinganWidget()
    app.run()