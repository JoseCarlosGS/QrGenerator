
class LogoError(Exception):
    """Excepción personalizada para errores de logo."""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        
class ArchivoInvalidoError(Exception):
    """Excepción para archivos que no son imágenes válidas."""
    def __init__(self, mensaje):
        super().__init__(mensaje)