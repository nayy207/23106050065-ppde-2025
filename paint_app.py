import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog

class PaintApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Paint App - Event Handling Demo")
        self.window.geometry("800x600")

        # Variabel untuk painting
        self.last_x = None
        self.last_y = None
        self.pen_color = "black"
        self.pen_size = 2
        self.is_drawing = False

        self.buat_interface()
        self.bind_events()

    def buat_interface(self):
        # Frame untuk toolbar
        toolbar = tk.Frame(self.window, bg="lightgray", height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        # Canvas untuk menggambar
        self.canvas = tk.Canvas(
            self.window, 
            bg="white", 
            cursor="pencil"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Tombol pilih warna
        btn_color = tk.Button(
            toolbar,
            text="Pilih Warna",
            command=self.pilih_warna,
            bg="lightblue"
        )
        btn_color.pack(side=tk.LEFT, padx=5, pady=5)

        # Label dan slider untuk ukuran pen
        tk.Label(toolbar, text="Ukuran:", bg="lightgray").pack(side=tk.LEFT, padx=5)

        self.size_var = tk.IntVar(value=2)
        size_scale = tk.Scale(
            toolbar,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            command=self.ubah_ukuran
        )
        size_scale.pack(side=tk.LEFT, padx=5)

        # Tombol clear
        btn_clear = tk.Button(
            toolbar,
            text="Clear",
            command=self.clear_canvas,
            bg="red",
            fg="white"
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        # Label info
        self.info_label = tk.Label(
            toolbar,
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}",
            bg="lightgray"
        )
        self.info_label.pack(side=tk.RIGHT, padx=10)

    def pilih_warna(self):
        """Event handler untuk memilih warna"""
        color = colorchooser.askcolor(title="Pilih Warna Pen")
        if color[1]:  # Jika user tidak cancel
            self.pen_color = color[1]
            self.update_info()

    def ubah_ukuran(self, value):
        """Event handler untuk mengubah ukuran pen"""
        self.pen_size = int(value)
        self.update_info()

    def clear_canvas(self):
        """Event handler untuk membersihkan canvas"""
        if messagebox.askyesno("Konfirmasi", "Hapus semua gambar?"):
            self.canvas.delete("all")

    def update_info(self):
        """Method untuk update info di toolbar"""
        self.info_label.config(
            text=f"Warna: {self.pen_color} | Ukuran: {self.pen_size}"

        )    

    def bind_events(self):
        """Method untuk binding semua events"""
        # Mouse events untuk menggambar
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Mouse events untuk info posisi
        self.canvas.bind("<Motion>", self.show_position)

        # Keyboard events
        self.window.bind("<Control-s>", self.save_image)
        self.window.bind("<Control-o>", self.open_image)
        self.window.bind("<Control-n>", self.new_canvas)

        # Window events
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_draw(self, event):
        """Event handler saat mulai menggambar (mouse press)"""
        self.last_x = event.x
        self.last_y = event.y
        self.is_drawing = True

    def draw(self, event):
        """Event handler saat menggambar (mouse drag)"""
        if self.is_drawing and self.last_x and self.last_y:
            # Gambar garis dari posisi terakhir ke posisi sekarang
            self.canvas.create_line(
                self.last_x, self.last_y,
                event.x, event.y,
                width=self.pen_size,
                fill=self.pen_color,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        """Event handler saat berhenti menggambar (mouse release)"""
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def show_position(self, event):
        """Event handler untuk menampilkan posisi mouse"""
        if hasattr(self, 'pos_label'):
            self.pos_label.destroy()

        self.pos_label = tk.Label(
            self.window,
            text=f"Posisi: ({event.x}, {event.y})",
            bg="yellow"
        )
        self.pos_label.place(x=event.x + 10, y=event.y + 10)

        # Hapus label setelah 1 detik
        self.window.after(1000, lambda: self.pos_label.destroy() if hasattr(self, 'pos_label') else None)

    def save_image(self, event=None):
        """Event handler untuk save (Ctrl+S)"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
        )
        if filename:
            self.canvas.postscript(file=filename)
            messagebox.showinfo("Info", f"Gambar disimpan sebagai {filename}")

    def open_image(self, event=None):
        """Event handler untuk open (Ctrl+O)"""
        messagebox.showinfo("Info", "Fitur buka gambar belum diimplementasi")

    def new_canvas(self, event=None):
        """Event handler untuk canvas baru (Ctrl+N)"""
        if messagebox.askyesno("Canvas Baru", "Buat canvas baru? Gambar saat ini akan hilang."):
            self.canvas.delete("all")

    def on_closing(self):
        """Event handler saat jendela akan ditutup"""
        if messagebox.askokcancel("Keluar", "Yakin ingin keluar? Gambar yang belum disimpan akan hilang."):
            self.window.destroy()

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = PaintApp()
    app.jalankan()