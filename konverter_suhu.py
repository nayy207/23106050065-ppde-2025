import tkinter as tk
from tkinter import ttk
import math

class KonverterSuhu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Konverter Suhu - State Management Demo")
        self.window.geometry("500x400")
        self.window.configure(bg="lightblue")

        # Variabel kontrol
        self.celsius_var = tk.DoubleVar()
        self.fahrenheit_var = tk.DoubleVar()
        self.kelvin_var = tk.DoubleVar()
        self.rankine_var = tk.DoubleVar()

        # Flag untuk mencegah infinite loop saat update
        self.updating = False

        self.buat_interface()
        self.setup_traces()

    def buat_interface(self):
        # Judul
        title_label = tk.Label(
            self.window,
            text="KONVERTER SUHU UNIVERSAL",
            font=("Arial", 16, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

        # Frame utama
        main_frame = tk.Frame(self.window, bg="lightblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Celsius
        celsius_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        celsius_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            celsius_frame,
            text="Celsius (°C):",
            font=("Arial", 12, "bold"),
            bg="white",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.celsius_entry = tk.Entry(
            celsius_frame,
            textvariable=self.celsius_var,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        self.celsius_entry.pack(side=tk.RIGHT, padx=10, pady=10)

        # Fahrenheit
        fahrenheit_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        fahrenheit_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            fahrenheit_frame,
            text="Fahrenheit (°F):",
            font=("Arial", 12, "bold"),
            bg="white",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.fahrenheit_entry = tk.Entry(
            fahrenheit_frame,
            textvariable=self.fahrenheit_var,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        self.fahrenheit_entry.pack(side=tk.RIGHT, padx=10, pady=10)

        # Kelvin
        kelvin_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        kelvin_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            kelvin_frame,
            text="Kelvin (K):",
            font=("Arial", 12, "bold"),
            bg="white",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.kelvin_entry = tk.Entry(
            kelvin_frame,
            textvariable=self.kelvin_var,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        self.kelvin_entry.pack(side=tk.RIGHT, padx=10, pady=10)

        # Rankine
        rankine_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        rankine_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            rankine_frame,
            text="Rankine (°R):",
            font=("Arial", 12, "bold"),
            bg="white",
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.rankine_entry = tk.Entry(
            rankine_frame,
            textvariable=self.rankine_var,
            font=("Arial", 12),
            width=20,
            justify="center"
        )
        self.rankine_entry.pack(side=tk.RIGHT, padx=10, pady=10)

        # Tombol reset
        btn_reset = tk.Button(
            main_frame,
            text="Reset Semua",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.reset_all
        )
        btn_reset.pack(pady=20)

        # Frame untuk informasi tambahan
        info_frame = tk.Frame(main_frame, bg="lightyellow", relief=tk.GROOVE, bd=2)
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text="INFORMASI SUHU",
            font=("Arial", 12, "bold"),
            bg="lightyellow"
        ).pack(pady=5)

        self.info_label = tk.Label(
            info_frame,
            text="Masukkan nilai suhu di salah satu field",
            font=("Arial", 10),
            bg="lightyellow",
            justify=tk.LEFT
        )
        self.info_label.pack(pady=5)

    def setup_traces(self):
        """Setup trace untuk semua variabel"""
        self.celsius_var.trace_add("write", self.from_celsius)
        self.fahrenheit_var.trace_add("write", self.from_fahrenheit)
        self.kelvin_var.trace_add("write", self.from_kelvin)
        self.rankine_var.trace_add("write", self.from_rankine)
    
    def from_celsius(self, *args):
        """Konversi dari Celsius ke skala lain"""
        if self.updating:
            return

        try:
            celsius = self.celsius_var.get()
            self.updating = True

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = (celsius + 273.15) * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()
        except tk.TclError:
            # Terjadi saat input tidak valid (kosong atau bukan angka)
            pass
        except Exception as e:
            self.updating = False

    def from_fahrenheit(self, *args):
        """Konversi dari Fahrenheit ke skala lain"""
        if self.updating:
            return

        try:
            fahrenheit = self.fahrenheit_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = (fahrenheit - 32) * 5/9
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Kelvin
            kelvin = celsius + 273.15
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Rankine
            rankine = fahrenheit + 459.67
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_kelvin(self, *args):
        """Konversi dari Kelvin ke skala lain"""
        if self.updating:
            return

        try:
            kelvin = self.kelvin_var.get()
            self.updating = True

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = (celsius * 9/5) + 32
            self.fahrenheit_var.set(round(fahrenheit, 2))

            # Konversi ke Rankine
            rankine = kelvin * 9/5
            self.rankine_var.set(round(rankine, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def from_rankine(self, *args):
        """Konversi dari Rankine ke skala lain"""
        if self.updating:
            return

        try:
            rankine = self.rankine_var.get()
            self.updating = True

            # Konversi ke Kelvin
            kelvin = rankine * 5/9
            self.kelvin_var.set(round(kelvin, 2))

            # Konversi ke Celsius
            celsius = kelvin - 273.15
            self.celsius_var.set(round(celsius, 2))

            # Konversi ke Fahrenheit
            fahrenheit = rankine - 459.67
            self.fahrenheit_var.set(round(fahrenheit, 2))

            self.updating = False
            self.update_info()

        except tk.TclError:
            pass
        except Exception as e:
            self.updating = False

    def reset_all(self):
        """Reset semua field"""
        self.updating = True
        self.celsius_var.set(0)
        self.fahrenheit_var.set(0)
        self.kelvin_var.set(0)
        self.rankine_var.set(0)
        self.updating = False
        self.update_info()

    def update_info(self):
        """Update informasi tambahan"""
        try:
            celsius = self.celsius_var.get()

            info_text = f"Suhu saat ini: {celsius}°C\n"

            if celsius == 0:
                info_text += "• Titik beku air (kondisi normal)"
            elif celsius == 100:
                info_text += "• Titik didih air (kondisi normal)"
            elif celsius == -273.15:
                info_text += "• Suhu absolut nol"
            elif celsius < 0:
                info_text += "• Di bawah titik beku air"
            elif celsius > 100:
                info_text += "• Di atas titik didih air"
            else:
                info_text += "• Suhu normal"

            self.info_label.config(text=info_text)

        except:
            self.info_label.config(text="Masukkan nilai suhu yang valid")

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = KonverterSuhu()
    app.jalankan()