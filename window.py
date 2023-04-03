import sys
from PyQt5 import QtWidgets


def Window():  # Arayüz iskeleti oluşturuldu
    app = QtWidgets.QApplication(sys.argv) # Uygulama widgeti oluşturuldu ve sisteme gönderildi.

    widgetWindow = QtWidgets.QWidget()  # Pencere oluşturuldu

    widgetWindow.setWindowTitle("Hastane Otomasyonu")  #Title Belirlendi

    widgetWindow.show()  # Ekrana yansıtıldı

    sys.exit(app.exec_())  # Uygulamadan çarpı tuşuna basmadığımız sürece uygulama çalışacak // yani uygulama döngüye girecek ve daima çalışacak.



if __name__ == "__main__":
    Window()  # Çalıştırıldı.