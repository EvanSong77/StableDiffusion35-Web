# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 10:16
# @Author  : codewen77
from typing import Optional

from pydantic import BaseModel


class TextToImageRequest(BaseModel):
    prompt: Optional[str] = None
    promptEnglish: str
    negative_prompt: Optional[str] = None
    negativePromptEnglish: Optional[str] = None
    style: str
    size: str
    n: int
    steps: int
    sampler_index: str
