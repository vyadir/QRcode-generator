import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

class QRCodeModel:
    def __init__(self):
        self.last_qr_image = None

    def generate_qr(self, data):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        self.last_qr_image = qr.make_image(fill='black', back_color='white')
        return self.last_qr_image

    def save_qr(self, file_path):
        if self.last_qr_image:
            self.last_qr_image.save(file_path, 'PNG')

class QRCodeView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.configure_ui()
        self.create_widgets()

    def configure_ui(self):
        self.title("Generador de Código QR")
        self.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))

    def create_widgets(self):
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(pady=10)

        self.button = ttk.Button(self, text="Generar QR", command=self.on_generate)
        self.button.pack(pady=5)

        self.save_button = ttk.Button(self, text="Guardar como PNG", command=self.on_save)
        self.save_button.pack(pady=5)

        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=5)

    def on_generate(self):
        data = self.entry.get()
        if data:
            self.controller.generate_qr(data)
        else:
            messagebox.showerror("Error", "Por favor, ingrese algún texto para generar el QR.")

    def on_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            self.controller.save_qr(file_path)

    def display_qr(self, img):
        img = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=img)
        self.image_label.image = img

class QRCodeController:
    def __init__(self):
        self.model = QRCodeModel()
        self.view = QRCodeView(self)

    def generate_qr(self, data):
        img = self.model.generate_qr(data)
        self.view.display_qr(img)

    def save_qr(self, file_path):
        self.model.save_qr(file_path)

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    controller = QRCodeController()
    controller.run()
