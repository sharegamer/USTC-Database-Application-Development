import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


class take_class_rmv_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入要删除的课程相关信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，填之前确保其承担学时为0")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('课程号:', self)
        layout.addWidget(label2)
        self.class_input = QLineEdit(self)
        self.class_input.setPlaceholderText("必填")
        layout.addWidget(self.class_input)

        label3 = QLabel('任课年份:', self)
        layout.addWidget(label3)
        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText("必填")
        layout.addWidget(self.year_input)

        label4 = QLabel('任课学期:', self)
        layout.addWidget(label4)
        self.term_input = QComboBox()
        self.term_input.addItem("1-春季学期")
        self.term_input.addItem("2-夏季学期")
        self.term_input.addItem("3-秋季学期")
        layout.addWidget(self.term_input)

        help_btn = QPushButton('帮助', self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("删除课程信息会删除该学期课程的相关记录\n要删除某个老师在某门课的任课记录，请提前将其承担学时设为0")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        class_id = self.class_input.text()
        year = self.year_input.text()
        term = int(self.term_input.currentIndex()) + 1
        term = str(term)
        take_class_rmv(self.conn, self.cursor, teacher_id, class_id, year, term)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续删除?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def take_class_rmv(conn, cursor, teacher_id, class_id, year, term):
    if teacher_id != "":
        sql = f"SELECT * FROM TakeClass WHERE ClassID = '{class_id}' and TeacherID = '{teacher_id}' " \
              f"and ClassYear = {year} and ClassTerm = {term}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的教师和课程记录")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        if results[0][4] != 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("教师承担学时不为0")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            sql = f"DELETE FROM TakeClass WHERE ClassID = '{class_id}' and TeacherID = '{teacher_id}' " \
                  f"and ClassYear = {year} and ClassTerm = {term}"
            cursor.execute(sql)
            conn.commit()
    else:
        sql = f"SELECT * FROM TakeClass WHERE ClassID = '{class_id}'" \
              f"and ClassYear = {year} and ClassTerm = {term}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的课程记录")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        sql = f"DELETE FROM TakeClass WHERE ClassID = '{class_id}'" \
              f"and ClassYear = {year} and ClassTerm = {term}"
        cursor.execute(sql)
        conn.commit()

