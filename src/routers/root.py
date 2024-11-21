# -*- coding: utf-8 -*-
# @Time    : 2024/11/8 14:28
# @Author  : codewen77
from fastapi import APIRouter

root_router = APIRouter(tags=["root"])


@root_router.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to StableDiffusion35 Server!"}
