import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask,
    ImageColorMask
)
from PIL import Image, ImageDraw

def crear_qr_personalizado(datos, 
                           qr_object,
                           estilo='redondeado',
                           color_estilo='solido',
                           color_qr=(0, 0, 0), 
                           color_fondo=(255, 255, 255),
                           color_gradiente=None,
                           tamano_modulo=10,
                           logo_file=None,
                           imagen_mascara=None):
    """
    Crea un código QR personalizado con diferentes estilos y opciones.
    
    Args:
        datos: Texto o URL para codificar en el QR
        qr_object: Objeto QR
        estilo: Forma de los módulos ('cuadrado', 'redondeado', 'circular', 'espaciado', 'barras_v', 'barras_h')
        color_estilo: Estilo de color ('solido', 'radial', 'horizontal', 'vertical', 'imagen')
        color_qr: Color principal del QR en formato RGB tuple (r,g,b)
        color_fondo: Color de fondo en formato RGB tuple (r,g,b)
        color_gradiente: Color externo para gradientes en formato RGB tuple (r,g,b) (opcional)
        tamano_modulo: Tamaño de cada módulo en píxeles
        logo_file: Imagen del logo a insertar (opcional)
        imagen_mascara: Ruta a una imagen para usar como máscara de color (opcional)
        
    Returns:
        Archivo generado
    """
    # Convertir colores de texto a RGB si es necesario
    color_qr = convert_color_to_rgb(color_qr)
    color_fondo = convert_color_to_rgb(color_fondo)
    
    if color_gradiente is None:
        color_gradiente = color_qr
    else:
        color_gradiente = convert_color_to_rgb(color_gradiente)
    
    # Crear el objeto QR
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_H,
    #     box_size=tamano_modulo,
    #     border=4,
    # )
    
    qr = qr_object
    
    qr.add_data(datos)
    qr.make(fit=True)
    
    # Seleccionar el estilo de módulo
    if estilo == 'redondeado':
        module_drawer = RoundedModuleDrawer()
    elif estilo == 'circular':
        module_drawer = CircleModuleDrawer()
    elif estilo == 'espaciado':
        module_drawer = GappedSquareModuleDrawer()
    elif estilo == 'barras_v':
        module_drawer = VerticalBarsDrawer()
    elif estilo == 'barras_h':
        module_drawer = HorizontalBarsDrawer()
    else:  # cuadrado por defecto
        module_drawer = SquareModuleDrawer()
    
    # Configurar colores y estilos
    try:
        if color_estilo == 'radial':
            color_mask = RadialGradiantColorMask(center_color=color_qr, edge_color=color_gradiente, back_color=color_fondo)
        elif color_estilo == 'horizontal':
            color_mask = HorizontalGradiantColorMask(left_color=color_qr, right_color=color_gradiente, back_color=color_fondo)
        elif color_estilo == 'vertical':
            color_mask = VerticalGradiantColorMask(top_color=color_qr, bottom_color=color_gradiente, back_color=color_fondo)
        elif color_estilo == 'imagen' and imagen_mascara:
            try:
                mask_image = Image.open(imagen_mascara)
                color_mask = ImageColorMask(back_color=color_fondo, mask_image=mask_image)
            except Exception as e:
                print(f"Error al cargar la imagen máscara: {e}")
                color_mask = None
        else:  # solido por defecto
            color_mask = None  # Usar colores predeterminados
        
        # Generar el código QR con los estilos seleccionados
        if color_mask:
            qr_image = qr.make_image(image_factory=StyledPilImage, 
                                    module_drawer=module_drawer,
                                    color_mask=color_mask)
        else:
            qr_image = qr.make_image(image_factory=StyledPilImage, 
                                    module_drawer=module_drawer,
                                    fill_color=color_qr, 
                                    back_color=color_fondo)
        
        # Insertar logo si se proporcionó
        if logo_file:
            try:
                # Cargar el logo
                # logo = Image.open(logo_path)
                logo = logo_file
                
                # Ajustar tamaño del logo (máximo 30% del tamaño del QR)
                qr_size = qr_image.size[0]
                logo_size = int(qr_size * 0.3)
                logo = logo.resize((logo_size, logo_size))
                
                # Calcular posición para centrar el logo
                position = ((qr_size - logo_size) // 2, (qr_size - logo_size) // 2)
                
                # Si el logo tiene canal alpha, usarlo como máscara
                if logo.mode == 'RGBA':
                    qr_image.paste(logo, position, logo)
                else:
                    qr_image.paste(logo, position)
                
            except Exception as e:
                print(f"Error al insertar el logo: {e}")
        
        # Guardar la imagen final
        # qr_image.save(ruta_salida)
        return qr_image
    
    except Exception as e:
        print(f"Error al generar el código QR: {e}")
        # Generar un QR básico en caso de error
        basic_qr = qr.make_image(fill_color="black", back_color="white")
        # basic_qr.save(ruta_salida)
        return basic_qr

def convert_color_to_rgb(color):
    """
    Convierte un color en formato string (#RRGGBB) o nombre a formato RGB tuple.
    También acepta ya un tuple RGB y lo devuelve sin cambios.
    """
    # Si ya es un tuple, devolverlo
    if isinstance(color, tuple) and len(color) in (3, 4):
        return color[:3]  # Asegurarse de que sea RGB (ignorar alpha si existe)
    
    # Si es un string con formato #RRGGBB
    if isinstance(color, str) and color.startswith('#'):
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    # Diccionario de nombres de colores comunes
    color_names = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'gray': (128, 128, 128)
    }
    
    # Si es un nombre de color conocido
    if isinstance(color, str) and color.lower() in color_names:
        return color_names[color.lower()]
    
    # Por defecto, devolver negro
    print(f"Color no reconocido: {color}. Usando negro como valor predeterminado.")
    return (0, 0, 0)

# if __name__ == "__main__":
#     # Ejemplo básico con módulos redondeados
#     crear_qr_personalizado(
#         datos="https://www.example.com",
#         estilo="redondeado",
#         ruta_salida="qr_redondeado.png"
#     )
    
#     # Ejemplo con gradiente radial y módulos circulares
#     crear_qr_personalizado(
#         datos="https://www.example.com",
#         estilo="circular",
#         color_estilo="radial",
#         color_qr=(0, 0, 255),  # Azul en el centro
#         color_gradiente=(0, 255, 255),  # Cian en los bordes
#         ruta_salida="qr_gradiente_radial.png"
#     )
    
#     # Ejemplo con barras verticales
#     crear_qr_personalizado(
#         datos="https://www.example.com",
#         estilo="barras_v",
#         color_qr=(255, 0, 0),  # Rojo
#         ruta_salida="qr_barras.png"
#     )