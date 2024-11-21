# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:44
# @Author  : codewen77
from fastapi import APIRouter

from src.routers.GenerateRouter import generate_router
from src.routers.root import root_router

v1_router = APIRouter(prefix="/api", tags=["sd35"])
v1_router.include_router(generate_router, tags=["生成图片"])

__all__ = ["v1_router", "root_router"]
