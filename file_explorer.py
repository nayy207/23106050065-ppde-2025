import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import shutil

class FileExplorer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Explorer - File Management Demo")
        self.window.geometry("800x600")
        self.window.configure(bg="lightsteelblue")

        # Variabel untuk menyimpan informasi file
        self.current_file = None
        self.current_directory = os.getcwd()
        self.selected_files = []

        self.buat_interface()
        self.update_directory_info()

    def buat_interface(self):
        # Header dengan informasi direktori
        header_frame = tk.Frame(self.window, bg="darkblue", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="FILE EXPLORER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="darkblue"
        ).pack(pady=15)

        # Frame untuk path dan navigasi
        nav_frame = tk.Frame(self.window, bg="lightgray", height=40)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Current Directory:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.path_label = tk.Label(
            nav_frame,
            text=self.current_directory,
            font=("Arial", 10),
            bg="lightgray",
            fg="blue",
            anchor="w"
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)

        # Toolbar dengan tombol operasi file
        toolbar = tk.Frame(self.window, bg="lightgray", relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X, padx=2, pady=2)

        # Tombol Open File
        btn_open = tk.Button(
            toolbar,
            text="📁 Open File",
            font=("Arial", 10),
            bg="lightblue",
            command=self.open_file,
            width=12
        )
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)

        # Tombol Open Directory
        btn_open_dir = tk.Button(
            toolbar,
            text="📂 Open Directory",
            font=("Arial", 10),
            bg="lightgreen",
            command=self.open_directory,
            width=15
        )
        btn_open_dir.pack(side=tk.LEFT, padx=2, pady=2)

        # Tombol Create File
        btn_create = tk.Button(
            toolbar,
            text="📄 Create File",
            font=("Arial", 10),
            bg="lightyellow",
            command=self.create_file,
            width=12
        )
        btn_create.pack(side=tk.LEFT, padx=2, pady=2)

        # Tombol Delete File
        btn_delete = tk.Button(
            toolbar,
            text="🗑 Delete",
            font=("Arial", 10),
            bg="lightcoral",
            command=self.delete_file,
            width=10
        )
        btn_delete.pack(side=tk.LEFT, padx=2, pady=2)

        # Tombol Refresh
        btn_refresh = tk.Button(
            toolbar,
            text="🔄 Refresh",
            font=("Arial", 10),
            bg="lightcyan",
            command=self.refresh_view,
            width=10
        )
        btn_refresh.pack(side=tk.LEFT, padx=2, pady=2)

        # Main content area
        content_frame = tk.Frame(self.window, bg="lightsteelblue")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame kiri untuk file list
        left_frame = tk.LabelFrame(
            content_frame,
            text="File Information",
            font=("Arial", 12, "bold"),
            bg="lightsteelblue"
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Text widget untuk menampilkan informasi file
        self.info_text = tk.Text(
            left_frame,
            font=("Courier", 10),
            bg="white",
            wrap=tk.WORD,
            height=15
        )

        # Scrollbar untuk info text
        info_scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)

        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        # Frame kanan untuk preview
        right_frame = tk.LabelFrame(
            content_frame,
            text="File Preview",
            font=("Arial", 12, "bold"),
            bg="lightsteelblue"
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Text widget untuk preview file
        self.preview_text = tk.Text(
            right_frame,
            font=("Courier", 9),
            bg="lightyellow",
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )

        # Scrollbar untuk preview
        preview_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)

        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

    def open_file(self):
        """Method untuk membuka file menggunakan file dialog"""
        # Definisikan jenis file yang didukung
        file_types = [
            ("Text files", "*.txt"),
            ("Python files", "*.py"),
            ("JSON files", "*.json"),
            ("CSV files", "*.csv"),
            ("All files", ".")
        ]

        # Tampilkan dialog open file
        filename = filedialog.askopenfilename(
            title="Select a file to open",
            filetypes=file_types,
            initialdir=self.current_directory
        )

        if filename:  # Jika user memilih file (tidak cancel)
            try:
                self.current_file = filename
                self.current_directory = os.path.dirname(filename)
                self.update_directory_info()
                self.show_file_info(filename)
                self.preview_file(filename)

                messagebox.showinfo("Success", f"File opened: {os.path.basename(filename)}")

            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {str(e)}")

    def show_file_info(self, filepath):
        """Method untuk menampilkan informasi detail file"""
        try:
            # Dapatkan informasi file
            stat_info = os.stat(filepath)
            file_size = stat_info.st_size
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            created_time = datetime.fromtimestamp(stat_info.st_ctime)

            # Format informasi
            info = f"""FILE INFORMATION
{'='*50}

File Name: {os.path.basename(filepath)}
Full Path: {filepath}
Directory: {os.path.dirname(filepath)}

File Size: {self.format_file_size(file_size)}
Extension: {os.path.splitext(filepath)[1] or 'No extension'}

Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}
Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}

Permissions:
- Readable: {'Yes' if os.access(filepath, os.R_OK) else 'No'}
- Writable: {'Yes' if os.access(filepath, os.W_OK) else 'No'}
- Executable: {'Yes' if os.access(filepath, os.X_OK) else 'No'}

File Type: {self.get_file_type(filepath)}
"""

            # Tampilkan di info text
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)

        except Exception as e:
            error_info = f"Error getting file information: {str(e)}"
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, error_info)

    def format_file_size(self, size_bytes):
        """Method untuk format ukuran file ke format yang mudah dibaca"""
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/1024**2:.1f} MB"
        else:
            return f"{size_bytes/1024**3:.1f} GB"

    def get_file_type(self, filepath):
        """Method untuk menentukan jenis file berdasarkan ekstensi"""
        extension = os.path.splitext(filepath)[1].lower()

        file_types = {
            '.txt': 'Text Document',
            '.py': 'Python Script',
            '.json': 'JSON Data',
            '.csv': 'CSV Data',
            '.html': 'HTML Document',
            '.css': 'CSS Stylesheet',
            '.js': 'JavaScript',
            '.jpg': 'JPEG Image',
            '.png': 'PNG Image',
            '.pdf': 'PDF Document',
            '.docx': 'Word Document',
            '.xlsx': 'Excel Spreadsheet'
        }

        return file_types.get(extension, 'Unknown File Type')
    
    def preview_file(self, filepath):
        """Method untuk preview isi file"""
        try:
            file_size = os.path.getsize(filepath)

            # Batasi preview untuk file besar
            if file_size > 1024 * 1024:  # 1MB
                preview_content = f"File too large for preview ({self.format_file_size(file_size)})\n"
                preview_content += "Please use appropriate application to view this file."
            else:
                # Coba baca file sebagai text
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()

                        # Batasi jumlah karakter yang ditampilkan
                        if len(content) > 5000:
                            preview_content = content[:5000] + "\n\n... (Content truncated for preview)"
                        else:
                            preview_content = content

                except UnicodeDecodeError:
                    # Jika tidak bisa dibaca sebagai text, coba sebagai binary
                    try:
                        with open(filepath, 'rb') as file:
                            binary_content = file.read(500)  # Baca 500 bytes pertama

                        preview_content = "Binary file detected. Showing first 500 bytes as hex:\n\n"
                        preview_content += ' '.join(f'{byte:02x}' for byte in binary_content)

                    except Exception:
                        preview_content = "Cannot preview this file type."

            # Tampilkan preview
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_content)
            self.preview_text.config(state=tk.DISABLED)

        except Exception as e:
            error_preview = f"Error previewing file: {str(e)}"
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, error_preview)
            self.preview_text.config(state=tk.DISABLED)

    def open_directory(self):
        """Method untuk membuka direktori menggunakan directory dialog"""
        directory = filedialog.askdirectory(
            title="Select a directory",
            initialdir=self.current_directory
        )

        if directory:
            try:
                self.current_directory = directory
                self.update_directory_info()
                self.show_directory_contents(directory)

                messagebox.showinfo("Success", f"Directory opened: {directory}")

            except Exception as e:
                messagebox.showerror("Error", f"Cannot open directory: {str(e)}")

    def show_directory_contents(self, directory):
        """Method untuk menampilkan isi direktori"""
        try:
            # Dapatkan daftar file dan folder
            items = os.listdir(directory)

            # Pisahkan folder dan file
            folders = []
            files = []

            for item in items:
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    folders.append(item)
                else:
                    files.append(item)

            # Sort alphabetically
            folders.sort()
            files.sort()

            # Format informasi direktori
            dir_info = f"""DIRECTORY CONTENTS
{'='*50}

Directory: {directory}
Total Items: {len(items)} ({len(folders)} folders, {len(files)} files)

FOLDERS ({len(folders)}):
{'-'*30}
"""

            for folder in folders:
                folder_path = os.path.join(directory, folder)
                try:
                    folder_size = self.get_directory_size(folder_path)
                    dir_info += f"📁 {folder} ({self.format_file_size(folder_size)})\n"
                except:
                    dir_info += f"📁 {folder} (Size unknown)\n"

            dir_info += f"\nFILES ({len(files)}):\n{'-'*30}\n"

            for file in files:
                file_path = os.path.join(directory, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_ext = os.path.splitext(file)[1]
                    dir_info += f"📄 {file} ({self.format_file_size(file_size)}) {file_ext}\n"
                except:
                    dir_info += f"📄 {file} (Size unknown)\n"

            # Tampilkan di info text
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, dir_info)

            # Clear preview
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, "Select a file to preview its contents")
            self.preview_text.config(state=tk.DISABLED)

        except Exception as e:
            error_info = f"Error reading directory: {str(e)}"
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, error_info)

    def get_directory_size(self, directory):
        """Method untuk menghitung ukuran total direktori"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        continue
        except:
            pass
        return total_size

    def update_directory_info(self):
        """Method untuk update informasi direktori di navigation bar"""
        self.path_label.config(text=self.current_directory)

    def create_file(self):
        """Method untuk membuat file baru"""
        # Dialog untuk memilih lokasi dan nama file
        filename = filedialog.asksaveasfilename(
            title="Create new file",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JSON files", "*.json"),
                ("All files", ".")
            ],
            initialdir=self.current_directory
        )

        if filename:
            try:
                # Buat file kosong
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write("")  # File kosong

                self.current_file = filename
                self.current_directory = os.path.dirname(filename)
                self.update_directory_info()
                self.show_file_info(filename)

                # Clear preview
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(1.0, "New empty file created")
                self.preview_text.config(state=tk.DISABLED)

                messagebox.showinfo("Success", f"File created: {os.path.basename(filename)}")

            except Exception as e:
                messagebox.showerror("Error", f"Cannot create file: {str(e)}")

    def delete_file(self):
        """Method untuk menghapus file"""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file selected for deletion!")
            return

        # Konfirmasi penghapusan
        filename = os.path.basename(self.current_file)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone."):
            try:
                os.remove(self.current_file)

                # Clear displays
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(1.0, "File deleted successfully")

                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(1.0, "No file selected")
                self.preview_text.config(state=tk.DISABLED)

                self.current_file = None

                messagebox.showinfo("Success", f"File '{filename}' has been deleted")

            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete file: {str(e)}")

    def refresh_view(self):
        """Method untuk refresh tampilan"""
        if self.current_file and os.path.exists(self.current_file):
            self.show_file_info(self.current_file)
            self.preview_file(self.current_file)
        elif os.path.exists(self.current_directory):
            self.show_directory_contents(self.current_directory)
        else:
            # Jika direktori tidak ada, kembali ke home directory
            self.current_directory = os.path.expanduser("~")
            self.update_directory_info()
            self.show_directory_contents(self.current_directory)

        messagebox.showinfo("Refresh", "View refreshed successfully")

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = FileExplorer()
    app.jalankan()