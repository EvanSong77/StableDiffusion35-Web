# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:54
# @Author  : codewen77
from pydantic import BaseModel


class BaseConfig(BaseModel):
    alias: str


class LLMConfig(BaseConfig):
    path: str


class TextToImageConfig(LLMConfig):
    path: str
    name: str
    num_inference_steps: int
    guidance_scale: float
    max_sequence_length: int
    save_path: str


class StyleConfig(BaseConfig):
    name: str
    width: int
    height: int
    negative_prompt: dict
    positive_prompt: dict
