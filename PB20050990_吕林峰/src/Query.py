import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog, QVBoxLayout
import jinja2
from docxtpl import DocxTemplate


teacher_title = [
    "",
    "博士后",
    "助教",
    "讲师",
    "副教授",
    "特任教授",
    "教授",
    "助理研究员",
    "特任副研究员",
    "副研究员",
    "特任研究员",
    "研究员"
]

paper_type = [
    "",
    "full paper",
    "short paper",
    "poster paper",
    "demo paper"
]

paper_level = [
    "",
    "CCF-A",
    "CCF-B",
    "CCF-C",
    "中文 CCF-A",
    "中文 CCF-B",
    "无级别"
]

project_type = [
    "",
    "国家级项目",
    "省部级项目",
    "市厅级项目",
    "企业合作项目",
    "其他类型项目"
]

term = [
    "",
    "春",
    "夏",
    "秋"
]

class_type = [
    "",
    "本科生课程",
    "研究生课程"
]

is_conn = ["", ", 通讯作者"]


class query(QDialog):
    def __init__(self, conn, cursor, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.cursor = cursor
        self.setWindowTitle('请输入信息')

        layout = QVBoxLayout()
        self.setLayout(layout)

        label1 = QLabel('教师工号:', self)
        layout.addWidget(label1)
        self.teacher_id_input = QLineEdit(self)
        layout.addWidget(self.teacher_id_input)

        label2 = QLabel('开始年份:', self)
        layout.addWidget(label2)
        self.year1_input = QLineEdit(self)
        layout.addWidget(self.year1_input)

        label3 = QLabel('结束年份:', self)
        layout.addWidget(label3)
        self.year2_input = QLineEdit(self)
        layout.addWidget(self.year2_input)

        button = QPushButton('确定', self)
        button.clicked.connect(self.click_button)
        layout.addWidget(button)

    def click_button(self):
        teacher_id = self.teacher_id_input.text()
        year1 = self.year1_input.text()
        year2 = self.year2_input.text()
        my_query(self.conn, self.cursor, teacher_id, year1, year2)
        reply = QMessageBox.question(self, '操作完成！', '操作完成，文件输入到目录下的output.docx下,\n是否继续查询?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            self.accept()


def my_query(conn, cursor, teacher_id, year1, year2):
    data = {'year1': year1, 'year2': year2, 'id': teacher_id}
    sql = f"SELECT * FROM Teacher WHERE TeacherID = '{teacher_id}' "
    cursor.execute(sql)
    results = cursor.fetchall()
    data['name'] = results[0][1]
    if results[0][2] == 1:
        data["sex"] = "男"
    else:
        data["sex"] = "女"
    class_info = ""
    paper_info = ""
    project_info = ""
    data["Title"] = teacher_title[results[0][3]]
    sql = f"SELECT PaperName, PaperSource, PaperYear, PaperType, PaperGrade, Pubrank, IsConAuthor" \
          f" FROM Paper INNER JOIN PubPaper ON Paper.sequence = PubPaper.sequence " \
          f"WHERE TeacherID = '{teacher_id}' and PaperYear >= {year1} and PaperYear <= {year2}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        i = 0
        for row in results:
            i += 1
            paper_info += f"{i}.{row[0]}, {row[1]}, {row[2]}, {paper_level[row[3]]}, 排名第{row[4]}{is_conn[row[5]]}\n"
        pass
    else:
        paper_info = "无"

    sql = f"SELECT Class.ClassID, ClassName, TakeHour, ClassYear, ClassTerm" \
          f" FROM Class INNER JOIN TakeClass ON Class.ClassID = TakeClass.ClassID " \
          f"WHERE TeacherID = '{teacher_id}' and ClassYear >= {year1} and ClassYear <= {year2}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        i = 0
        for row in results:
            i += 1
            class_info += f" 课程号:{row[0]}\t课程名:{row[1]}\t主讲学时:{row[2]}\t学期:{row[3]} {term[row[4]]}\n"
        pass
    else:
        class_info = "无"

    sql = f"SELECT ProjectName, ProjectSource, ProjectType, ProBeginYear, ProEndYear, ProjectFund, TakeFund" \
          f" FROM Project INNER JOIN TakeProject ON Project.sequence = TakeProject.sequence " \
          f"WHERE TeacherID = '{teacher_id}' and ProEndYear >= {year1} and ProBeginYear <= {year2}"
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) != 0:
        i = 0
        for row in results:
            i += 1
            project_info += f" {i}.{row[0]}, {row[1]}, {project_type[row[2]]}, " \
                            f"{row[3]} - {row[4]}, 总经费: {row[5]}, 承担经费: {row[6]}\n"
        pass
    else:
        project_info = "无"

    data["class"] = class_info
    data["paper"] = paper_info
    data["project"] = project_info

    # 保存生成的Word文档
    tpl = DocxTemplate('template.docx')
    jinja_env = jinja2.Environment()  # Jinja2环境 可以自定义渲染规则 默认就行了
    tpl.render(data, jinja_env)
    tpl.save("output.docx")
    output_path = 'output2.docx'


