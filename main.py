#Librerías necesarias
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import qrcode
from PIL import Image, ImageTk
import webbrowser

# Clase para crear tooltips
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1, font=("Arial", "10", "normal"))
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            
# Clase modelo para la generación y guardado del código QR
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
        if self.last_qr_image and file_path:
            self.last_qr_image.save(file_path, 'PNG')
            return True
        return False

# Clase vista para la interfaz de usuario
class QRCodeView(ThemedTk):
    def __init__(self, controller):
        super().__init__(theme="arc")  # Usando el tema 'arc'
        self.controller = controller

        self.configure_ui()
        self.create_widgets()
        self.create_menu()

    def configure_ui(self):
        self.title("Generador de Código QR")
        self.geometry("800x600")  # Tamaño de la ventana
        # Centrar la ventana en la pantalla
        screen_width = self.winfo_screenwidth()   # Ancho de la pantalla
        screen_height = self.winfo_screenheight() # Alto de la pantalla
        x = (screen_width / 2) - (800 / 2)        # Posición X
        y = (screen_height / 2) - (600 / 2)       # Posición Y
        self.geometry(f'+{int(x)}+{int(y)}')      # Establecer posición
        self.resizable(False, False)

    def create_widgets(self):
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(pady=10)
        self.button = ttk.Button(self, text="Generar QR", command=self.on_generate)
        self.button.pack(pady=5)
        self.add_tooltip(self.button, "Generar código QR")
        self.save_button = ttk.Button(self, text="Guardar como PNG", command=self.on_save)
        self.save_button.pack(pady=5)
        self.add_tooltip(self.save_button, "Guardar QR como imagen PNG")
        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=5)
        self.whatsapp_button = ttk.Button(self, text="Abrir WhatsApp Web", command=self.open_whatsapp_web)
        self.whatsapp_button.pack(pady=5)
        self.add_tooltip(self.whatsapp_button, "Abrir WhatsApp Web para enviar el QR")

    def open_whatsapp_web(self):
        webbrowser.open('https://web.whatsapp.com')

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)

    def show_about(self):
        messagebox.showinfo("Acerca de", "Generador de Código QR\n© 2023 Yadir Vega Espinoza")

    # Método modificado para agregar tooltip
    def add_tooltip(self, widget, text):
        Tooltip(widget, text)

    def on_generate(self):
        data = self.entry.get()
        if data:
            self.controller.generate_qr(data)
        else:
            messagebox.showerror("Error", "Por favor, ingrese algún texto para generar el QR.")

    def on_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png")])
        if file_path:
            success = self.controller.save_qr(file_path)
            if success:
                messagebox.showinfo("Guardar QR", "El código QR se guardó exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar el código QR.")

    def display_qr(self, img):
        img = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=img)
        self.image_label.image = img

# Clase controlador para manejar la interacción entre la vista y el modelo
class QRCodeController:
    def __init__(self):
        self.model = QRCodeModel()
        self.view = QRCodeView(self)

    def generate_qr(self, data):
        img = self.model.generate_qr(data)
        self.view.display_qr(img)

    def save_qr(self, file_path):
        return self.model.save_qr(file_path)

    def run(self):
        self.view.mainloop()

# Punto de entrada del programa
if __name__ == "__main__":
    controller = QRCodeController()
    controller.run()
