# 这是一个一个面向教师的教学科研登记系统
## 实现的功能
### 登记发表论文情况：
提供教师论文发表信息的的增、删、改、查功能；输入时要求检查：一篇论文只能有一位通讯作者，论文的作者排名不能有重复，论文的类型和级别只
能在约定的取值集合中选取（实现时建议用下拉框）。
### 登记承担项目情况：
提供教师承担项目信息的增、删、改、查功能；输入时要求检查：
排名不能有重复，一个项目中所有教师的承担经费总额应等于项目的总经费，项目类型
只能在约定的取值集合中选取。
### 登记主讲课程情况：
提供教师主讲课程信息的增、删、改、查功能；输入时要求检查：
一门课程所有教师的主讲学时总额应等于课程的总学时，学期。
### 查询统计： 
实现按教师工号和给定年份范围汇总查询该教师的教学科研情况的功能；例如输入
工号“01234”，“2023-2023”可以查询 01234 教师在 2023 年度的教学科研工
作情况。
### 导出功能
实现按教师工号和给定年份范围生成教学科研工作量统计表并导出文档的功能，导出文档格式可以是 PDF、Word、Excel 等。
## 用户界面如下    
![image](https://github.com/user-attachments/assets/b57b1740-5cf7-4d0f-8608-7db92e8f5ba3)
![image](https://github.com/user-attachments/assets/52300a4a-0e77-43fd-a0c8-dc1d524236c5)
![image](https://github.com/user-attachments/assets/b1b47d67-6514-4dec-a690-d51ac4d7f5e3)
## 数据关系
![image](https://github.com/user-attachments/assets/bd822080-6a83-49f5-91b9-1cf7b983a5c5)
