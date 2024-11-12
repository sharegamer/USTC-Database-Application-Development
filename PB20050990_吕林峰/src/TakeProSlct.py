import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout

class take_project_slct_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入要查询的项目承担人或项目信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('项目号:', self)
        layout.addWidget(label2)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.seq_input)

        label3 = QLabel('关键字查找:', self)
        layout.addWidget(label3)
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.key_input)

        help_btn = QPushButton('帮助', self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("输入要查找的教师id或项目号即可\n也可根据项目或来源的名字进行关键字查找")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        seq = self.seq_input.text()
        key = self.key_input.text()
        take_pro_slct(self.conn, self.cursor, teacher_id, seq, key)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续查找?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()

def take_pro_slct(conn, cursor, teacher_id, sequence, key):
    if teacher_id != '':
        sql = f"SELECT * FROM TakeProject WHERE TeacherID = '{teacher_id}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到该教师承担的项目")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            i = 0
            flag1 = 1
            flag2 = 0
            length = len(results)
            while 1:
                sql = f"SELECT * FROM Project WHERE sequence = '{results[i][1]}'"
                cursor.execute(sql)
                result2 = cursor.fetchall()
                message = f"共查找到{length}条记录,正在显示第{i + 1}条\n"
                message += f"项目号 : {results[i][1]} \n"
                message += f"该教师在项目中的排名 : {results[i][2]} \n"
                message += f"该教师承担经费 : {results[i][3]} \n"
                message += f"项目名称 : {result2[0][1]} \n"
                message += f"项目来源 : {result2[0][2]} \n"
                message += f"项目类型 : {result2[0][3]} \n"
                message += f"总经费 : {result2[0][4]} \n"
                message += f"开始年份 : {result2[0][5]} \n"
                message += f"结束年份 : {result2[0][6]} \n"
                message += "选择'是'进入下一条，'否'返回上一条，'关闭'退出"
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
                    else:
                        flag2 = 0
                        flag1 = 0
                elif reply == QMessageBox.StandardButton.No:
                    i -= 1
                    if i == 0:
                        flag1 = 1
                    else:
                        flag1 = 0
                        flag2 = 0
                elif reply == QMessageBox.StandardButton.Close:
                    break
            return

    if sequence != '':
        sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的项目")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            message = "查找成功\n"
            message += "项目相关信息为:\n"
            message += f"项目名称 : {results[0][1]} \n"
            message += f"项目来源为 : {results[0][2]} \n"
            message += f"项目类型 : {results[0][3]} \n"
            message += f"总经费 : {results[0][4]} \n"
            message += f"开始年份 : {results[0][5]} \n"
            message += f"结束年份 : {results[0][6]} \n"
            message += "是否查询其相关教师"
            reply = QMessageBox.question(None, "查找成功", message,
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Close)
            if reply == QMessageBox.StandardButton.Yes:
                sql = f"SELECT * FROM TakeProject WHERE sequence = '{sequence}'"
                cursor.execute(sql)
                results = cursor.fetchall()
                message = "相关教师为"
                for row in results:
                    message += "\n"
                    message += f"教师id为:{row[0]} "
                    message += f" 其贡献排名为{row[2]} "
                    message += f" 其承担经费为{row[3]}"
                message_box = QMessageBox()
                message_box.setWindowTitle("查询结果")
                message_box.setText(message)
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.exec()
        return
    else:
        sql = f"SELECT * FROM Project"
        cursor.execute(sql)
        results = cursor.fetchall()
        flag = 0
        for row in results:
            if key in row[1] or key in row[2]:
                flag = 1
                message = ""
                message += f"项目名称 : {row[1]} \n"
                message += f"项目来源为 : {row[2]} \n"
                message += f"项目类型 : {row[3]} \n"
                message += f"总经费 : {row[4]} \n"
                message += f"开始年份 : {row[5]} \n"
                message += f"结束年份 : {row[6]} \n"
                message_box = QMessageBox()
                message_box.setWindowTitle("查询结果")
                message_box.setText(message)
                custom_button = message_box.addButton("下一条", QMessageBox.ButtonRole.ActionRole)
                message_box.exec()
        if flag == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
