# Importaciones necesarias
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

# Clase modelo para la generación y guardado del código QR
class QRCodeModel:
    def __init__(self):
        # Inicializar variable para almacenar la última imagen del código QR generada
        self.last_qr_image = None

    def generate_qr(self, data):
        # Generar un código QR a partir de los datos proporcionados
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        self.last_qr_image = qr.make_image(fill='black', back_color='white')
        return self.last_qr_image

    def save_qr(self, file_path):
        # Guardar la última imagen del código QR en el archivo especificado
        if self.last_qr_image and file_path:
            self.last_qr_image.save(file_path, 'PNG')
            return True
        return False

# Clase vista para la interfaz de usuario
class QRCodeView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Configurar la interfaz de usuario y crear los widgets
        self.configure_ui()
        self.create_widgets()

    def configure_ui(self):
        # Configurar aspectos básicos de la ventana
        self.title("Generador de Código QR")
        self.geometry("800x600")  # Tamaño de la ventana
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Tema para los widgets
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))

    def create_widgets(self):
        # Crear y colocar los widgets en la ventana
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(pady=10)

        self.button = ttk.Button(self, text="Generar QR", command=self.on_generate)
        self.button.pack(pady=5)

        self.save_button = ttk.Button(self, text="Guardar como PNG", command=self.on_save)
        self.save_button.pack(pady=5)

        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=5)

    def on_generate(self):
        # Obtener los datos y generar el código QR
        data = self.entry.get()
        if data:
            self.controller.generate_qr(data)
        else:
            messagebox.showerror("Error", "Por favor, ingrese algún texto para generar el QR.")

    def on_save(self):
        # Abrir un diálogo para guardar el archivo y guardar el código QR
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            success = self.controller.save_qr(file_path)
            if success:
                messagebox.showinfo("Guardar QR", "El código QR se guardó exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar el código QR.")

    def display_qr(self, img):
        # Mostrar el código QR en la interfaz de usuario
        img = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=img)
        self.image_label.image = img

# Clase controlador para manejar la interacción entre la vista y el modelo
class QRCodeController:
    def __init__(self):
        self.model = QRCodeModel()
        self.view = QRCodeView(self)

    def generate_qr(self, data):
        # Generar el código QR y mostrarlo en la vista
        img = self.model.generate_qr(data)
        self.view.display_qr(img)

    def save_qr(self, file_path):
        # Guardar el código QR y devolver el resultado del proceso
        return self.model.save_qr(file_path)

    def run(self):
        # Iniciar la interfaz de usuario
        self.view.mainloop()

# Punto de entrada del programa
if __name__ == "__main__":
    controller = QRCodeController()
    controller.run()
