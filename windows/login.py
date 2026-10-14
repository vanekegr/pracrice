from PyQt5.QtWidgets import QMainWindow, QMessageBox
from database import DB
from paths import load_ui


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_ui(self, "vhod.ui")
        self.db = DB()
        self.pushButton.clicked.connect(self._login_teacher)
        self.pushButton_3.clicked.connect(self._login_student)
        self.pushButton_2.clicked.connect(self._open_teacher_registration)
        self.pushButton_4.clicked.connect(self._open_student_registration)
        self._student_window = None
        self._teacher_window = None
        self._reg_windows = []

    def _open_teacher_registration(self):
        from windows.registration import TeacherRegistration
        w = TeacherRegistration()
        w.show()
        self._reg_windows.append(w)

    def _open_student_registration(self):
        from windows.registration import StudentRegistration
        w = StudentRegistration()
        w.show()
        self._reg_windows.append(w)

    def _login_student(self):
        login = self.lineEdit_3.text().strip()
        password = self.lineEdit_4.text()
        row = self.db.fetchone(
            "SELECT * FROM RegistraziaYhenika WHERE Login = ? AND Password = ?",
            (login, password),
        )
        if not row:
            QMessageBox.warning(self, "", "Аккаунт не найден")
            return
        from windows.student import StudentWindow
        self._student_window = StudentWindow(dict(row))
        self._student_window.show()
        self.hide()

    def _login_teacher(self):
        login = self.lineEdit.text().strip()
        password = self.lineEdit_2.text()
        row = self.db.fetchone(
            "SELECT * FROM RegTicher WHERE Login = ? AND Password = ?",
            (login, password),
        )
        if not row:
            QMessageBox.warning(self, "", "Аккаунт не найден")
            return
        from windows.teacher_home import TeacherHomeWindow
        self._teacher_window = TeacherHomeWindow(dict(row))
        self._teacher_window.show()
        self.hide()