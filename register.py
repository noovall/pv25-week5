import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QVBoxLayout, QFormLayout, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

class FormApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.age_input = QLineEdit()
        
        self.phone_input = QLineEdit()
        self.phone_input.setText("+62 ")
        self.phone_input.setReadOnly(False)
        
        regex = QRegExp(r"\+62\s\d{0,3}-?\d{0,4}-?\d{0,4}")
        validator = QRegExpValidator(regex)
        self.phone_input.setValidator(validator)
        self.phone_input.textChanged.connect(self.format_phone_number)
        
        self.address_input = QTextEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Pilih Jenis Kelamin", "Pria", "Wanita"])
        self.education_input = QComboBox()
        self.education_input.addItems(["Pilih Pendidikan", "SLTA/sederajat", "S1", "S2"])
        
        form_layout.addRow("Nama:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Umur:", self.age_input)
        form_layout.addRow("Nomor Telp.:", self.phone_input)
        form_layout.addRow("Alamat:", self.address_input)
        form_layout.addRow("Jenis Kelamin:", self.gender_input)
        form_layout.addRow("Pendidikan:", self.education_input)
      
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.clear_button = QPushButton("Clear")
        
        self.save_button.clicked.connect(self.save_data)
        self.clear_button.clicked.connect(self.clear_fields)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.nim_label = QLabel("Lalu Muhammad Noval Adipratama (F1D022056)")
        layout.addWidget(self.nim_label)
        
        self.setLayout(layout)
        self.setWindowTitle("Form Validation")
        self.setGeometry(200, 200, 600, 500)
    
    def format_phone_number(self):
        text = self.phone_input.text()
        if not text.startswith("+62 "):
            self.phone_input.setText("+62 ")
        
        numbers = text.replace("+62 ", "").replace("-", "").strip()
        format = "+62 "
        
        if len(numbers) > 3:
            format += numbers[:3] + "-"
            numbers = numbers[3:]
        if len(numbers) > 4:
            format += numbers[:4] + "-"
            numbers = numbers[4:]
        format += numbers
        
        self.phone_input.setText(format)
    
    def save_data(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        age = self.age_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()
        gender = self.gender_input.currentText()
        education = self.education_input.currentText()
        
        if not name:
            self.show_error("Isi Nama Anda")
            return
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            self.show_error("Format email salah")
            return
        
        if not age.isdigit():
            self.show_error("Umur harus angka")
            return
        
        age = int(age)
        if age < 18 or age > 100:
            self.show_error("Umur harus antara 18 dan 100")
            return
        
        if not re.match(r"^\+62\s\d{3}-\d{4}-\d{4}$", phone):
            self.show_error("Nomor Telp. harus dengan format: +62 999-9999-9999")
            return
        
        if not address:
            self.show_error("Alamat tidak boleh kosong")
            return
        
        if gender == "Pilih Jenis Kelamin":
            self.show_error("Silahkan pilih jenis kelamin anda")
            return
        
        if education == "Pilih Pendidikan":
            self.show_error("Silahkan pilih pendidikan anda")
            return
        
        QMessageBox.information(self, "Sukses", "Data Tersimpan")
        self.clear_fields()
    
    def show_error(self, message):
        QMessageBox.warning(self, "Validasi Eror", message)
    
    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()
        self.phone_input.setText("+62 ")
        self.address_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.education_input.setCurrentIndex(0)
    
    def keyPressEvent(self, event):
        if event.key() == ord('Q'):
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormApp()
    window.show()
    sys.exit(app.exec_())
