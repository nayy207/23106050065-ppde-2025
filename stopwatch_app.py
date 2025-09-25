import tkinter as tk
import math
import time

class StopwatchApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Stopwatch dengan Animasi")
        self.window.geometry("600x500")
        self.window.configure(bg="black")

        # Variabel untuk stopwatch
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.timer_job = None

        # Variabel untuk animasi
        self.animation_job = None
        self.rotation_angle = 0

        self.buat_interface()
        self.start_animation()

    def buat_interface(self):
        # Frame untuk display waktu
        time_frame = tk.Frame(self.window, bg="black")
        time_frame.pack(pady=20)

        # Label untuk menampilkan waktu
        self.time_label = tk.Label(
            time_frame,
            text="00:00:00",
            font=("Digital-7", 48, "bold"),
            fg="lime",
            bg="black"
        )
        self.time_label.pack()

        # Label untuk milidetik
        self.ms_label = tk.Label(
            time_frame,
            text="000",
            font=("Digital-7", 24),
            fg="yellow",
            bg="black"
        )
        self.ms_label.pack()

        # Canvas untuk animasi
        self.canvas = tk.Canvas(
            self.window,
            width=300,
            height=300,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # Gambar lingkaran luar (static)
        self.canvas.create_oval(
            50, 50, 250, 250,
            outline="white",
            width=3,
            tags="outer_circle"
        )

        # Gambar titik-titik penanda waktu
        self.buat_penanda_waktu()

        # Jarum detik (akan beranimasi)
        self.jarum_detik = self.canvas.create_line(
            150, 150, 150, 70,
            fill="red",
            width=3,
            tags="second_hand"
        )

        # Titik tengah
        self.canvas.create_oval(
            145, 145, 155, 155,
            fill="white",
            outline="white"
        )

    def buat_penanda_waktu(self):
        """Membuat penanda waktu di sekeliling lingkaran"""
        center_x, center_y = 150, 150
        radius = 90

        for i in range(60):
            angle = math.radians(i * 6 - 90)  # -90 untuk mulai dari atas

            if i % 5 == 0:  # Penanda jam (setiap 5 detik)
                inner_radius = radius - 15
                width = 3
                color = "white"
            else:  # Penanda detik
                inner_radius = radius - 8
                width = 1
                color = "gray"

            # Titik luar
            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)

            # Titik dalam
            x2 = center_x + inner_radius * math.cos(angle)
            y2 = center_y + inner_radius * math.sin(angle)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width
            )

        # Frame untuk tombol kontrol
        control_frame = tk.Frame(self.window, bg="black")
        control_frame.pack(pady=20)

        # Tombol Start/Stop
        self.start_stop_btn = tk.Button(
            control_frame,
            text="START",
            font=("Arial", 14, "bold"),
            bg="green",
            fg="white",
            width=10,
            command=self.toggle_stopwatch
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=10)

        # Tombol Reset
        self.reset_btn = tk.Button(
            control_frame,
            text="RESET",
            font=("Arial", 14, "bold"),
            bg="red",
            fg="white",
            width=10,
            command=self.reset_stopwatch
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)

        # Tombol Lap
        self.lap_btn = tk.Button(
            control_frame,
            text="LAP",
            font=("Arial", 14, "bold"),
            bg="blue",
            fg="white",
            width=10,
            command=self.record_lap,
            state=tk.DISABLED
        )
        self.lap_btn.pack(side=tk.LEFT, padx=10)

        # Frame untuk lap times
        lap_frame = tk.LabelFrame(
            self.window,
            text="Lap Times",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="black"
        )
        lap_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Listbox untuk menampilkan lap times
        self.lap_listbox = tk.Listbox(
            lap_frame,
            font=("Courier", 11),
            bg="black",
            fg="lime",
            selectbackground="gray"
        )
        self.lap_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Variabel untuk lap times
        self.lap_times = []
        self.lap_count = 0

    def toggle_stopwatch(self):
        """Toggle start/stop stopwatch"""
        if not self.is_running:
            self.start_stopwatch()
        else:
            self.stop_stopwatch()

    def start_stopwatch(self):
        """Mulai stopwatch"""
        self.is_running = True
        self.start_time = time.time() - self.elapsed_time

        # Update tampilan tombol
        self.start_stop_btn.config(text="STOP", bg="red")
        self.lap_btn.config(state=tk.NORMAL)

        # Mulai timer
        self.update_time()

    def stop_stopwatch(self):
        """Stop stopwatch"""
        self.is_running = False

        # Update tampilan tombol
        self.start_stop_btn.config(text="START", bg="green")
        self.lap_btn.config(state=tk.DISABLED)

        # Hentikan timer
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

    def reset_stopwatch(self):
        """Reset stopwatch"""
        self.stop_stopwatch()
        self.elapsed_time = 0

        # Reset tampilan
        self.time_label.config(text="00:00:00")
        self.ms_label.config(text="000")

        # Reset lap times
        self.lap_times.clear()
        self.lap_count = 0
        self.lap_listbox.delete(0, tk.END)

        # Reset jarum detik
        self.update_second_hand(0)

    def record_lap(self):
        """Catat lap time"""
        if self.is_running:
            self.lap_count += 1
            current_time = self.elapsed_time

            # Hitung lap time (selisih dengan lap sebelumnya)
            if self.lap_times:
                lap_time = current_time - self.lap_times[-1][1]
            else:
                lap_time = current_time

            # Simpan lap time
            self.lap_times.append((self.lap_count, current_time, lap_time))

            # Format dan tampilkan
            total_formatted = self.format_time(current_time)
            lap_formatted = self.format_time(lap_time)

            lap_text = f"Lap {self.lap_count:2d}: {lap_formatted} (Total: {total_formatted})"
            self.lap_listbox.insert(tk.END, lap_text)

            # Scroll ke bawah
            self.lap_listbox.see(tk.END)

    def update_time(self):
        """Update tampilan waktu"""
        if self.is_running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time

            # Update tampilan waktu
            time_str = self.format_time(self.elapsed_time)
            self.time_label.config(text=time_str)

            # Update milidetik
            ms = int((self.elapsed_time % 1) * 1000)
            self.ms_label.config(text=f"{ms:03d}")

            # Update jarum detik
            seconds = self.elapsed_time % 60
            self.update_second_hand(seconds)

            # Schedule next update
            self.timer_job = self.window.after(10, self.update_time)

    def format_time(self, seconds):
        """Format waktu ke string HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_second_hand(self, seconds):
        """Update posisi jarum detik"""
        # Hitung sudut (0 detik = atas, 15 detik = kanan, dst)
        angle = math.radians(seconds * 6 - 90)  # -90 untuk mulai dari atas

        center_x, center_y = 150, 150
        length = 70

        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)

        # Update koordinat jarum
        self.canvas.coords(
            self.jarum_detik,
            center_x, center_y,
            end_x, end_y
        )

    def start_animation(self):
        """Mulai animasi latar belakang"""
        self.animate_background()

    def animate_background(self):
        """Animasi latar belakang (opsional)"""
        # Rotasi sudut untuk efek visual
        self.rotation_angle = (self.rotation_angle + 1) % 360

        # Update warna border berdasarkan status
        if self.is_running:
            color = f"#{int(127 + 127 * math.sin(math.radians(self.rotation_angle * 4))):02x}0000"
        else:
            color = "white"

        self.canvas.itemconfig("outer_circle", outline=color)

        # Schedule next animation frame
        self.animation_job = self.window.after(50, self.animate_background)

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = StopwatchApp()
    app.jalankan()