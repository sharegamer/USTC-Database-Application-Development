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


class take_project_add_button(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle("请输入教师及项目信息")

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel("教师工号:", self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        self.teacher_id_input.setPlaceholderText("可选，只增加项目时可以不输入")
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel("教师承担项目排名:", self)
        layout.addWidget(label2)
        self.rank_input = QLineEdit(self)
        self.rank_input.setPlaceholderText("只增加项目时可以不输入")
        layout.addWidget(self.rank_input)

        label3 = QLabel("教师承担经费:", self)
        layout.addWidget(label3)
        self.fund_input = QLineEdit(self)
        self.fund_input.setPlaceholderText("只增加项目时可以不输入")
        layout.addWidget(self.fund_input)

        label4 = QLabel("项目号:", self)
        layout.addWidget(label4)
        self.seq_input = QLineEdit(self)
        self.seq_input.setPlaceholderText("必填")
        layout.addWidget(self.seq_input)

        label9 = QLabel("项目名称:", self)
        layout.addWidget(label9)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("可选，已有该项目时可以不输入")
        layout.addWidget(self.name_input)

        label5 = QLabel("项目来源:", self)
        layout.addWidget(label5)
        self.src_input = QLineEdit(self)
        self.src_input.setPlaceholderText("可选，已有该项目时可以不输入")
        layout.addWidget(self.src_input)

        label7 = QLabel("项目类型:", self)
        layout.addWidget(label7)
        self.type_combo = QComboBox()
        self.type_combo.addItem("0-已有该项目时可以不输入")
        self.type_combo.addItem("1-国家级项目")
        self.type_combo.addItem("2-省部级项目")
        self.type_combo.addItem("3-市厅级项目")
        self.type_combo.addItem("4-企业合作项目")
        self.type_combo.addItem("5-其他类型项目")
        layout.addWidget(self.type_combo)

        label10 = QLabel("项目开始年份:", self)
        layout.addWidget(label10)
        self.beg_year_input = QLineEdit(self)
        self.beg_year_input.setPlaceholderText("可选，已有该项目时可以不输入")
        layout.addWidget(self.beg_year_input)

        label8 = QLabel("项目结束年份:", self)
        layout.addWidget(label8)
        self.end_year_input = QLineEdit(self)
        self.end_year_input.setPlaceholderText("可选，已有该项目时可以不输入")
        layout.addWidget(self.end_year_input)

        help_btn = QPushButton("帮助", self)
        help_btn.clicked.connect(self.showhelp)
        layout.addWidget(help_btn)

        button = QPushButton("确定", self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def showhelp(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("帮助")
        message_box.setText(
            "可以实现仅插入项目信息和插入教师承担项目记录\n前者可以不输入项目相关信息\n后者也可插入项目信息" "\n如果论文是现有项目只需输入项目号即可"
        )
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
        if teacher_id == "":
            take_pro = None
        else:
            take_pro = [teacher_id, seq, rank, fund]
        if name == "":
            project = None
        else:
            project = [seq, name, src, type2, 0, beg_year, end_year]
        if seq == "":
            message_box = QMessageBox()
            message_box.setWindowTitle("Error！")
            message_box.setText("项目号不能为空")
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return
        take_pro_add(self.conn, self.cursor, teacher_id, seq, take_pro, project)
        reply = QMessageBox.question(
            self,
            "操作完成！",
            "操作完成，是否继续插入?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def take_pro_add(conn, cursor, teacher_id, sequence, take_pro, project):
    # 先检查是否有对应的项目，没有的话会直接替换
    sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        # 只插项目的话 总经费是0
        # 总经费改动在插入承担工程记录时更改
        sql = (
            f"INSERT INTO Project VALUE('{project[0]}', '{project[1]}', '{project[2]}', {project[3]}, {0}, "
            f"{project[5]}, {project[6]})"
        )
        cursor.execute(sql)
    else:
        # 存在项目但是与目标项目信息不一致
        if project is not None:
            project[4] = results[0][4]
            temppro = project
            temppro[5] = to_int(project[5])
            temppro[6] = to_int(project[6])
            if results[0] != tuple(temppro):
                message = ""
                message += "存在项目与目标不一致 相关记录为\n"
                for row in results:
                    message += "项目号:" + row[0] + "\n"
                    message += "项目名称:" + row[1] + "\n"
                    message += "项目来源:" + row[2] + "\n"
                    message += "项目类型:" + str(row[3]) + "\n"
                    message += "总经费:" + str(row[4]) + "\n"
                    message += "开始年费:" + str(row[5]) + "\n"
                    message += "结束年份:" + str(row[6]) + "\n"
                message += "请删除后再添加"
                message_box = QMessageBox()
                message_box.setWindowTitle("存在不一致记录")
                message_box.setText(message)
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.exec()
                return

        # 先查重 检测承担记录是否有重复
    if take_pro is not None:
        sql = f"SELECT * FROM TakeProject WHERE TeacherID = '{teacher_id}' AND sequence = '{sequence}'"
        cursor.execute(sql)
        results = cursor.fetchall()
        temptake = take_pro
        temptake[2] = to_int(take_pro[2])
        temptake[3] = to_int(take_pro[3])
        if len(results) != 0 and results[0] != tuple(temptake):
            message = ""
            message += "存在记录与目标不一致 相关记录为\n"
            for row in results:
                message += "教师工号:" + row[0] + "\n"
                message += "项目号:" + row[1] + "\n"
                message += "教师排名:" + str(row[2]) + "\n"
                message += "教师承担经费:" + str(row[3]) + "\n"
            message += "请删除后再添加"
            message_box = QMessageBox()
            message_box.setWindowTitle("存在不一致记录")
            message_box.setText(message)
            message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            message_box.exec()
            return

        elif len(results) == 0:
            # 检测rank是否重复
            sql = f"SELECT * FROM TakeProject WHERE sequence = '{sequence}' and Takerank = {take_pro[2]}"
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0 and results[0][0] != teacher_id:
                message_box = QMessageBox()
                message_box.setWindowTitle("排名重复！")
                message_box.setText(f"存在另一个排名为{take_pro[2]}的作者,其教师id为{results[0][0]}")
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.exec()
                return

            # 无对应记录 插入新纪录
            sql = f"SELECT * FROM Project WHERE sequence = '{sequence}'"
            cursor.execute(sql)
            results = cursor.fetchall()
            total_fund = results[0][4]
            total_fund += float(take_pro[3])
            sql = f"UPDATE Project SET ProjectFund = {total_fund} WHERE sequence = '{sequence}'"
            cursor.execute(sql)
            sql = (
                f"INSERT INTO TakeProject VALUE('{take_pro[0]}', '{take_pro[1]}',"
                f"{take_pro[2]}, {take_pro[3]})"
            )
            cursor.execute(sql)
    conn.commit()
