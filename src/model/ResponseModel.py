# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 10:31
# @Author  : codewen77
from pydantic import BaseModel


class TextToImageResponse(BaseModel):
    id: str
    object: str
    created: int
    data: list
