from PyQt5.QtWidgets import QMainWindow, QMessageBox
from database import DB
from paths import load_ui


class TeacherHomeWindow(QMainWindow):
    """Главное окно учителя («Добавить работу» / «Открыть сохранённую»)."""

    def __init__(self, user: dict):
        super().__init__()
        load_ui(self, "dobavit.ui")
        self.db = DB()
        self.user = user
        self.pushButton.clicked.connect(self._create_work)
        self.pushButton_22.clicked.connect(self._open_existing)
        self._load_subjects()
        self._load_classes()

    def _load_subjects(self):
        for i in range(1, 14):
            row = self.db.fetchone("SELECT * FROM XZ WHERE id = ?", (i,))
            if row:
                self.comboBox.addItem(row[1])

    def _load_classes(self):
        for i in range(1, 34):
            row = self.db.fetchone("SELECT * FROM Klas WHERE id = ?", (i,))
            if row:
                self.comboBox_2.addItem(row[1])

    def _get_selection(self):
        name = self.lineEdit_2.text().strip()
        predmet = self.comboBox.currentText()
        klass_name = self.comboBox_2.currentText()
        data = self.dateEdit.text()
        klass = self.db.fetchone(
            "SELECT id FROM Klas WHERE Klasss = ?", (klass_name,)
        )
        subj = self.db.fetchone(
            "SELECT id FROM XZ WHERE Predm = ?", (predmet,)
        )
        return name, data, subj["id"] if subj else None, klass["id"] if klass else None

    def _create_work(self):
        name, data, predmet_id, klass_id = self._get_selection()
        if not name:
            QMessageBox.warning(self, "", "Введите название работы")
            return
        self.db.insert(
            """INSERT INTO Rabota (Names, Data, Predmet, Klass, Status)
               VALUES (?, ?, ?, ?, 1)""",
            (name, data, predmet_id, klass_id),
        )
        rows = self.db.fetchall(
            """SELECT * FROM Rabota
               WHERE Names = ? AND Data = ? AND Predmet = ? AND Klass = ?""",
            (name, data, predmet_id, klass_id),
        )
        self._open_check_window(rows)

    def _open_existing(self):
        name, data, predmet_id, klass_id = self._get_selection()
        rows = self.db.fetchall(
            """SELECT * FROM Rabota
               WHERE Names = ? AND Predmet = ? AND Klass = ? AND Data = ?""",
            (name, predmet_id, klass_id, data),
        )
        if not rows:
            QMessageBox.warning(self, "", "Работа не найдена")
            return
        self._open_check_window(rows)

    def _open_check_window(self, rows):
        from windows.work_check import WorkCheckWindow
        self.check_window = WorkCheckWindow(rows)
        self.check_window.show()
        self.hide()