use lab3;
DELETE From Teacher;
DELETE From Paper;
DELETE From Class;
DELETE From Pubpaper;
insert into Teacher value('t1', '张三', 1, 1);
insert into Teacher value('t2', '李四', 1, 4);
insert into Teacher value('t3', '王五', 2, 3);
insert into Teacher value('t4', '赵六', 1, 2);
insert into Class value('c1',"数学分析", 80,1);
insert into Class value('c2',"线性代数", 40,1);
insert into Class value('c3',"数理逻辑", 40,1);
insert into Paper value(10, "母猪的产后护理", "医学杂志", 2022, 1, 1);
insert into Paper value(11, "数学分析", "数学杂志", 2023, 2, 2);
insert into Pubpaper value('t1', 10, 1, 1);
insert into Pubpaper value('t2', 10, 2, 0);
insert into Pubpaper value('t1', 11, 1, 1);