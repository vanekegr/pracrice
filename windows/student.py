from PyQt5.QtWidgets import QMainWindow, QMessageBox
from database import DB
from paths import load_ui


class StudentWindow(QMainWindow):
    def __init__(self, user: dict):
        super().__init__()
        load_ui(self, "yhenik.ui")
        self.db = DB()
        self.user = user
        self.pushButton.clicked.connect(self._send_work)
        self._load_works()

    def _load_works(self):
        rows = self.db.fetchall(
            """SELECT * FROM Rabota
               WHERE Status = 1 AND Klass = ?""",
            (self.user["Klassyh"],),
        )
        for row in rows:
            subj = self.db.fetchone(
                "SELECT * FROM XZ WHERE id = ?", (row["Predmet"],)
            )
            if subj:
                self.comboBox.addItem(f"{row['Names']}, {subj[1]}, {row['Data']}")

    def _send_work(self):
        answer = QMessageBox.question(
            self, "",
            "Вы действительно хотите отправить работу?\n"
            "После отправки работу нельзя будет редактировать",
            QMessageBox.Yes, QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        text = self.textEdit.toPlainText()
        combo = self.comboBox.currentText().split(", ")
        if not text or combo == [""]:
            QMessageBox.critical(self, "", "Работа отсутствует")
            return

        name, predmet, data = combo[0], combo[1], combo[2]
        subj = self.db.fetchone("SELECT id FROM XZ WHERE Predm = ?", (predmet,))
        existing = self.db.fetchone(
            """SELECT 1 FROM Rabota
               WHERE Names = ? AND Data = ? AND Predmet = ?
                 AND Klass = ? AND Yhenik = ?""",
            (name, data, subj["id"], self.user["Klassyh"], self.user["id"]),
        )
        if existing:
            QMessageBox.warning(self, "", "Работа уже отправлена")
            return
        self.db.insert(
            """INSERT INTO Rabota
               (Names, Data, Predmet, Klass, Yhenik, Status, Samarab)
               VALUES (?, ?, ?, ?, ?, 2, ?)""",
            (name, data, subj["id"], self.user["Klassyh"], self.user["id"], text),
        )
        self.textEdit.setText("")
        QMessageBox.information(self, "", "Работа успешно отправлена")