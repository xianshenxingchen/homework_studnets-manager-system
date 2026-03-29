import random
import os
from datetime import datetime

# ====================== 1. 学生数据类 Student ======================
class Student:
    """学生数据类，用于封装单个学生的属性信息"""
    def __init__(self, stu_id, name, gender, cls, college):
        """初始化学生对象的属性"""
        self.id = stu_id       # 学号（原始格式，不做任何处理）
        self.name = name       # 姓名
        self.gender = gender   # 性别
        self.class_ = cls      # 班级
        self.college = college # 学院

    def __str__(self):
        """打印学生对象时自动输出友好信息"""
        return f"学号：{self.id}，姓名：{self.name}，性别：{self.gender}，班级：{self.class_}，学院：{self.college}"

# ====================== 2. 考试管理系统类 ExamSystem ======================
class ExamSystem:
    """考试管理系统，封装所有业务逻辑功能"""
    def __init__(self):
        self.students = []  # 存储所有学生对象

    @staticmethod
    def validate_id(stu_id):
        """静态方法：校验学号是否非空且有效"""
        return stu_id is not None and len(stu_id.strip()) > 0

    def create_student_file(self):
        """
        程序启动时自动创建学生文件
        使用制表符\t分隔，完全匹配你的原始数据格式
        """
        filename = "人工智能编程语言学生名单.txt"
        # 如果文件已存在，不覆盖，避免原有数据丢失
        if os.path.exists(filename):
            return

        # 文件不存在，自动创建并写入你提供的原始数据（制表符分隔）
        try:
            with open(filename, "w", encoding="utf-8") as f:
                # 表头+10条数据，全部用\t分隔，和读取逻辑一致
                f.write("序号\t姓名\t性别\t班级\t学号\t学院\n")
                f.write("1\t张三\t男\t1\t2001101\t电气\n")
                f.write("2\t李四\t女\t2\t2001102\t能动\n")
                f.write("3\t魏五\t男\t3\t2001103\t能动\n")
                f.write("4\t丁七\t女\t1\t2001104\t电气\n")
                f.write("5\t王八\t男\t2\t2001105\t计算机\n")
                f.write("6\t何九\t女\t3\t2001106\t计算机\n")
                f.write("7\t赵十\t男\t1\t2001107\t外国语\n")
                f.write("8\t吴一\t女\t2\t2001108\t外国语\n")
                f.write("9\t蓝二\t男\t3\t2001109\t经管\n")
                f.write("10\t刘六\t女\t1\t2001110\t经管\n")
            print("学生名单文件不存在，已使用你提供的数据自动创建完成")
        except Exception as e:
            print(f"创建文件失败：{e}")
            os._exit(1)

    def load_students_from_file(self):
        """从文件中读取学生信息并封装为学生对象，保证字段精准匹配"""
        filename = "人工智能编程语言学生名单.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # 跳过表头，从第二行开始读取数据
            for line_num, line in enumerate(lines[1:], 2):
                line = line.strip()
                if not line:
                    continue  # 跳过空行
                # 按制表符\t分割，和写入逻辑完全一致，避免字段错位
                data = line.split("\t")
                # 严格校验字段数量（必须6列），避免脏数据
                if len(data) != 6:
                    print(f"警告：第{line_num}行数据格式错误，已跳过")
                    continue
                # 解包字段：序号、姓名、性别、班级、学号、学院（精准对应）
                _, name, gender, cls_, stu_id, college = data
                # 创建学生对象并加入列表，学号原始存储
                student = Student(stu_id, name, gender, cls_, college)
                self.students.append(student)

            if len(self.students) == 0:
                print("错误：未加载到有效学生数据")
                os._exit(1)
            print(f"学生信息加载完成，共 {len(self.students)} 人")

        except FileNotFoundError:
            print(f"错误：未找到文件 {filename}")
            os._exit(1)
        except Exception as e:
            print(f"读取文件失败：{e}")
            os._exit(1)

    def search_student_by_id(self):
        """按学号查询学生信息，保证精准匹配"""
        stu_id = input("\n请输入要查询的学号：").strip()  # 仅去除首尾空格，保留原始格式
        # 调用静态方法校验学号
        if not ExamSystem.validate_id(stu_id):
            print("错误：学号不能为空或仅输入空格")
            return

        # 遍历查找匹配学号（完全相等匹配，无格式转换）
        for stu in self.students:
            if stu.id == stu_id:
                print("\n学生信息如下：")
                print(stu)
                return
        # 未找到时提示，同时给出示例，方便用户核对
        print(f"未找到学号为【{stu_id}】的学生，请检查学号是否输入正确")
        print("示例学号：2001101、2001102、2001110")

    def random_call_roll(self):
        """随机点名功能，处理输入异常和数量限制"""
        total = len(self.students)
        if total == 0:
            print("暂无学生数据")
            return

        while True:
            try:
                num = int(input(f"\n请输入点名人数（总人数：{total}）："))
                if num <= 0:
                    print("请输入大于0的正整数")
                elif num > total:
                    print(f"点名人数不能超过总人数 {total}，请重新输入")
                else:
                    break
            except ValueError:
                print("错误：请输入纯数字，不要输入字母、空格或符号")

        # 随机抽取不重复学生
        selected = random.sample(self.students, num)
        print("\n随机点名结果：")
        for i, stu in enumerate(selected, 1):
            print(f"{i}. 学号：{stu.id} | 姓名：{stu.name}")

    def generate_exam_table(self):
        """生成考场安排表，第一行带生成时间，格式规范"""
        if not self.students:
            print("暂无学生数据，无法生成考场安排表")
            return

        # 随机打乱学生顺序，保证每次生成结果不同
        shuffled = random.sample(self.students, len(self.students))
        # 获取当前系统时间，格式：年-月-日 时:分:秒
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open("考场安排表.txt", "w", encoding="utf-8") as f:
                f.write(f"生成时间：{now}\n")
                f.write("----------------------------------------\n")
                f.write("考场座位号\t姓名\t学号\n")
                f.write("----------------------------------------\n")
                for seat_num, stu in enumerate(shuffled, 1):
                    f.write(f"{seat_num}\t{stu.name}\t{stu.id}\n")
            print("考场安排表已生成：考场安排表.txt")
        except Exception as e:
            print(f"生成考场安排表失败：{e}")

    def generate_ticket_files(self):
        """生成准考证文件夹和对应学生的准考证文件，命名规范"""
        if not self.students:
            print("暂无学生数据，无法生成准考证文件")
            return

        # 定义准考证文件夹名称
        folder = "准考证"
        # 文件夹不存在则创建
        if not os.path.exists(folder):
            os.mkdir(folder)

        # 随机打乱学生顺序（与考场安排表一致）
        shuffled = random.sample(self.students, len(self.students))
        try:
            # 生成01.txt~10.txt格式的准考证文件
            for seat_num, stu in enumerate(shuffled, 1):
                filename = f"{folder}/{seat_num:02d}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"考场座位号：{seat_num}\n")
                    f.write(f"姓名：{stu.name}\n")
                    f.write(f"学号：{stu.id}\n")
            print("准考证文件夹与文件已全部生成完成！")
        except Exception as e:
            print(f"生成准考证失败：{e}")

    def show_menu(self):
        """显示系统功能菜单，简洁明了"""
        print("\n" + "="*40)
        print("        学生信息管理系统")
        print("="*40)
        print("1. 按学号查询学生信息")
        print("2. 随机点名")
        print("3. 生成考场安排表")
        print("4. 生成准考证文件")
        print("0. 退出程序")
        print("="*40)

    def run(self):
        """系统主运行入口，按流程执行"""
        self.create_student_file()    # 步骤1：自动创建学生文件（你的原始数据）
        self.load_students_from_file()# 步骤2：加载学生信息到系统
        # 步骤3：循环显示菜单，接收用户操作
        while True:
            self.show_menu()
            choice = input("请输入功能编号：").strip()
            if choice == "1":
                self.search_student_by_id()
            elif choice == "2":
                self.random_call_roll()
            elif choice == "3":
                self.generate_exam_table()
            elif choice == "4":
                self.generate_ticket_files()
            elif choice == "0":
                print("程序已退出，感谢使用！")
                break
            else:
                print("输入错误，请输入0-4之间的有效数字！")

# ====================== 程序主入口 ======================
if __name__ == "__main__":
    # 创建系统对象并启动
    exam_system = ExamSystem()
    exam_system.run()