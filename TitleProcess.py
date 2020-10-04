# 程序功能：从文本文档中提取CCNA在线课件的章节页编号与标题，并保存到另一个文本文件中（用于下一步导入到Excel当中）


import re

SourceFileName = "TitleList.txt"
UsefulFileName = "UsefulTitleList.txt"
UsefulContents = []


# 函数功能：接收1个字符串，功能是判断字符串是否能够匹配正则表达式，返回值为布尔值
def check_line(line):
    useful_line_regex = re.compile(r'\"\);$')
    check_result = useful_line_regex.search(line)
    if check_result:
        return True
    else:
        return False


# 函数功能：接收1个字符串，功能是按照特定规则截取字符串的部分内容拼接成符合需要的新字符串，并返回该字符串
def cutdown(line):
    parts = line.split('"')
    newline = parts[1] + '\t' + parts[3] + '\n'
    newline = newline.replace('.', '\t\t')
    return newline


with open(SourceFileName, 'r', encoding="(utf8)") as file_object:
    contents = file_object.readlines()

for i in range(len(contents)):
    if check_line(contents[i]):
        NewLine = contents[i]
        NewLine = cutdown(NewLine)
        UsefulContents.append(NewLine)

print('一共有 {} 行Useful Line 将被写入到新文件！'.format(str(len(UsefulContents))))

with open(UsefulFileName, 'w', encoding="(utf8)") as file_object:
    for i in range(len(UsefulContents)):
        file_object.write(UsefulContents[i])

print('写入操作完成，已经把 {} 行数据写入到文件 {} 中。'.format(str(len(UsefulContents)), UsefulFileName))
