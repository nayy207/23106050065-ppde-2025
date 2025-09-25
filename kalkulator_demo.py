import tkinter as tk
from tkinter import messagebox

class KalkulatorEventDriven:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Kalkulator Event-Driven")
        self.window.geometry("300x400")
        self.window.configure(bg="lightgray")

        # Variabel untuk menyimpan state
        self.current_input = ""
        self.operator = ""
        self.first_number = 0

        self.buat_interface()

    def buat_interface(self):
        # Display untuk menampilkan angka
        self.display = tk.Entry(
            self.window, 
            font=("Arial", 16), 
            justify="right",
            state="readonly",
            bg="white"
        )
        self.display.pack(fill=tk.X, padx=10, pady=10)

        # Frame untuk tombol
        button_frame = tk.Frame(self.window, bg="lightgray")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tombol angka (0-9)
        for i in range(3):
            for j in range(3):
                angka = i * 3 + j + 1
                btn = tk.Button(
                    button_frame,
                    text=str(angka),
                    font=("Arial", 14),
                    width=5,
                    height=2,
                    command=lambda n=angka: self.input_angka(n)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)

        # Tombol 0
        btn_0 = tk.Button(
            button_frame,
            text="0",
            font=("Arial", 14),
            width=5,
            height=2,
            command=lambda: self.input_angka(0)
        )
        btn_0.grid(row=3, column=1, padx=2, pady=2)

        # Tombol operator
        operators = ['+', '-', '*', '/']
        for i, op in enumerate(operators):
            btn_op = tk.Button(
                button_frame,
                text=op,
                font=("Arial", 14),
                width=5,
                height=2,
                bg="orange",
                command=lambda o=op: self.input_operator(o)
            )
            btn_op.grid(row=i, column=3, padx=2, pady=2)

        # Tombol sama dengan
        btn_equals = tk.Button(
            button_frame,
            text="=",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="lightblue",
            command=self.hitung_hasil
        )
        btn_equals.grid(row=3, column=2, padx=2, pady=2)

        # Tombol clear
        btn_clear = tk.Button(
            button_frame,
            text="C",
            font=("Arial", 14),
            width=5,
            height=2,
            bg="red",
            fg="white",
            command=self.clear_all
        )
        btn_clear.grid(row=3, column=0, padx=2, pady=2)

    def input_angka(self, angka):
        """Event handler untuk input angka"""
        self.current_input += str(angka)
        self.update_display()

    def update_display(self):
        """Method untuk memperbarui tampilan display"""
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
        self.display.config(state="readonly")

    def input_operator(self, op):
        """Event handler untuk input operator"""
        if self.current_input:
            self.first_number = float(self.current_input)
            self.operator = op
            self.current_input = ""
            self.update_display()

    def hitung_hasil(self):
        """Event handler untuk menghitung hasil"""
        if self.current_input and self.operator:
            try:
                second_number = float(self.current_input)

                if self.operator == '+':
                    result = self.first_number + second_number
                elif self.operator == '-':
                    result = self.first_number - second_number
                elif self.operator == '*':
                    result = self.first_number * second_number
                elif self.operator == '/':
                    if second_number != 0:
                        result = self.first_number / second_number
                    else:
                        messagebox.showerror("Error", "Pembagian dengan nol!")
                        return

                self.current_input = str(result)
                self.operator = ""
                self.first_number = 0
                self.update_display()

            except ValueError:
                messagebox.showerror("Error", "Input tidak valid!")

    def clear_all(self):
        """Event handler untuk clear semua"""
        self.current_input = ""
        self.operator = ""
        self.first_number = 0
        self.update_display()

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan kalkulator event-driven
if __name__ == "__main__":
    kalkulator = KalkulatorEventDriven()
    kalkulator.jalankan()