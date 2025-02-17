from src.qr_generator import QrGenerator
import os
import sys

def hello(name):
    return f'hola {name}'

def main():
    url = input("url: ")
    qr = QrGenerator()
    qr.setLogoByPath("app_icon_wb.png")
    qr.getImageQr(url)

if __name__ == '__main__':
    main()