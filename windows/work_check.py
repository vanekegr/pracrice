import difflib
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from database import DB
from paths import load_ui


PLAGIARISM_THRESHOLD = 80  # %


class WorkCheckWindow(QMainWindow):
    """Окно проверки работ учеников."""

    def __init__(self, rows):
        super().__init__()
        load_ui(self, "projectOSn.ui")
        self.db = DB()
        self.rows = rows  # список работ
        self.current = rows[0]
        self._setup_ui()
        self._setup_student_buttons()
        self._load_current()

    # ---------- инициализация ----------
    def _setup_ui(self):
        self.pushButton.clicked.connect(self._back_to_home)
        self.pushButton_2.clicked.connect(self._save_work)
        self.pushButton_4.clicked.connect(self._check_plagiarism)
        self.pushButton_25.clicked.connect(self._show_profile)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(0)

        # класс и предмет — те, что у текущей работы
        klass = self.db.fetchone(
            "SELECT Klasss FROM Klas WHERE id = ?", (self.current["Klass"],)
        )
        if klass:
            self.comboBox_2.addItem(klass["Klasss"])
        predmet = self.db.fetchone(
            "SELECT Predm FROM XZ WHERE id = ?", (self.current["Predmet"],)
        )
        if predmet:
            self.comboBox.addItem(predmet["Predm"])
        for i in (1, 2):
            stat = self.db.fetchone("SELECT * FROM Stat WHERE id = ?", (i,))
            if stat:
                self.comboBox_3.addItem(stat[1])

    def _setup_student_buttons(self):
        # pushButton_5 … pushButton_24 — 20 кнопок с индексами 1..20 в self.rows
        for idx in range(1, 21):
            btn = getattr(self, f"pushButton_{idx + 4}")
            if len(self.rows) <= idx:
                btn.hide()
                continue
            btn.setText(self._student_label(self.rows[idx]))
            btn.clicked.connect(lambda _checked, i=idx: self._show_work(i))

    def _student_label(self, row):
        stu = self.db.fetchone(
            "SELECT Famili, Neme, Otez FROM RegistraziaYhenika WHERE id = ?",
            (row["Yhenik"],),
        )
        if not stu:
            return "—"
        return f"{stu['Famili']} {stu['Neme'][0]}. {stu['Otez'][0]}."

    def _load_current(self):
        row = self.current
        # заголовок
        self.label_31.setText(row["Names"])
        self.lineEdit_2.setText(row["Data"])
        # данные выбранного ученика
        self._render_work(row)

    def _render_work(self, row):
        if row["Yhenik"]:
            self.lineEdity.setText(self._student_label(row))
        self.textEdit_2.setText(row["Samarab"] or "")
        self.textEdit_3.setText(row["Komment"] or "")
        self.textEdit_4.setText(row["Feile"] or "")
        if row["Ozenka"]:
            self.spinBox.setMinimum(2)
            self.spinBox.setMaximum(5)
            self.spinBox.setValue(int(row["Ozenka"]))

    # ---------- действия ----------
    def _show_work(self, idx):
        self.current = self.rows[idx]
        self._render_work(self.current)

    def _back_to_home(self):
        from windows.teacher_home import TeacherHomeWindow
        self.home = TeacherHomeWindow(self.db.fetchone(
            "SELECT * FROM RegTicher LIMIT 1"
        ))
        self.home.show()
        self.hide()

    def _show_profile(self):
        from windows.profile import ProfileWindow
        self.profile = ProfileWindow(self.current)
        self.profile.show()

    def _save_work(self):
        if QMessageBox.question(
            self, "", "Вы действительно хотите сохранить работу?",
            QMessageBox.Yes, QMessageBox.No,
        ) != QMessageBox.Yes:
            return
        status = self.db.fetchone(
            "SELECT id FROM Stat WHERE Stata = ?",
            (self.comboBox_3.currentText(),),
        )
        self.db.execute(
            """UPDATE Rabota
               SET Ozenka = ?, Feile = ?, Komment = ?, Status = ?
               WHERE id = ?""",
            (
                self.spinBox.text(),
                self.textEdit_4.toPlainText(),
                self.textEdit_3.toPlainText(),
                status["id"] if status else None,
                self.current["id"],
            ),
        )
        self.db.commit()
        QMessageBox.information(self, "", "Работа успешно сохранена")

    def _check_plagiarism(self):
        suspects = []
        for i in range(1, len(self.rows)):
            for j in range(i + 1, len(self.rows)):
                t1 = (self.rows[i]["Samarab"] or "").lower()
                t2 = (self.rows[j]["Samarab"] or "").lower()
                if not t1 or not t2:
                    continue
                ratio = int(difflib.SequenceMatcher(None, t1, t2).ratio() * 100)
                if ratio >= PLAGIARISM_THRESHOLD:
                    suspects.append(
                        (self._student_label(self.rows[i]),
                         self._student_label(self.rows[j]),
                         ratio)
                    )
        if not suspects:
            QMessageBox.information(self, "", "Схожих работ нет")
            return
        text = "\n".join(
            f"Работы {a} и {b} схожи на {p}%" for a, b, p in suspects
        )
        QMessageBox.warning(self, "", text)