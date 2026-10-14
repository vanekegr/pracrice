from PyQt5.QtWidgets import QMainWindow
from database import DB
from paths import load_ui


class ProfileWindow(QMainWindow):
    def __init__(self, work_row):
        super().__init__()
        load_ui(self, "profile.ui")
        self.db = DB()
        student = self.db.fetchone(
            "SELECT * FROM RegistraziaYhenika WHERE id = ?",
            (work_row["Yhenik"],),
        )
        if not student:
            return
        self.lineEdit.setText(student["Neme"])
        self.lineEdit_2.setText(student["Famili"])
        self.lineEdit_3.setText(student["Otez"])
        for w in (self.lineEdit, self.lineEdit_2, self.lineEdit_3):
            w.setEnabled(False)

        klass = self.db.fetchone(
            "SELECT Klasss FROM Klas WHERE id = ?", (student["Klassyh"],)
        )
        if klass:
            self.lineEdit_4.setText(klass["Klasss"])
        self.lineEdit_4.setEnabled(False)

        self.spinBox.setMinimum(student["Year"])
        self.spinBox.setMaximum(student["Year"])