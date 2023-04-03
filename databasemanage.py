from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QMessageBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # QListWidget ve düğmeleri içeren bir yatay düzen oluşturun
        layout = QHBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        layout2 = QVBoxLayout()
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.show_selected)
        self.show_button = QPushButton("Show Doctor")
        self.show_button.clicked.connect(self.show_doctor)
        layout2.addWidget(self.select_button)
        layout2.addWidget(self.show_button)
        layout.addLayout(layout2)
        self.setLayout(layout)

        # QListWidget'e öğeler ekleyin
        self.list_widget.addItem("Doctor A")
        self.list_widget.addItem("Doctor B")
        self.list_widget.addItem("Doctor C")

        self.show()

    def show_selected(self):
        # Seçilen öğeyi alın ve seçilmiş olarak işaretleyin
        item = self.list_widget.currentItem()
        item.setSelected(True)

    def show_doctor(self):
        # Seçilen öğenin bilgilerini görüntüleyen bir mesaj kutusu gösterin
        item = self.list_widget.currentItem()
        if item is not None:
            message_box = QMessageBox()
            message_box.setText(f"You selected {item.text()}")
            message_box.exec_()

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    app.exec_()
