import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


class take_class_slct_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入要查询的任课信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('课程:', self)
        layout.addWidget(label2)
        self.seq_input = QLineEdit(self)
        layout.addWidget(self.seq_input)

        label3 = QLabel('课程名字关键字:', self)
        layout.addWidget(label3)
        self.key_input = QLineEdit(self)
        layout.addWidget(self.key_input)

        label4 = QLabel('课程年份:', self)
        layout.addWidget(label4)
        self.year_input = QLineEdit(self)
        layout.addWidget(self.year_input)

        label5 = QLabel('课程学期:', self)
        layout.addWidget(label5)
        self.term_combo = QComboBox()
        self.term_combo.addItem("0-任意")
        self.term_combo.addItem("1-春季学期")
        self.term_combo.addItem("2-夏季学期")
        self.term_combo.addItem("3-秋季学期")
        layout.addWidget(self.term_combo)

        label6 = QLabel('课程类型:', self)
        layout.addWidget(label6)
        self.type_combo = QComboBox()
        self.type_combo.addItem("0-任意")
        self.type_combo.addItem("1-本科生课程")
        self.type_combo.addItem("2-研究生课程")
        layout.addWidget(self.type_combo)

        label7 = QLabel('课程学时:', self)
        layout.addWidget(label7)
        self.hour_input = QLineEdit(self)
        layout.addWidget(self.hour_input)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        class_id = self.seq_input.text()
        year = self.year_input.text()
        term = self.term_combo.currentIndex()
        key = self.key_input.text()
        type2 = self.type_combo.currentIndex()
        hour = self.hour_input.text()
        take_class_slct(self.conn, self.cursor, teacher_id, class_id, key, year, term, type2, hour)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续查找?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def take_class_slct(conn, cursor, teacher_id, class_id, key, year, term, type2, hour):
    sql = "SELECT * FROM Class INNER JOIN TakeClass ON Class.ClassID = TakeClass.ClassID WHERE"
    if teacher_id != "":
        sql += f" TeacherID = '{teacher_id}' and"
    if class_id != "":
        sql += f" TakeClass.ClassID = '{class_id}' and"
    if year != "":
        sql += f" ClassYear = {year} and"
    if term != 0:
        sql += f" ClassTerm = {term} and"
    if hour != "":
        sql += f" ClassHour = {hour} and"
    if type2 != 0:
        sql += f" ClassType = {type2} and"
    if key != "":
        sql += f" ClassName LIKE '%{key}%' and"
    sql = sql[:-4]
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("Not Found!")
        message_box.setText("找不到对应的条目")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        return
    else:
        i = 0
        flag1 = 1
        flag2 = 0
        length = len(results)
        while 1:
            message = f"共查找到{length}条记录,正在显示第{i + 1}条\n"
            message += f"课程名称 : {results[i][1]} \n"
            message += f"课程学时 : {results[i][2]} \n"
            message += f"教师id为 : {results[i][4]} \n"
            message += f"课程id为 : {results[i][5]} \n"
            message += f"课程年份 : {results[i][6]} \n"
            message += f"课程学期 : "
            if results[i][7] == 1:
                message += "春季学期 \n"
            elif results[i][7] == 2:
                message += "夏季学期 \n"
            else:
                message += "秋季学期 \n"
            message += f"课程类型 : "
            if results[i][3] == 1:
                message += "本科生课程 \n"
            else:
                message += "研究生课程 \n"
            message += "选择'是'进入下一条，'否'返回上一条，'关闭'退出"
            if length == 1:
                reply = QMessageBox.question(None, "查找成功", message,QMessageBox.StandardButton.Close)
                return
            if flag1 == 1:
                reply = QMessageBox.question(None, "查找成功", message,
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Close)
            elif flag2 == 1:
                reply = QMessageBox.question(None, "查找成功", message,
                                             QMessageBox.StandardButton.No | QMessageBox.StandardButton.Close)
            else:
                reply = QMessageBox.question(None, "查找成功", message,
                                             QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes |
                                             QMessageBox.StandardButton.Close)

            # 检查用户点击的按钮类型
            if reply == QMessageBox.StandardButton.Yes:
                i += 1
                if i == length - 1:
                    flag2 = 1
                    flag1 = 0
                else:
                    flag2 = 0
                    flag1 = 0
            elif reply == QMessageBox.StandardButton.No:
                i -= 1
                if i == 0:
                    flag1 = 1
                    flag2 = 0
                else:
                    flag1 = 0
                    flag2 = 0
            elif reply == QMessageBox.StandardButton.Close:
                break
        return


