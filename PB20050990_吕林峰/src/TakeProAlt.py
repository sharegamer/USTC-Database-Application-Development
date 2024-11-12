import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout


class take_project_alt_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入教师及项目信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只更改项目时请勿输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('教师承担项目排名:', self)
        layout.addWidget(label2)
        self.rank_input = QLineEdit(self)
        self.rank_input.setPlaceholderText("只更改项目时可以不输入")
        layout.addWidget(self.rank_input)

        label3 = QLabel('教师承担经费:', self)
        layout.addWidget(label3)
        self.fund_input = QLineEdit(self)
        self.fund_input.setPlaceholderText("只更改项目时可以不输入")
        layout.addWidget(self.fund_input)

        label4 = QLabel('项目号:', self)
        layout.addWidget(label4)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("必填")
        layout.addWidget(self.seq_input)

        label9 = QLabel('项目名称(新值):', self)
        layout.addWidget(label9)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("可选，不更改项目信息时可以不输入")
        layout.addWidget(self.name_input)

        label5 = QLabel('项目来源(新值):', self)
        layout.addWidget(label5)
        self.src_input = QLineEdit(self)
        self.src_input.setPlaceholderText("可选，不更改项目信息时可以不输入")
        layout.addWidget(self.src_input)

        label7 = QLabel('项目类型(新值):', self)
        layout.addWidget(label7)
        self.type_combo = QComboBox()
        self.type_combo.addItem("0-不更改项目信息时可以不输入")
        self.type_combo.addItem("1-国家级项目")
        self.type_combo.addItem("2-省部级项目")
        self.type_combo.addItem("3-市厅级项目")
        self.type_combo.addItem("4-企业合作项目")
        self.type_combo.addItem("5-其他类型项目")
        layout.addWidget(self.type_combo)

        label10 = QLabel('项目开始年份(新值):', self)
        layout.addWidget(label10)
        self.beg_year_input = QLineEdit(self)
        self.beg_year_input.setPlaceholderText("可选，不更改项目信息时可以不输入")
        layout.addWidget(self.beg_year_input)

        label8 = QLabel('项目结束年份(新值):', self)
        layout.addWidget(label8)
        self.end_year_input = QLineEdit(self)
        self.end_year_input.setPlaceholderText("可选，不更改项目信息时可以不输入")
        layout.addWidget(self.end_year_input)

        help_btn = QPushButton('帮助', self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText("需要改什么就填什么\n可以只更改项目信息")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        rank = self.rank_input.text()
        fund = self.fund_input.text()
        seq = self.seq_input.text()
        name = self.name_input.text()
        src = self.src_input.text()
        beg_year = self.beg_year_input.text()
        end_year = self.end_year_input.text()
        type2 = self.type_combo.currentIndex()
        take_pro = [teacher_id, seq, rank, fund]
        project = [seq, name, src, type2, 0, beg_year, end_year]
        if seq is None:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("项目号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        take_pro_alt(self.conn, self.cursor, teacher_id, seq, take_pro, project)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，是否继续更改?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def take_pro_alt(conn, cursor, teacher_id, sequence, take_pro, project):
    # 根据teaherID改关系
    # teacherID留空视为只改项目
    if teacher_id != "":
        sql = f"SELECT * FROM TakeProject WHERE TeacherID = '{teacher_id}' AND sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有找到对应的教师和项目记录")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        else:
            sql = "UPDATE TakeProject SET "
            if take_pro[2] != '':
                # 检测rank是否重复
                sql2 = f"SELECT * FROM TakeProject WHERE sequence = '{sequence}' and Takerank = {take_pro[2]}"
                cursor.execute(sql2)
                results = cursor.fetchall()
                if len(results) != 0 and results[0][0] != teacher_id:
                    message_box = QMessageBox()
                    message_box.setWindowTitle("排名重复！")
                    message_box.setText(f"存在另一个排名为{take_pro[2]}的作者,其教师id为{results[0][0]}")
                    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                    message_box.exec()
                    return
                sql += f"Takerank = {take_pro[2]},"
            if take_pro[3] != '':
                sql2 = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
                cursor.execute(sql2)
                results2 = cursor.fetchall()
                old_fund = results2[0][4]
                new_fund = old_fund + float(take_pro[3]) - float(results[0][3])
                sql2 = f"UPDATE Project SET ProjectFund = {new_fund} WHERE sequence = '{sequence}'"
                cursor.execute(sql2)
                sql += f"TakeFund = {take_pro[3]},"
            sql = sql[:-1]
            sql += f" WHERE sequence = '{sequence}' AND TeacherID = '{teacher_id}'"
            cursor.execute(sql)
        sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if project[1] == "" and project[2] == "" and project[3] == 0 and project[5] == "" and project[6] == "":
            conn.commit()
            return
        reply = QMessageBox.question(None, '是否修改项目信息', '检测到项目信息有输入 是否修改?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            sql = "UPDATE Project SET "
            if project[1] != "":
                sql += f"ProjectName = '{project[1]}',"
            if project[2] != "":
                sql += f"ProjectSource = '{project[2]}',"
            if project[3] != 0:
                sql += f"ProjectType = {project[3]},"
            if project[5] != "":
                sql += f"ProBeginYear = {project[5]},"
            if project[6] != "":
                sql += f"ProEndYear = {project[6]},"
            sql = sql[:-1]
            sql += f" WHERE sequence = '{sequence}'"
            cursor.execute(sql)
    else:
        sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 0:
            message_box = QMessageBox()
            message_box.setWindowTitle("Not Found!")
            message_box.setText("没有对应的项目")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        sql = "UPDATE Project SET "
        if project[1] != "":
            sql += f"ProjectName = '{project[1]}',"
        if project[2] != "":
            sql += f"ProjectSource = '{project[2]}',"
        if project[3] != 0:
            sql += f"ProjectType = {project[3]},"
        if project[5] != "":
            sql += f"ProBeginYear = {project[5]},"
        if project[6] != "":
            sql += f"ProEndYear = {project[6]},"
        sql = sql[:-1]
        sql += f" WHERE sequence = '{sequence}'"
        cursor.execute(sql)
    conn.commit()
