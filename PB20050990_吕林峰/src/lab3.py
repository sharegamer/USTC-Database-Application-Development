import mysql.connector
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QDialog,QMessageBox
from PubPaperAdd import pub_paper_add_button
from PubPaperRmv import pub_paper_rmv_button
from PubPaperSlct import pub_paper_slct_button
from PubPaperAlt import pub_paper_alt_button
from TakeProAdd import take_project_add_button
from TakeProRmv import take_project_rmv_button
from TakeProAlt import take_project_alt_button
from TakeProSlct import take_project_slct_button
from TakeClassAdd import take_class_add_button
from TakeClassRmv import take_class_rmv_button
from TakeClassSlct import take_class_slct_button
from Query import query


class MyWindow(QWidget):

    def __init__(self, conn, cursor):
        super().__init__()
        self.conn = conn
        self.cursor = cursor
        self.initUI()

    def initUI(self):
        button1 = QPushButton("增加发表论文情况")
        button2 = QPushButton("删除发表论文情况")
        button3 = QPushButton("更改发表论文情况")
        button4 = QPushButton("查找发表论文情况")
        button5 = QPushButton("增加承担项目情况")
        button6 = QPushButton("删除承担项目情况")
        button7 = QPushButton("更改承担项目情况")
        button8 = QPushButton("查找承担项目情况")
        button9 = QPushButton("增加或更改主讲课程情况")
        button10 = QPushButton("删除课程")
        button12 = QPushButton("查找主讲课程情况")
        button13 = QPushButton("查询统计功能")
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(button1, 1, 0)
        grid.addWidget(button2, 1, 1)
        grid.addWidget(button3, 1, 2)
        grid.addWidget(button4, 1, 3)
        grid.addWidget(button5, 2, 0)
        grid.addWidget(button6, 2, 1)
        grid.addWidget(button7, 2, 2)
        grid.addWidget(button8, 2, 3)
        grid.addWidget(button9, 3, 0, 1, 2)
        grid.addWidget(button10, 3, 2)
        grid.addWidget(button12, 3, 3)
        grid.addWidget(button13, 4, 1, 1, 2)
        button1.setFixedHeight(80)
        button2.setFixedHeight(80)
        button3.setFixedHeight(80)
        button4.setFixedHeight(80)
        button5.setFixedHeight(80)
        button6.setFixedHeight(80)
        button7.setFixedHeight(80)
        button8.setFixedHeight(80)
        button9.setFixedHeight(80)
        button10.setFixedHeight(80)
        button12.setFixedHeight(80)
        button13.setFixedHeight(80)
        # 将每个按钮的点击事件连接到相应的处理函数
        button1.clicked.connect(self.btn1)
        button2.clicked.connect(self.btn2)
        button3.clicked.connect(self.btn3)
        button4.clicked.connect(self.btn4)
        button5.clicked.connect(self.btn5)
        button6.clicked.connect(self.btn6)
        button7.clicked.connect(self.btn7)
        button8.clicked.connect(self.btn8)
        button9.clicked.connect(self.btn9)
        button10.clicked.connect(self.btn10)
        button12.clicked.connect(self.btn12)
        button13.clicked.connect(self.btn13)
        self.setLayout(grid)
        # 窗口左上角位于屏幕坐标(200, 200)，宽度为 1000 像素，高度为550像素。
        self.setGeometry(200, 200, 1000, 550)
        self.setWindowTitle('欢迎使用教学科研登记系统 作者：吕林峰 PB20050990')
        self.show()

    def btn1(self):
        btn1_window = pub_paper_add_button(self.conn, self.cursor)
        btn1_window.exec()

    def btn2(self):
        btn2_window = pub_paper_rmv_button(self.conn, self.cursor)
        btn2_window.exec()

    def btn3(self):
        btn3_window = pub_paper_alt_button(self.conn, self.cursor)
        btn3_window.exec()

    def btn4(self):
        btn4_window = pub_paper_slct_button(self.conn, self.cursor)
        btn4_window.exec()

    def btn5(self):
        btn5_window = take_project_add_button(self.conn, self.cursor)
        btn5_window.exec()

    def btn6(self):
        btn6_window = take_project_rmv_button(self.conn, self.cursor)
        btn6_window.exec()

    def btn7(self):
        btn7_window = take_project_alt_button(self.conn, self.cursor)
        btn7_window.exec()

    def btn8(self):
        btn8_window = take_project_slct_button(self.conn, self.cursor)
        btn8_window.exec()

    def btn9(self):
        btn9_window = take_class_add_button(self.conn, self.cursor)
        btn9_window.exec()

    def btn10(self):
        btn10_window = take_class_rmv_button(self.conn, self.cursor)
        btn10_window.exec()

    def btn12(self):
        btn12_window = take_class_slct_button(self.conn, self.cursor)
        btn12_window.exec()

    def btn13(self):
        btn13_window = query(self.conn, self.cursor)
        btn13_window.exec()

    # 重载closeEvent方法：
    # 如果用户选择
    # "Yes"，则执行数据库提交操作并关闭游标和连接。
    # 如果用户选择
    # "No"，则忽略关闭事件，窗口保持打开状态。
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认退出', '你确定要退出吗？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.conn.commit()  # 提交数据库更改
                self.cursor.close()  # 关闭游标
                self.conn.close()  # 关闭数据库连接
            except Exception as e:
                QMessageBox.critical(self, '错误', f'提交数据库更改时出错: {e}')
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="Lab3"
    )
    cursor = conn.cursor()
    app = QApplication(sys.argv)
    window = MyWindow(conn, cursor)
    sys.exit(app.exec())

    # 关闭游标和连接
    conn.commit()
    cursor.close()
    conn.close()
