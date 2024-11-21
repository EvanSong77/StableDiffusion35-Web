# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:45
# @Author  : codewen77
from src.config.env import CONFIG_PATH
from src.controller import ModelController

MODEL_CONTROLLER = ModelController.from_yaml(CONFIG_PATH)