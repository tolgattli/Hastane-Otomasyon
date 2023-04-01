from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QMessageBox, QDialog, QInputDialog, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Patient Complaint Form")
        self.setFixedSize(500, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.doctor_window = None

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.age_label = QLabel("Age:")
        self.age_input = QComboBox()
        self.age_input.addItems([str(i) for i in range(1, 101)])

        self.complaint_label = QLabel("Complaint:")
        self.complaint_input = QTextEdit()

        self.doctor_label = QLabel("Doctor:")
        self.doctor_input = QComboBox()
        self.doctor_input.addItems(
            ["Dr. John Doe", "Dr. Jane Smith", "Dr. Michael Lee"])

        self.doctor_button = QPushButton("I am a doctor")
        self.submit_button = QPushButton("Submit")

        self.doctor_button.clicked.connect(self.doctor_login)
        self.submit_button.clicked.connect(self.submit)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.name_label, 0, 0)
        grid_layout.addWidget(self.name_input, 0, 1)
        grid_layout.addWidget(self.age_label, 1, 0)
        grid_layout.addWidget(self.age_input, 1, 1)
        grid_layout.addWidget(self.complaint_label, 2, 0)
        grid_layout.addWidget(self.complaint_input, 2, 1)
        grid_layout.addWidget(self.doctor_label, 3, 0)
        grid_layout.addWidget(self.doctor_input, 3, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.doctor_button)
        button_layout.addWidget(self.submit_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

    def submit(self):
        name = self.name_input.text()
        age = self.age_input.currentText()
        complaint = self.complaint_input.toPlainText()
        doctor = self.doctor_input.currentText()

        message_box = QMessageBox()
        message_box.setText(
            f"Name: {name}\nAge: {age}\nComplaint: {complaint}\nDoctor: {doctor}")
        message_box.exec_()

    def doctor_login(self):
        password, ok = QInputDialog.getText(
            self, 'Doctor Login', 'Enter password:', QLineEdit.Password)

        if ok and password == "123":
            self.setEnabled(False)
            self.doctor_window = DoctorWindow(self)
            self.doctor_window.closed.connect(self.doctor_closed)
            # doctor_window = DoctorWindow(self)
            self.doctor_window.show()

    def doctor_closed(self):
        self.setEnabled(True)
        self.doctor_window = None


class DoctorWindow(QDialog):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Doctor Panel")
        self.setFixedSize(700, 400)

        self.appointments_label = QLabel("Appointments:")
        self.appointments_list = QListWidget()
        self.show_appointment_button = QPushButton("Show Appointment")
        self.show_appointment_button.clicked.connect(self.show_appointment)
        self.delete_appointment_button = QPushButton("Delete Appointment")
        self.delete_appointment_button.clicked.connect(self.delete_appointment)


        self.doctors_label = QLabel("Doctors:")
        self.doctors_list = QListWidget()
        self.add_doctor_button = QPushButton("Add Doctor")
        self.add_doctor_button.clicked.connect(self.add_doctor)
        self.delete_doctor_button = QPushButton("Delete Doctor")
        self.delete_doctor_button.clicked.connect(self.delete_doctor)
        self.show_doctor_button = QPushButton("Show Doctor")
        self.show_doctor_button.clicked.connect(self.show_doctor)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit)

        layout = QVBoxLayout()

        doctor_buttons = QHBoxLayout()
        appt_buttons = QHBoxLayout()

        doctor_buttons.addWidget(self.show_doctor_button)
        doctor_buttons.addWidget(self.add_doctor_button)
        doctor_buttons.addWidget(self.delete_doctor_button)
        
        appt_buttons.addWidget(self.delete_appointment_button)
        appt_buttons.addWidget(self.show_appointment_button)

        layout.addWidget(QLabel("Doctor Panel"))
        layout.addWidget(self.appointments_label)
        layout.addWidget(self.appointments_list)
        layout.addLayout(appt_buttons)
        layout.addWidget(self.doctors_label)
        layout.addWidget(self.doctors_list)
        layout.addLayout(doctor_buttons)
        # layout.addWidget(self.delete_appointment_button)
        # # layout.addWidget(self.add_doctor_button)
        # layout.addWidget(self.delete_doctor_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def delete_appointment(self):
        selected_appointment = self.appointments_list.currentItem()
        if selected_appointment is not None:
            message_box = QMessageBox()
            message_box.setText(
                f"Are you sure you want to delete appointment:\n{selected_appointment.text()}?")
            message_box.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Cancel)
            result = message_box.exec_()
            if result == QMessageBox.Yes:
                self.appointments_list.takeItem(
                    self.appointments_list.row(selected_appointment))

    def show_appointment(self):
        #appointment oluştururken girilen bilgilerin aynısı message box ile gösterilecek
        pass

    def add_doctor(self):
        new_doctor, ok = QInputDialog.getText(
            self, "Add Doctor", "Enter doctor name:")
        if ok and new_doctor.strip() != "":
            self.doctors_list.addItem(new_doctor)

    def delete_doctor(self):
        selected_doctor = self.doctors_list.currentItem()
        if selected_doctor is not None:
            message_box = QMessageBox()
            message_box.setText(
                f"Are you sure you want to delete doctor:\n{selected_doctor.text()}?")
            message_box.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Cancel)
            result = message_box.exec_()
            if result == QMessageBox.Yes:
                self.doctors_list.takeItem(
                    self.doctors_list.row(selected_doctor))

    def show_doctor(self):
        # message box çıkıcak doktorun özelliklerini söylicek yaş, cinsiyet gibi
        pass

    def exit(self):
        self.closed.emit()
        # self.parent().setEnabled(True)
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
