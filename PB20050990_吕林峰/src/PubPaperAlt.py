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


class pub_paper_alt_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle("请输入作者及论文信息")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel("教师工号:", self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只更改论文时可以不输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel("教师发表论文的排名(新值):", self)
        layout.addWidget(label2)
        self.rank_input = QLineEdit(self)
        self.rank_input.setPlaceholderText("只更改论文时可以不输入")
        layout.addWidget(self.rank_input)

        label3 = QLabel("是否通讯作者(新值):", self)
        layout.addWidget(label3)
        self.con_combo = QComboBox()
        self.con_combo.addItem("0-否")
        self.con_combo.addItem("1-是")
        layout.addWidget(self.con_combo)

        label4 = QLabel("论文序号:", self)
        layout.addWidget(label4)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("必填")
        layout.addWidget(self.seq_input)

        label9 = QLabel("论文名称(新值):", self)
        layout.addWidget(label9)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("可选，不更改论文信息时可以不输入")
        layout.addWidget(self.name_input)

        label5 = QLabel("论文发表源(新值):", self)
        layout.addWidget(label5)
        self.src_input = QLineEdit(self)
        self.src_input.setPlaceholderText("可选，不更改论文信息时可以不输入")
        layout.addWidget(self.src_input)

        label6 = QLabel("论文发表年份(新值):", self)
        layout.addWidget(label6)
        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText("可选，不更改论文信息时可以不输入")
        layout.addWidget(self.year_input)

        label7 = QLabel("论文类型(新值):", self)
        layout.addWidget(label7)
        self.type_combo = QComboBox()
        self.type_combo.addItem("0-不更改论文信息时可以不输入")
        self.type_combo.addItem("1-full paper")
        self.type_combo.addItem("2-short paper")
        self.type_combo.addItem("3-poster paper")
        self.type_combo.addItem("4-demo paper")
        layout.addWidget(self.type_combo)

        label8 = QLabel("论文级别(新值):", self)
        layout.addWidget(label8)
        self.grade_combo = QComboBox()
        self.grade_combo.addItem("0-不更改论文信息时可以不输入")
        self.grade_combo.addItem("1-CCF-A")
        self.grade_combo.addItem("2-CCF-B")
        self.grade_combo.addItem("3-CCF-C")
        self.grade_combo.addItem("4-中文 CCF-A")
        self.grade_combo.addItem("5-中文 CCFB")
        self.grade_combo.addItem("6-无级别")
        layout.addWidget(self.grade_combo)

        help_btn = QPushButton("帮助", self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton("确定", self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("需要改什么就填什么\n可以只更改论文信息\n注意通讯作者栏默认值为否")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        rank = self.rank_input.text()
        rank = to_int(rank)
        con = self.con_combo.currentIndex()
        seq = self.seq_input.text()
        if not seq.isdigit() and seq != "":
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("论文序号必须为数字")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        seq = to_int(seq)
        name = self.name_input.text()
        src = self.src_input.text()
        year = self.year_input.text()
        year = to_int(year)
        type2 = self.type_combo.currentIndex()
        grade = self.grade_combo.currentIndex()
        pub_paper = [teacher_id, seq, rank, con]
        paper = [seq, name, src, year, type2, grade]
        if seq is None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("论文序号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        pub_paper_alt(self.conn, self.cursor, teacher_id, seq, pub_paper, paper)
        reply = QMessageBox.question(
            self,
            "操作完成！",
            "操作完成，是否继续更改?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def pub_paper_alt(conn, cursor, teacher_id, sequence, pub_paper, paper):
    # 根据teaherID改关系
    # teacherID留空视为只改论文
    if teacher_id != "":
        sql = f"SELECT * FROM PubPaper WHERE TeacherID = '{teacher_id}' AND sequence = {sequence}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的教师和论文发表记录")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            sql = "UPDATE PubPaper SET "
            if pub_paper[2] is not None:
                # 检测rank是否重复
                sql2 = f"SELECT * FROM PubPaper WHERE sequence = {sequence} and Pubrank = {pub_paper[2]}"
                cursor.execute(sql2)
                results = cursor.fetchall()
                if len(results) != 0 and results[0][0] != teacher_id:
                    message_box = QMessageBox()
                    message_box.setWindowTitle("排名重复！")
                    message_box.setText(
                        f"存在另一个排名为{pub_paper[2]}的作者,其教师id为{results[0][0]}"
                    )
                    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    message_box.exec()
                    return
                sql += f"Pubrank = {pub_paper[2]},"
            # 检测是否有多个通讯作者
            if pub_paper[3] == 1:
                sql2 = f"SELECT * FROM PubPaper WHERE sequence = {sequence} and IsConAuthor = 1"
                cursor.execute(sql2)
                results = cursor.fetchall()
                if len(results) != 0 and results[0][0] != teacher_id:
                    message_box = QMessageBox()
                    message_box.setWindowTitle("多个通讯作者")
                    message_box.setText(f"存在另一个通讯作者，其id为{results[0][0]}")
                    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    message_box.exec()
                    return
            sql += f"IsConAuthor = {pub_paper[3]}"
            sql += f" WHERE sequence = {sequence} AND TeacherID = '{teacher_id}'"
            cursor.execute(sql)

    else:
        sql = f"SELECT * FROM Paper WHERE sequence = {sequence}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有对应的论文")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        sql = "UPDATE Paper SET "
        if paper[1] != "":
            sql += f"PaperName = '{paper[1]}',"
        if paper[2] != "":
            sql += f"PaperSource = '{paper[2]}',"
        if paper[3] is not None:
            sql += f"PaperYear = {paper[3]},"
        if paper[4] != 0:
            sql += f"PaperType = {paper[4]},"
        if paper[5] != 0:
            sql += f"PaperGrade = {paper[5]},"
        sql = sql[:-1]
        sql += f" WHERE sequence = {sequence}"
        cursor.execute(sql)
    conn.commit()
