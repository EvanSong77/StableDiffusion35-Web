# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:45
# @Author  : codewen77
import os

from dotenv import load_dotenv

load_dotenv()

LOGGER_PATH = os.environ.get("LOGGER_PATH")
DEVICE = os.environ.get("DEVICE")
BEARER = os.environ.get("BEARER")
CONFIG_PATH = os.environ.get("CONFIG_PATH")
