import csv
from datetime import datetime


def convert_date_format(date_str, current_format, target_format):
    current_date = datetime.strptime(date_str, current_format)  # 解析当前格式的时间字符串
    target_date_str = current_date.strftime(target_format)  # 将时间转换为目标格式的字符串
    return target_date_str


class Award:
    def __init__(
        self,
        time,
        type,
        award_level,
        award_title,
        award_grade,
        issuer,
        rank_in_group,
        group_total,
        note,
        has_certificate,
    ):
        self.time = time
        self.type = type
        self.award_level = award_level
        self.award_title = award_title
        self.award_grade = award_grade
        self.issuer = issuer
        self.rank_in_group = rank_in_group
        self.group_total = group_total
        self.note = note
        self.has_certificate = has_certificate


def read_award(path):
    # 打开CSV文件
    with open(path, "r", encoding="utf-8-sig") as file:
        # 创建CSV读取器
        reader = csv.reader(file)

        # 跳过CSV文件的标题行
        next(reader)

        # 存储所有奖项对象的列表
        awards = []

        # 遍历每一行数据
        for row in reader:
            # 读取每一列数据
            time = row[0]
            type = row[1]
            award_level = row[2]
            award_title = row[3]
            award_location = row[4]
            issuer = row[5]
            rank_in_group = row[6]
            group_total = row[7]
            note = row[8]
            has_certificate = row[9]

            # 创建Award对象并添加到列表中
            award = Award(
                time,
                type,
                award_level,
                award_title,
                award_location,
                issuer,
                rank_in_group,
                group_total,
                note,
                has_certificate,
            )
            awards.append(award)

    return awards


def print_award(award):
    print("时间:", award.time)
    print("类别:", award.type)
    print("层次:", award.award_level)
    print("名称:", award.award_title)
    print("等级:", award.award_grade)
    print("颁发单位:", award.issuer)
    print("组内排名:", award.rank_in_group)
    print("组总人数:", award.group_total)
    print("备注:", award.note)
    print("是否有证书:", award.has_certificate)
    print("-------------------")


def print_member():
    print(
        """成员变量、编号、其他控制符的符号列表：
|\t在此处分列
#\t标识序号
0\ttime：时间
1\ttype：类别（学科竞赛、荣誉表彰、科研成果）
2\taward_level：层次（国、省、校、院）
3\taward_title：名称（如“蓝桥杯”）
4\taward_grade：等级（如“一等奖”）
5\tissuer：颁发单位（如“南京大学”）
6\trank_in_group：组内排名
7\tgroup_total：组总人数
8\tnote：备注
9\thas_certificate：是否有证书"""
    )


def change_time_format(award, target_format):
    award.time = convert_date_format(award.time, r"%Y-%m-%d", target_format)


def export_to_csv(awards, handle, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        i = 0  # i 记录当前是第几个奖项
        for award in awards:
            i += 1
            j = 0  # j 记录当前是第几个单元格
            row = []
            row.append("")
            for char in handle:  # 对于每一个控制字符
                if char.isdigit():  # 如果是序号，则找到序号对应的成员变量
                    index = int(char)
                    attribute_name = list(award.__dict__.keys())[index]
                    value = getattr(award, attribute_name)
                    row[j] += value
                elif char == "#":
                    row[j] += str(i)
                elif char == "|":
                    row.append("")
                    j += 1
                else:
                    row[j] += char
            writer.writerow(row)


def main():
    PATH = str(input(r"请输入奖项.csv文件的绝对路径（注意：需要符合.csv模板）"))
    OUT = PATH[:-4] + "(MODIFIED).csv"
    awards = read_award(PATH)
    print(f"一共读取了{len(awards)}个奖项")
    print(r"请输入你想要改写成的日期格式。日期控制符参考：对于20020304，%Y=2002；%y=02；%m=03；%d=04")
    target_format = str(input("如果无需改写，使用回车跳过："))
    if len(target_format) > 0:
        for award in awards:
            change_time_format(award, target_format)
    print_member()
    handle = str(input('请输入你想要改写成的文件格式。例如"#|0|1|2|34|6/7"：'))
    export_to_csv(awards, handle, OUT)
    print(f"改写完成，文件路径为{OUT}")


if __name__ == "__main__":
    main()
