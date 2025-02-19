import sqlite3
from src.qr_generator import QrGenerator

def hello(name):
    return f'hola {name}'

def main():
    
    conexion = sqlite3.connect("db.sqlite")
    url = input("url: ")
    qr = QrGenerator(conexion)
    qr.setLogoByPath("app_icon_wb.png")
    qr.getImageQr(url)

if __name__ == '__main__':
    main()