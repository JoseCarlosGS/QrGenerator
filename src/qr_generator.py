"""_summary_
    """
import os
from datetime import datetime
import qrcode as QR
from PIL import Image
from .exceptions.logo_error import LogoError
from .exceptions.logo_error import ArchivoInvalidoError
from .repository import crear_tabla_metadatos, guardar_metadatos
from .logo_processor import process_logo_for_qr
import uuid

class QrGenerator():
    """Generador de QR en formato imagen
    """
    def __init__(self, db_conexion = None):
        self.logo = None
        self.conexion = db_conexion
        self.qr = QR.QRCode(
            version=1,  # Controla el tamaño del código QR (1 es el más pequeño)
            error_correction=QR.constants.ERROR_CORRECT_H,  # Nivel de corrección de errores
            box_size=10,  # Tamaño de cada "caja" en el código QR
            border=4,  # Ancho del borde (mínimo 4 según la especificación QR)
        )
        self.output_dir = "out"  # Carpeta donde se guardarán los archivos
        # Crear la carpeta si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
    def setLogoByPath(self, path):
        """Cargar el logo para el QR a partir del path del archivo

        Args:
            path (str): Ruta del archivo del logo.

        Raises:
            LogoError: Si el archivo no existe.
            ArchivoInvalidoError: Si el archivo no es una imagen válida.
        """
        if not os.path.exists(path):
            raise LogoError(f"El archivo '{path}' no existe o la ruta es incorrecta")
        try:
            with Image.open(path) as img:
                img.verify()  # Verifica si es una imagen válida sin cargarla 
            self.logo = process_logo_for_qr(logo_file=Image.open(path))   
            print("Logo cargado con exito")     
        except Exception:
            raise ArchivoInvalidoError(f"El archivo '{path}' no es una imagen válida.")
        
    
    def getImageQr(self, data):
        """Obtener el codigo QR en formato imagen png

        Args:
            data (str): Datos a almacenar en el QR
        """
        #Metadatos
        author = "Tu Nombre"
        created_at = datetime.now().isoformat()
        description = "Código QR para la página principal"
        
        qr_id = str(uuid.uuid4()) 
        
        if self.conexion is not None:
            crear_tabla_metadatos(self.conexion)
            guardar_metadatos(self.conexion, qr_id, data, author, created_at, description)
        
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"{qr_id}_{timestamp}.png")
        self.qr.add_data(data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color = "black", back_color="white").convert("RGB")

        if self.logo is not None:
            logo_size = 80
            self.logo = self.logo.resize((logo_size, logo_size))
            qr_width, qr_height = img.size
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(self.logo, logo_position, self.logo)
            
        img.save(filename)

        print(f"Código QR generado y guardado {filename}")
    

#data = "www.google.com"







