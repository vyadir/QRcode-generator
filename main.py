# Librerías necesarias
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Menu
from ttkthemes import ThemedTk
import qrcode
from PIL import Image, ImageTk
import webbrowser
import io
import win32clipboard

# Clase para crear tooltips
class Tooltip:
    def __init__(self, widget, text):
        # Constructor de la clase Tooltip.
        # widget: El widget al que se asociará el tooltip.
        # text: El texto que se mostrará en el tooltip.
        self.widget = widget  # Almacenar la referencia al widget.
        self.text = text      # Almacenar el texto del tooltip.
        self.tooltip = None   # Inicializar la variable tooltip a None. Esta variable almacenará el tooltip cuando se cree.
        # Vincular el evento de movimiento del ratón al widget.
        # Cuando el ratón se mueva sobre el widget, se llamará a self.enter.
        self.widget.bind("<Motion>", self.enter)
        # Vincular el evento de salida del ratón del widget.
        # Cuando el ratón salga del widget, se llamará a self.leave.
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        # Método llamado cuando el ratón se mueve sobre el widget.
        if not self.tooltip:
            # Si el tooltip no existe aún (es decir, es la primera vez que se mueve el ratón sobre el widget):
            # Calcular la posición en la pantalla donde se mostrará el tooltip.
            # Se suma 20 píxeles para desplazar ligeramente el tooltip y evitar que el cursor lo cubra.
            x = self.widget.winfo_rootx() + event.x + 20
            y = self.widget.winfo_rooty() + event.y + 20
            # Crear un nuevo widget Toplevel para el tooltip.
            # Este widget es una pequeña ventana que se mostrará encima de otros widgets.
            self.tooltip = tk.Toplevel(self.widget)
            # Configurar el widget tooltip para que no tenga decoraciones de ventana (como bordes o barra de título).
            self.tooltip.wm_overrideredirect(True)
            # Establecer la geometría del tooltip (su posición en la pantalla).
            self.tooltip.wm_geometry(f"+{x}+{y}")
            # Crear y empaquetar un widget Label dentro del tooltip para mostrar el texto.
            # Configurar el fondo a amarillo y el borde a sólido.
            label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1, font=("Arial", "10", "normal"))
            label.pack()

    def leave(self, event=None):
        # Método llamado cuando el ratón sale del widget.
        if self.tooltip:
            # Si existe un tooltip (el ratón había entrado antes en el widget y había creado un tooltip):
            # Destruir el tooltip para ocultarlo.
            self.tooltip.destroy()
            # Restablecer la variable tooltip a None para indicar que ya no hay un tooltip activo.
            self.tooltip = None

# Clase modelo para la generación y guardado del código QR
class QRCodeModel:
    def __init__(self):
        # Constructor de la clase QRCodeModel.
        self.last_qr_image = None  # Inicializa una variable para almacenar la última imagen de código QR generada.
        self.qr_data = ""          # Inicializa una variable para almacenar los datos (texto) del código QR.

    def generate_qr(self, data):
        # Método para generar un código QR a partir de los datos proporcionados.
        self.qr_data = data  # Almacena los datos del QR en la variable qr_data.
        # Crea una nueva instancia de QRCode con configuraciones específicas.
        # version=1 indica el tamaño del QR, box_size controla el tamaño de cada caja del QR,
        # y border define el borde alrededor del código QR.
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        # Añade los datos proporcionados al código QR.
        qr.add_data(data)
        # Genera el código QR.
        qr.make(fit=True)
        # Crea una imagen a partir del QR generado, con un relleno negro y fondo blanco.
        self.last_qr_image = qr.make_image(fill='black', back_color='white')
        # Devuelve la imagen generada.
        return self.last_qr_image

    def save_qr(self, file_path):
        # Método para guardar la imagen del código QR en un archivo.
        if self.last_qr_image and file_path:
            # Si hay una imagen de código QR generada y se proporcionó una ruta de archivo:
            # Guarda la imagen del código QR en la ruta especificada en formato PNG.
            self.last_qr_image.save(file_path, 'PNG')
            # Devuelve True para indicar que el guardado fue exitoso.
            return True
        # Si no hay una imagen de código QR o no se proporcionó una ruta de archivo,
        # devuelve False para indicar que el guardado no fue exitoso.
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
        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=5)
        self.image_label.bind("<Button-3>", self.show_context_menu)  # Vincular menú contextual
        self.button = ttk.Button(self, text="Generar QR", command=self.on_generate)
        self.button.pack(pady=5)
        self.add_tooltip(self.button, "Generar código QR")
        self.save_button = ttk.Button(self, text="Guardar como PNG", command=self.on_save)
        self.save_button.pack(pady=5)
        self.add_tooltip(self.save_button, "Guardar QR como imagen PNG")
        self.whatsapp_button = ttk.Button(self, text="Abrir WhatsApp Web", command=self.open_whatsapp_web)
        self.whatsapp_button.pack(pady=5)
        self.add_tooltip(self.whatsapp_button, "Abrir WhatsApp Web para enviar el QR")

    def show_context_menu(self, event):
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Copiar imagen", command=self.copy_image_to_clipboard)
        context_menu.tk_popup(event.x_root, event.y_root)

    def copy_image_to_clipboard(self):
        if self.controller.model.last_qr_image:
            # Convertir la imagen PIL a formato DIB (Device Independent Bitmap)
            output = io.BytesIO()
            self.controller.model.last_qr_image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]  # El archivo BMP tiene un encabezado de 14 bytes que debe ser removido
            output.close()
            win32clipboard.OpenClipboard()  # Abrir el portapapeles
            win32clipboard.EmptyClipboard()  # Limpiar el portapapeles
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # Copiar la imagen
            win32clipboard.CloseClipboard()  # Cerrar el portapapeles
            messagebox.showinfo("Información", "Imagen del código QR copiada al portapapeles.")
        else:
            messagebox.showerror("Error", "No hay imagen del QR para copiar.")
    
    def display_qr(self, img):
        img = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=img)
        self.image_label.image = img
        self.create_context_menu()
        # Crear tooltip para la imagen
        Tooltip(self.image_label, "Copiar imagen al portapapeles (Click derecho & Copiar)") 


    def create_context_menu(self):
        # Crear menú contextual
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copiar imagen", command=self.copy_image_to_clipboard)

        # Vincular el menú contextual con la etiqueta del QR
        self.image_label.bind("<Button-3>", self.show_context_menu)
    # abre whatsapp web 
    def open_whatsapp_web(self):
        webbrowser.open('https://web.whatsapp.com')
    # menu bar del app
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    # about del menu bar
    def show_about(self):
        messagebox.showinfo("Acerca de", "Generador de Código QR\n© 2023 Yadir Vega Espinoza")

    def add_tooltip(self, widget, text):
        Tooltip(widget, text)

    def on_generate(self):
        data = self.entry.get()
        if data:
            self.controller.generate_qr(data)
        else:
            messagebox.showerror("Error", "Por favor, ingrese algún texto para generar el QR.")

    def on_save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            success = self.controller.save_qr(file_path)
            if success:
                messagebox.showinfo("Guardar QR", "El código QR se guardó exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar el código QR.")

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
