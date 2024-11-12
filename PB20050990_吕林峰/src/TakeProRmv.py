import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


class take_project_rmv_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle("请输入要删除项目或者教师承担项目记录")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel("教师工号:", self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只删除项目时可以不输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel("项目号:", self)
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
        message_box.setText("输入要删除条目的教师id和项目号即可\n如果删除项目，会删除所有的相关条目，请谨慎操作")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        seq = self.seq_input.text()
        if seq is None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("项目号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        take_project_rmv(self.conn, self.cursor, teacher_id, seq)
        reply = QMessageBox.question(
            self,
            "操作完成！",
            "操作完成，是否继续删除?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def take_project_rmv(conn, cursor, teacher_id, sequence):
    if teacher_id == "":
        # 仅删除论文
        # 查询是否有发表记录关联改论文
        sql = f"SELECT * FROM  TakeProject WHERE sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            reply = QMessageBox.question(
                None,
                "有其他教师关联",
                "将删除所有与该项目关联的记录，是否继续?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            else:
                # 删除论文和相关的发表条目
                sql = f"DELETE FROM TakeProject WHERE sequence = {sequence}"
                cursor.execute(sql)
                sql = f"DELETE FROM Project WHERE sequence = {sequence}"
                cursor.execute(sql)
                conn.commit()
                return

        # 仅删除论文
        sql = f"DELETE FROM Project WHERE sequence = {sequence}"
        cursor.execute(sql)
        conn.commit()
        return

    # 教师id不为空 删除的是发表条目
    sql = f"SELECT * FROM TakeProject WHERE TeacherID = '{teacher_id}' AND sequence = '{sequence}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        message_box = QMessageBox()
        message_box.setWindowTitle("Not Found!")
        message_box.setText("找不到与目标一致的条录,请检查输入")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
        return

    # 改一下资金
    sql = f"SELECT * FROM TakeProject WHERE TeacherID = '{teacher_id}' AND sequence = '{sequence}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    fund = results[0][3]
    sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    fund = results[0][4] - fund
    sql = f"UPDATE Project SET ProjectFund = {fund} WHERE sequence = '{sequence}'"
    cursor.execute(sql)
    sql = f"DELETE FROM TakeProject WHERE TeacherID = '{teacher_id}' AND sequence = '{sequence}'"
    cursor.execute(sql)

    conn.commit()
