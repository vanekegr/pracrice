from PyQt5.QtWidgets import QMainWindow, QMessageBox
from database import DB
from paths import load_ui
from validators import validate_login, validate_password, validate_names


class _BaseRegistration(QMainWindow):
    TABLE = ""
    SUCCESS_MSG = "Регистрация прошла успешно"

    def __init__(self):
        super().__init__()
        load_ui(self, "Reg.ui")
        self.db = DB()
        self.pushButton.clicked.connect(self._on_register)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(20)
        self._populate()

    def _populate(self):
        pass

    def _collect_errors(self) -> list[str]:
        cur = self.db.cursor()
        login = self.lineEdit.text().strip()
        password = self.lineEdit_2.text()
        errors = validate_login(login, cur, self.TABLE)
        errors += validate_password(password)
        errors += validate_names(
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
        )
        return errors

    def _on_register(self):
        errors = self._collect_errors()
        if errors:
            QMessageBox.critical(self, "", "\n".join(errors))
            return
        self._save()
        QMessageBox.information(self, "", self.SUCCESS_MSG)
        self.close()

    def _save(self):
        raise NotImplementedError


class StudentRegistration(_BaseRegistration):
    TABLE = "RegistraziaYhenika"

    def _populate(self):
        for i in range(1, 34):
            row = self.db.fetchone("SELECT * FROM Klas WHERE id = ?", (i,))
            if row:
                self.comboBox.addItem(row[1])

    def _save(self):
        klass_name = self.comboBox.currentText()
        klas = self.db.fetchone(
            "SELECT id FROM Klas WHERE Klasss = ?", (klass_name,)
        )
        self.db.insert(
            """INSERT INTO RegistraziaYhenika
               (Login, Password, Famili, Neme, Otez, Klassyh, Year)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                self.lineEdit.text().strip(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                klas["id"],
                self.spinBox.text(),
            ),
        )


class TeacherRegistration(_BaseRegistration):
    TABLE = "RegTicher"

    def _populate(self):
        # у учителя нет класса
        self.comboBox.hide()
        self.label_7.hide()

    def _save(self):
        self.db.insert(
            """INSERT INTO RegTicher
               (Login, Password, Famili, Name, Otez, Year)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.lineEdit.text().strip(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.spinBox.text(),
            ),
        )