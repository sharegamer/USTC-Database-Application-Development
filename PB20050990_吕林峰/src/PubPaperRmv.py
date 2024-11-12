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


class pub_paper_rmv_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle("请输入要删除论文或者发表记录")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel("教师工号:", self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只删除论文时可以不输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel("论文序号:", self)
        layout.addWidget(label2)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("必填")
        layout.addWidget(self.seq_input)

        help_btn = QPushButton("帮助", self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton("确定", self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("输入要删除条目的作者id和论文序号即可\n如果删除论文，会删除所有的相关发表条目，请谨慎操作")
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
        if seq is None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("论文序号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        pub_paper_rmv(self.conn, self.cursor, teacher_id, seq)
        reply = QMessageBox.question(
            self,
            "操作完成！",
            "操作完成，是否继续删除?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def pub_paper_rmv(conn, cursor, teacher_id, sequence):
    if teacher_id == "":
        # 仅删除论文
        # 查询是否有发表记录关联改论文
        sql = f"SELECT * FROM  PubPaper WHERE sequence = {sequence}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            reply = QMessageBox.question(
                None,
                "有其他教师关联",
                "将删除所有与该论文的发表记录，是否继续?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            else:
                # 删除论文和相关的发表条目
                sql = f"DELETE FROM PubPaper WHERE sequence = {sequence}"
                cursor.execute(sql)
                sql = f"DELETE FROM Paper WHERE sequence = {sequence}"
                cursor.execute(sql)
                conn.commit()
                return

        # 仅删除论文
        sql = f"DELETE FROM Paper WHERE sequence = {sequence}"
        cursor.execute(sql)
        conn.commit()
        return

    # 教师id不为空 删除的是发表条目
    sql = f"SELECT * FROM PubPaper WHERE TeacherID = '{teacher_id}' AND sequence = {sequence}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("Not Found!")
        message_box.setText("找不到与目标一致的条录,请检查输入")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        return
    sql = f"DELETE FROM PubPaper WHERE TeacherID = '{teacher_id}' AND sequence = {sequence}"
    cursor.execute(sql)

    conn.commit()
