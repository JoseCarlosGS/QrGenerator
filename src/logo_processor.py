from PIL import Image, ImageDraw, ImageFilter, ImageOps

def process_logo_for_qr(logo_path='', output_size=150,    border_thickness=2, 
                        border_color="black", background_color="white", logo_file = None, quality_factor=4 ):
    """
    Procesa una imagen de logo para ser insertada en un código QR.
    
    Args:
        logo_path: Ruta al archivo de imagen del logo
        output_size: Tamaño final de la imagen del logo (sin contar el borde)
        border_thickness: Grosor del borde circular
        border_color: Color del borde
        background_color: Color del fondo circular
        
    Returns:
        PIL.Image: Imagen procesada lista para insertar en el QR
    """
    try:
        # Trabajar con tamaños internos mayores para preservar calidad
        internal_size = output_size * quality_factor
        internal_border = border_thickness * quality_factor
        # Cargar la imagen del logo
        if logo_file is not None:
            logo = logo_file
        else:
            logo = Image.open(logo_path)
        
        # Convertir a RGBA si no lo está ya
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Redimensionar el logo con alta calidad
        logo = ImageOps.contain(logo, (internal_size, internal_size), 
                                method=Image.LANCZOS)
        
        # Calcular dimensiones para centrar el logo
        logo_position = ((internal_size - logo.width) // 2, 
                         (internal_size - logo.height) // 2)
        
        # Crear una imagen cuadrada con fondo transparente
        base_img = Image.new("RGBA", (internal_size, internal_size), (0, 0, 0, 0))
        base_img.paste(logo, logo_position, logo)
        
        # Crear máscara circular con antialiasing
        mask = Image.new("L", (internal_size, internal_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, internal_size, internal_size), fill=255)
        
        # Suavizar la máscara para evitar bordes pixelados
        mask = mask.filter(ImageFilter.GaussianBlur(radius=quality_factor/2))
        
        # Aplicar máscara circular al logo
        logo_circular = Image.new("RGBA", (internal_size, internal_size), (0, 0, 0, 0))
        logo_circular.paste(base_img, (0, 0), mask)
        
        # Crear un fondo circular con el color especificado
        background = Image.new("RGBA", (internal_size, internal_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(background)
        draw.ellipse((0, 0, internal_size, internal_size), fill=background_color)
        
        # Combinar el logo circular con el fondo
        logo_with_background = Image.alpha_composite(background, logo_circular)
        
        # Crear la imagen final con borde
        final_size = internal_size + 2 * internal_border
        final_image = Image.new("RGBA", (final_size, final_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(final_image)
        
        # Dibujar el borde circular con antialiasing
        draw.ellipse((0, 0, final_size, final_size), fill=border_color)
        
        # Dibujar el fondo dentro del borde
        draw.ellipse((internal_border, internal_border,
                    final_size - internal_border, final_size - internal_border),
                    fill=background_color)
        
        # Pegar el logo circular sobre el fondo
        logo_position = (internal_border, internal_border)
        final_image.paste(logo_with_background, logo_position, logo_with_background)
        
        # Aplicar filtros para mejorar calidad
        final_image = final_image.filter(ImageFilter.SMOOTH_MORE)
        
        # Redimensionar al tamaño de salida manteniendo calidad
        target_size = output_size + 2 * border_thickness
        final_image = final_image.resize((target_size, target_size), 
                                         resample=Image.LANCZOS)
        
        return final_image
        
    except Exception as e:
        print(f"Error procesando el logo: {e}")
        return None


# if __name__ == "__main__":
#     # Procesar el logo
#     processed_logo = process_logo_for_qr(
#         logo_path="app_icon_wb.png",
#         output_size=100,
#         border_thickness=5,
#         border_color="black",
#         background_color="white"
#     )
    
#     if processed_logo:
#         # Para visualizar o guardar
#         processed_logo.save("logo_procesado.png")
#         # Para usar con el código QR
#         # qr_img.paste(processed_logo, position, processed_logo)