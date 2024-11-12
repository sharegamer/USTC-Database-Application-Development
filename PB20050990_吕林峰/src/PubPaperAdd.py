import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


def to_int(string):
    if string == '':
        return None
    else:
        return int(string)


class pub_paper_add_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入作者及论文信息')
        # 创建一个垂直布局QVBoxLayout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # 创建了多个标签(QLabel)、输入框(QLineEdit); 和下拉框(QComboBox)，并将它们添加到布局中。
        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只增加论文时可以不输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('教师发表论文的排名:', self)
        layout.addWidget(label2)
        self.rank_input = QLineEdit(self)
        self.rank_input.setPlaceholderText("只增加论文时可以不输入")
        layout.addWidget(self.rank_input)

        label3 = QLabel('是否通讯作者:', self)
        layout.addWidget(label3)
        self.con_combo = QComboBox()
        self.con_combo.addItem("0-否")
        self.con_combo.addItem("1-是")
        layout.addWidget(self.con_combo)

        label4 = QLabel('论文序号:', self)
        layout.addWidget(label4)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("必填")
        layout.addWidget(self.seq_input)

        label9 = QLabel('论文名称:', self)
        layout.addWidget(label9)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("可选，已有该论文时可以不输入")
        layout.addWidget(self.name_input)

        label5 = QLabel('论文发表源:', self)
        layout.addWidget(label5)
        self.src_input = QLineEdit(self)
        self.src_input.setPlaceholderText("可选，已有该论文时可以不输入")
        layout.addWidget(self.src_input)

        label6 = QLabel('论文发表年份:', self)
        layout.addWidget(label6)
        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText("可选，已有该论文时可以不输入")
        layout.addWidget(self.year_input)

        label7 = QLabel('论文类型:', self)
        layout.addWidget(label7)
        self.type_combo = QComboBox()
        self.type_combo.addItem("0-已有该论文时可以不输入")
        self.type_combo.addItem("1-full paper")
        self.type_combo.addItem("2-short paper")
        self.type_combo.addItem("3-poster paper")
        self.type_combo.addItem("4-demo paper")
        layout.addWidget(self.type_combo)

        label8 = QLabel('论文级别:', self)
        layout.addWidget(label8)
        self.grade_combo = QComboBox()
        self.grade_combo.addItem("0-已有该论文时可以不输入")
        self.grade_combo.addItem("1-CCF-A")
        self.grade_combo.addItem("2-CCF-B")
        self.grade_combo.addItem("3-CCF-C")
        self.grade_combo.addItem("4-中文 CCF-A")
        self.grade_combo.addItem("5-中文 CCFB")
        self.grade_combo.addItem("6-无级别")
        layout.addWidget(self.grade_combo)

        help_btn = QPushButton('帮助', self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("可以实现仅插入论文信息和插入教师发表论文信息\n前者可以不输入教师相关信息\n后者也可插入论文信息"
                            "\n如果论文是现有论文只需输入序号即可")
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
        if teacher_id == '':
            pub_paper = None
        else:
            pub_paper = [teacher_id, seq, rank, con]
        if name == '':
            paper = None
        else:
            paper = [seq, name, src, year, type2, grade]
        if seq is None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("论文序号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        pub_paper_add(self.conn, self.cursor, teacher_id, seq, pub_paper, paper)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续插入?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def pub_paper_add(conn, cursor, teacher_id, sequence, pub_paper=None, paper=None):
    # 先检查是否有对应的论文，没有的话会直接替换
    sql = f"SELECT * FROM Paper WHERE sequence = {sequence}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if paper is not None:
        if len(results) == 0:
            sql = f"INSERT INTO Paper VALUE({paper[0]}, '{paper[1]}', '{paper[2]}', {paper[3]}, {paper[4]}, {paper[5]})"
            cursor.execute(sql)
        else:
            if paper is not None and results[0] != tuple(paper):
                reply = QMessageBox.question(None, 'Error！', '存在论文与目标论文信息不一致，是否替换?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    sql = f"UPDATE Paper SET PaperName = '{paper[1]}', PaperSource = '{paper[2]}', PaperYear = {paper[3]}, " \
                          f" PaperType =  {paper[4]}, PaperGrade = {paper[5]} WHERE sequence = {sequence}"
                    cursor.execute(sql)

    # 先查重，再插入
    if pub_paper is not None:
        sql = f"SELECT * FROM PubPaper WHERE TeacherID = '{teacher_id}' AND sequence = {sequence}"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0 and results[0] != tuple(pub_paper):
            message = ""
            message += "存在记录与目标不一致 相关记录为\n"
            for row in results:
                message += "教师工号:" + row[0] + "\n"
                message += "论文序号:" + str(row[1]) + "\n"
                message += "作者排名:" + str(row[2]) + "\n"
                message += "是否通讯作者:" + str(row[3]) + "\n"
            message += "请删除后再添加"
            message_box = QMessageBox()
            message_box.setWindowTitle("存在不一致记录")
            message_box.setText(message)
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        elif len(results) == 0:

            # 检测是否有其他通讯作者
            if pub_paper[3] == 1:
                sql = f"SELECT * FROM PubPaper WHERE sequence = {sequence} and IsConAuthor = 1"
                cursor.execute(sql)
                results = cursor.fetchall()
                if len(results) != 0 and results[0][0] != teacher_id:
                    message_box = QMessageBox()
                    message_box.setWindowTitle("多个通讯作者")
                    message_box.setText(f"存在另一个通讯作者，其id为{results[0][0]}")
                    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    message_box.exec()
                    return

            # 检测rank是否重复
            sql = f"SELECT * FROM PubPaper WHERE sequence = {sequence} and Pubrank = {pub_paper[2]}"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0 and results[0][0] != teacher_id:
                message_box = QMessageBox()
                message_box.setWindowTitle("排名重复！")
                message_box.setText(f"存在另一个排名为{pub_paper[2]}的作者,其教师id为{results[0][0]}")
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.exec()
                return
            sql = f"INSERT INTO PubPaper VALUE('{pub_paper[0]}', {pub_paper[1]}, {pub_paper[2]}, {pub_paper[3]})"
            cursor.execute(sql)
    conn.commit()




