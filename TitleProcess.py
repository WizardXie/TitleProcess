# 程序功能：从文本文档中提取CCNA在线课件的章节页编号与标题，并保存到另一个文本文件中（用于下一步导入到Excel当中）
# TODO:
# DONE:应添加关于文件处理的异常处理代码

import re

SourceFileName = "TitleList.txt"        # 原始数据所在文件名
UsefulFileName = "UsefulTitleList.txt"  # 处理后的数据要写入的文件名
UsefulContents = []                     # 用于暂存要写入的内容
MaxTabCount = 4                         # 每行应该至少有4个\t

# 函数功能：接收1个字符串，功能是判断字符串是否能够匹配正则表达式，返回值为布尔值


def check_line(line: str):
    useful_line_regex = re.compile(r'\"\);$')
    check_result = useful_line_regex.search(line)
    if check_result:
        return True
    else:
        return False

# 函数功能：接收1个字符串，功能是按照特定规则（以双引号为分隔符）截取字符串的部分内容拼接成符合需要的新字符串，并返回该字符串


def cutdown(line: str):
    parts = line.split('"')
    newline = parts[1] + '\t' + parts[3] + '\n'
    newline = newline.replace('.', '\t')
    return newline

# 函数功能：如果章节标题达不到足够的长度，补足相应的\t


def addup(line: str):
    count = 0
    for char in line:   # 计算当前行中所包含的 \t 的个数
        if char == '\t':
            count += 1
    if count == MaxTabCount:    # 如果当前行中所包含的 \t 的个数已经达到最大值，则直接返回该行
        return line
    if count < MaxTabCount:     # 如果当前行中所包含的 \t 的个数＜最大值，则需要补充\t
        parts = line.split('\t')
        length = len(parts)
        i = 0
        while i <= count-1:     # 在数字编号之间加上\t
            parts[i] += '\t'
            i += 1
        j = 1
        while j <= MaxTabCount - i:     # 在标题之前加入足够的\t
            parts.insert(-1, '\t')
            j += 1
        newline = ''
        for part in parts:
            newline += part
        return newline
    else:
        txt = line.replace('\n', '')
        print('该行 "{}" 内容异常，无法进行处理'.format(txt))
        return ''


if __name__ == '__main__':

    try:
        with open(SourceFileName, 'r', encoding="(utf8)") as file_object:
            contents = file_object.readlines()
    except FileNotFoundError:
        print('找不到原始数据文件，无法继续处理')
        exit(-1)

    for i in range(len(contents)):
        if check_line(contents[i]):
            NewLine = contents[i]
            NewLine = cutdown(NewLine)
            NewLine = addup(NewLine)
            UsefulContents.append(NewLine)

    print('一共有 {} 行Useful Line 将被写入到新文件！'.format(str(len(UsefulContents))))

    with open(UsefulFileName, 'w', encoding="(utf8)") as file_object:
        for i in range(len(UsefulContents)):
            file_object.write(UsefulContents[i])

    print('写入操作完成，已经把 {} 行数据写入到文件 {} 中。'.format(
        str(len(UsefulContents)), UsefulFileName))
