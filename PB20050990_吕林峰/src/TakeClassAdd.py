import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout

pro_list = []


class take_class_add_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入教师及课程信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("必填")
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

        label5 = QLabel('承担学时:', self)
        layout.addWidget(label5)
        self.hour_input = QLineEdit(self)
        self.hour_input.setPlaceholderText("必填")
        layout.addWidget(self.hour_input)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        class_id = self.class_input.text()
        year = self.year_input.text()
        hour = self.hour_input.text()
        term = int(self.term_input.currentIndex()) + 1
        term = str(term)
        succ = take_class_add(self.conn, self.cursor, teacher_id, class_id, year, hour, term)
        if succ == 1:
            reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续操作?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                self.accept()


def take_class_add(conn, cursor, teacher_id, class_id, year, hour, term):
    sql = f"SELECT * FROM Class WHERE ClassID = '{class_id}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("Not Found!")
        message_box.setText("找不到目标课程号,请检查输入")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        return 0
    sql = f"SELECT * FROM Teacher WHERE TeacherID = '{teacher_id}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("Not Found!")
        message_box.setText("找不到目标教师,请检查输入")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        return 0
    sql = f"SELECT * FROM TakeClass WHERE ClassID = '{class_id}' and TeacherID = '{teacher_id}' " \
          f"and ClassYear = {year} and ClassTerm = {term}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        message = f"已存在记录所提供的学时为{results[0][4]}, 是否替换"
        reply = QMessageBox.question(None, '检测到重复', message,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return 0
        else:
            sql = f"DELETE FROM TakeClass WHERE ClassID = '{class_id}' and TeacherID = '{teacher_id}' " \
                  f"and ClassYear = {year} and ClassTerm = {term}"
            cursor.execute(sql)

    # 插入
    sql = f"INSERT INTO TakeClass VALUE('{teacher_id}', '{class_id}', {year}, {term}, {hour})"
    cursor.execute(sql)
    sql = f"SELECT SUM(TakeHour) FROM TakeClass WHERE ClassID = '{class_id}' " \
          f"and ClassTerm = {term} and ClassYear = {year}"
    cursor.execute(sql)
    results = cursor.fetchall()
    curr_hour = results[0][0]
    sql = f"SELECT * FROM Class WHERE ClassID = '{class_id}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    dest_hour = results[0][2]
    if curr_hour != dest_hour:
        message_box = QMessageBox()
        message_box.setWindowTitle("学时不够")
        message_box.setText(f"课程{class_id} 要求的总学时为{dest_hour} 提供的学时为 {curr_hour} 请继续为该课程添加教师")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        if [class_id, year, term] not in pro_list:
            pro_list.append([class_id, year, term])
    else:
        if [class_id, year, term] in pro_list:
            pro_list.remove([class_id, year, term])
    if len(pro_list) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("提交成功")
        message_box.setText(f"课程学时满足要求，提交成功")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        conn.commit()
        return 1
    else:
        return 0
