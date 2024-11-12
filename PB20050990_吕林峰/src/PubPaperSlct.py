import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


def to_int(string):
    if string == "":
        return None
    else:
        return int(string)


class pub_paper_slct_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle("请输入要查询的作者或论文信息")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel("教师工号:", self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel("论文序号:", self)
        layout.addWidget(label2)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.seq_input)

        label3 = QLabel("关键字查找:", self)
        layout.addWidget(label3)
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("只填一个即可")
        layout.addWidget(self.key_input)

        help_btn = QPushButton("帮助", self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton("确定", self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("输入要查找的作者id或论文序号即可\n也可根据论文或发表源的名字进行关键字查找")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        seq = self.seq_input.text()
        if not seq.isdigit() and seq != "":
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("论文序号必须为数字")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        seq = to_int(seq)
        key = self.key_input.text()
        pub_paper_slct(self.conn, self.cursor, teacher_id, seq, key)
        reply = QMessageBox.question(
            self,
            "操作完成！",
            "操作完成，是否继续查找?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def pub_paper_slct(conn, cursor, teacher_id, sequence, key):
    if teacher_id != "":
        sql = f"SELECT * FROM PubPaper WHERE TeacherID = '{teacher_id}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到该教师发表的论文")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            i = 0
            flag1 = 1
            flag2 = 0
            length = len(results)
            while 1:
                sql = f"SELECT * FROM Paper WHERE sequence = {results[i][1]}"
                cursor.execute(sql)
                result2 = cursor.fetchall()
                message = f"共查找到{length}条记录,正在显示第{i + 1}条\n"
                message += f"发表论文序号 : {results[i][1]} \n"
                message += f"该教师论文排名为 : {results[i][2]} \n"
                message += f"是否为第一作者 : {results[i][3]} \n"
                message += f"论文标题为 : {result2[0][1]} \n"
                message += f"论文发表源为 : {result2[0][2]} \n"
                message += f"论文发表年份为 : {result2[0][3]} \n"
                message += f"论文类型为 : {result2[0][4]} \n"
                message += f"论文类别为 : {result2[0][5]} \n"
                message += "选择'是'进入下一条，'否'返回上一条，'关闭'退出"
                if flag1 == 1:
                    reply = QMessageBox.question(
                        None,
                        "查找成功",
                        message,
                        QMessageBox.StandardButton.Yes
                        | QMessageBox.StandardButton.Close,
                    )
                elif flag2 == 1:
                    reply = QMessageBox.question(
                        None,
                        "查找成功",
                        message,
                        QMessageBox.StandardButton.No
                        | QMessageBox.StandardButton.Close,
                    )
                else:
                    reply = QMessageBox.question(
                        None,
                        "查找成功",
                        message,
                        QMessageBox.StandardButton.No
                        | QMessageBox.StandardButton.Yes
                        | QMessageBox.StandardButton.Close,
                    )
                # 当用户点击"是"按钮时，表示要查看下一条记录。如果当前正在显示的是倒数第二条记录，则将flag2设置为1，flag1设置为0。否则，将flag1和flag2都设置为0。
                # 当用户点击"否"按钮时，表示要查看上一条记录。如果当前正在显示第一条记录，则将flag1设置为1，flag2设置为0。否则，将flag1和flag2都设置为0。
                # 检查用户点击的按钮类型
                if reply == QMessageBox.StandardButton.Yes:
                    if length == 1:
                        break
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
    if sequence is not None:
        sql = f"SELECT * FROM Paper WHERE sequence = {sequence}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的论文")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            message = "查找成功\n"
            message += "论文相关信息为:\n"
            message += f"论文标题为 : {results[0][1]} \n"
            message += f"论文发表源为 : {results[0][2]} \n"
            message += f"论文发表年份为 : {results[0][3]} \n"
            message += f"论文类型为 : {results[0][4]} \n"
            message += f"论文类别为 : {results[0][5]} \n"
            message += "是否查询其相关作者"
            reply = QMessageBox.question(
                None,
                "查找成功",
                message,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Close,
            )
            if reply == QMessageBox.StandardButton.Yes:
                sql = f"SELECT * FROM PubPaper WHERE sequence = {sequence}"
                cursor.execute(sql)
                results = cursor.fetchall()
                message = "相关作者为"
                for row in results:
                    message += "\n"
                    message += f"教师id为:{row[0]}"
                    message += f" 其贡献排名为{row[2]}"
                    if row[3] == 1:
                        message += f" 是通讯作者"
                message_box = QMessageBox()
                message_box.setWindowTitle("查询结果")
                message_box.setText(message)
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.exec()
        return
    else:
        sql = f"SELECT * FROM Paper"
        cursor.execute(sql)
        results = cursor.fetchall()
        flag = 0
        for row in results:
            if key in row[1] or key in row[2]:
                flag = 1
                message = ""
                message += f"论文标题为 : {row[1]} \n"
                message += f"论文发表源为 : {row[2]} \n"
                message += f"论文发表年份为 : {row[3]} \n"
                message += f"论文类型为 : {row[4]} \n"
                message += f"论文类别为 : {row[5]} \n"
                message_box = QMessageBox()
                message_box.setWindowTitle("查询结果")
                message_box.setText(message)
                custom_button = message_box.addButton(
                    "下一条", QMessageBox.ButtonRole.ActionRole
                )
                message_box.exec()
        if flag == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
