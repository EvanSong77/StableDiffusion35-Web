# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 10:05
# @Author  : codewen77


def read_txt(file_path):
    with open(file_path, "r", encoding='utf-8') as fp:
        return '\n'.join(fp.readlines())
