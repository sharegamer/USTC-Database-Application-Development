CREATE DATABASE IF NOT EXISTS lab3;

USE lab3;

DROP TABLE IF EXISTS PubPaper;
DROP TABLE IF EXISTS TakeProject;
DROP TABLE IF EXISTS TakeClass;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS Paper;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Class;

CREATE TABLE Teacher (
	TeacherID VARCHAR(5) PRIMARY KEY,
    TeacherName VARCHAR(256),
    sex INT,
    JobTitle INT,
    CHECK (sex IN (1, 2)),
    CHECK (JobTitle IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
    ) DEFAULT CHARSET=UTF8;
    
CREATE TABLE Paper(
	sequence INT PRIMARY KEY,
    PaperName VARCHAR(256),
    PaperSource VARCHAR(256),
    PaperYear Year,
    PaperType INT,
    PaperGrade INT,
    CHECK (PaperType IN (1, 2, 3, 4)),
    CHECK (PaperGrade IN (1, 2, 3, 4, 5, 6))
)DEFAULT CHARSET=UTF8;

CREATE TABLE Project(
	sequence VARCHAR(256) PRIMARY KEY,
    ProjectName VARCHAR(256),
    ProjectSource VARCHAR(256),
    ProjectType INT,
    ProjectFund FLOAT,
    ProBeginYear Year,
    ProEndYear Year,
    CHECK (ProjectType IN (1, 2, 3, 4, 5))
)DEFAULT CHARSET=UTF8;

CREATE TABLE Class(
	ClassID VARCHAR(256) PRIMARY KEY,
    ClassName VARCHAR(256),
    ClassHour INT,
    ClassType INT,
    check (ClassType IN (1, 2))
)DEFAULT CHARSET=UTF8;

CREATE TABLE PubPaper(
	TeacherID VARCHAR(5),
    sequence INT,
    Pubrank INT,
    IsConAuthor Boolean,
	PRIMARY KEY (TeacherID , sequence),
    FOREIGN KEY (TeacherID)
        REFERENCES Teacher (TeacherID),
    FOREIGN KEY (sequence)
        REFERENCES Paper (sequence),
	check (Pubrank >= 1)
)DEFAULT CHARSET=UTF8;

CREATE TABLE TakeProject(
	TeacherID VARCHAR(5),
    sequence VARCHAR(256),
    Takerank INT,
    TakeFund FLOAT,
	PRIMARY KEY (TeacherID , sequence),
    FOREIGN KEY (TeacherID)
        REFERENCES Teacher (TeacherID),
    FOREIGN KEY (sequence)
        REFERENCES Project (sequence),
	check (Takerank >= 1)
)DEFAULT CHARSET=UTF8;

CREATE TABLE TakeClass(
	TeacherID VARCHAR(5),
    ClassID VARCHAR(256),
    ClassYear Year,
    ClassTerm INT,
    TakeHour INT,
	PRIMARY KEY (TeacherID , ClassID, ClassYear, ClassTerm),
    FOREIGN KEY (TeacherID)
        REFERENCES Teacher (TeacherID),
    FOREIGN KEY (ClassID)
        REFERENCES Class (ClassID),
	check (ClassTerm IN (1, 2, 3))
)DEFAULT CHARSET=UTF8;

insert into Teacher value('t1', '张三', 1, 1);
insert into Teacher value('t2', '李四', 1, 4);
insert into Teacher value('t3', '王五', 2, 3);
insert into Teacher value('t4', '赵六', 1, 2);
insert into Class value('c1',"数学分析", 80,1);
insert into Class value('c2',"线性代数", 40,1);
insert into Class value('c3',"数理逻辑", 40,1);
insert into Paper value(10, "人工智能", "计算机杂志", 2022, 1, 1);
insert into Paper value(11, "数学分析", "数学杂志", 2023, 2, 2);