from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QMessageBox, QDialog, QInputDialog, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("patient.db")
        self.cursor = self.con.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS patient (name TEXT, age TEXT, complaint TEXT, doctor TEXT)")
        self.con.commit()

        # self.condr = sqlite3.connect("doctorpanel.db")
        # self.cursordb = self.condr.cursor()
        # self.cursordb.execute("CREATE TABLE IF NOT EXISTS doctor (name TEXT, appointment TEXT, information TEXT)")

        self.setWindowTitle("Patient Complaint Form")
        self.setFixedSize(500, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.doctor_window = None

        self.name_label = QLabel("Full Name:")
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

        self.doctor_button = QPushButton("Login as doctor")
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
        age = (self.age_input.currentText())
        complaint = self.complaint_input.toPlainText()
        doctor = self.doctor_input.currentText()

        if name == "" or complaint == "":
            message_box = QMessageBox()
            message_box.setText(
                "You entered an invalid value. Please check your appointment details")
            message_box.exec_()

            return

        self.add_appointment_database(name, age, complaint, doctor)

    def add_appointment_database(self, name, age, complaint, doctor):
        self.cursor.execute(
            "INSERT INTO patient VALUES(?,?,?,?)", (name, age, complaint, doctor))
        self.con.commit()

        message_box = QMessageBox()
        message_box.setText(
            "You have set up an appointment. Thank you for choosing our hospital.")
        message_box.exec_()

    def doctor_login(self):
        password, ok = QInputDialog.getText(
            self, 'Doctor Login', 'Enter password:', QLineEdit.Password)
        doctors = {'Dr. John Doe': '1234',
                   'Dr. Jane Smith': '4567', 'Dr. Michael Lee': '7890'}
        if ok and password in doctors.values():
            for doctor, pwd in doctors.items():
                if password == pwd:
                    self.setEnabled(False)
                    self.doctor_window = DoctorWindow(self, doctor)
                    self.doctor_window.closed.connect(self.doctor_closed)
                    self.doctor_window.show()
                    break
        else:
            QMessageBox.warning(self, 'Error', 'Invalid password!')

    def doctor_closed(self):
        self.setEnabled(True)
        self.doctor_window = None


class DoctorWindow(QDialog):
    closed = pyqtSignal()

    def __init__(self, parent=None, doctor=None):
        super().__init__(parent)
        self.setWindowTitle("Doctor Panel")
        self.setFixedSize(700, 400)
        self.doctor = doctor
        self.selectedAppointment = []

        self.appointments_label = QLabel("Appointments:")
        self.appointments_list = QListWidget()
        self.appointments_list.itemSelectionChanged.connect(
            self.setSelectedApp)
        self.show_appointment_button = QPushButton("Show Appointment")
        self.show_appointment_button.clicked.connect(
            self.show_appointment)
        self.delete_appointment_button = QPushButton("Delete Appointment")
        self.delete_appointment_button.clicked.connect(self.delete_appointment)
        self.appointments_list.addItems(self.setAppointments())

        self.doctorJohnDoe = """
        Dr. John Doe received his medical degree from Harvard Medical School in 2005.
        He completed his residency in internal medicine at Massachusetts General Hospital and is board-certified in internal medicine.
        Dr. Doe has been practicing medicine for over 15 years and is committed to providing his patients with the highest quality care."""
        self.doctorJaneSmith = """
        Dr. Jane Smith earned her medical degree from the University of California, San Francisco in 2010.
        She completed her residency in pediatrics at Children's Hospital Los Angeles and is board-certified in pediatrics.
        Dr. Smith has a passion for working with children and their families, and strives to make each visit a positive and comfortable experience."""
        self.doctorMichaelLee = """Dr. Michael Lee received his medical degree from Stanford University School of Medicine in 2008.
        He completed his residency in neurology at the University of California, San Francisco and is board-certified in neurology.
        Dr. Lee has a special interest in the treatment of migraines and other chronic headaches, and is dedicated to helping his patients achieve relief and improve their quality of life."""

        self.doctors_label = QLabel("Doctors:")
        self.doctors_list = QListWidget()
        self.doctors_list.addItem("Dr. John Doe")
        self.doctors_list.addItem("Dr. Jane Smith")
        self.doctors_list.addItem("Dr. Michael Lee")

        self.show_doctor_button = QPushButton("Show Doctor's Information")
        self.show_doctor_button.clicked.connect(self.show_doctor)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit)

        layout = QVBoxLayout()

        bottom_buttons = QHBoxLayout()
        appt_buttons = QHBoxLayout()

        bottom_buttons.addWidget(self.show_doctor_button)
        bottom_buttons.addWidget(self.exit_button)
        appt_buttons.addWidget(self.delete_appointment_button)
        appt_buttons.addWidget(self.show_appointment_button)

        layout.addWidget(QLabel("Doctor Panel"))
        layout.addWidget(self.appointments_label)
        layout.addWidget(self.appointments_list)
        layout.addLayout(appt_buttons)
        layout.addWidget(self.doctors_label)
        layout.addWidget(self.doctors_list)
        layout.addLayout(bottom_buttons)

        self.setLayout(layout)

    def delete_appointment(self):
        selected_appointment = self.appointments_list.currentItem()
        if selected_appointment is not None:
            message_box = QMessageBox()
            message_box.setText("Are you sure you want to delete appointment?")
            message_box.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Cancel)
            result = message_box.exec_()
            if result == QMessageBox.Yes:
                conn = sqlite3.connect('patient.db')
                c = conn.cursor()
                appointment_info = selected_appointment.text().split('\n')
                name = appointment_info[0].split(':')[1].strip()
                age = appointment_info[1].split(':')[1].strip()
                message = appointment_info[2].split(':')[1].strip()
                doctor = appointment_info[3].split(':')[1].strip()
                c.execute(
                    f"DELETE FROM patient WHERE Name='{name}' AND Age='{age}' AND Complaint='{message}' AND Doctor='{doctor}'")
                conn.commit()
                c.close()
                conn.close()
                self.appointments_list.takeItem(
                    self.appointments_list.row(selected_appointment))

    def setSelectedApp(self):
        self.selectedAppointment = self.appointments_list.selectedItems()[
            0].text()

    def setAppointments(self):
        listOfAppointments = []
        conn = sqlite3.connect('patient.db')
        cursor = conn.cursor()
        appointments = cursor.execute(
            f"SELECT * FROM patient WHERE doctor='{self.doctor}'")
        for appointment in appointments:
            item = f"{appointment[0]}"
            listOfAppointments.append(item)

        return listOfAppointments

    def show_appointment(self):
        conn = sqlite3.connect('patient.db')
        cursor = conn.cursor()
        a = []
        appointments = cursor.execute(
            f"SELECT * FROM patient WHERE doctor='{self.doctor}'")
        for appointment in appointments:
            if appointment[0] == self.selectedAppointment:
                pass
                a = list(appointment)
        if a != []:
            message_box = QMessageBox()
            message_box.setText(
                f"Full Name: {a[0]}\nAge: {a[1]}\nComplaint: {a[2]}\nDoctor: {a[3]}")
            message_box.exec_()

        conn.close()

    def show_doctor(self):
        selected_doctor = self.doctors_list.currentItem()
        if selected_doctor is not None:
            doctor_name = selected_doctor.text()
            if doctor_name == "Dr. John Doe":
                doctor_info = self.doctorJohnDoe
            elif doctor_name == "Dr. Jane Smith":
                doctor_info = self.doctorJaneSmith
            elif doctor_name == "Dr. Michael Lee":
                doctor_info = self.doctorMichaelLee

            message_box = QMessageBox()
            message_box.setWindowTitle(doctor_name)
            message_box.setText(doctor_info)
            message_box.exec_()

    def exit(self):
        self.closed.emit()
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
