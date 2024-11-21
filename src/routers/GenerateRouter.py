# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:49
# @Author  : codewen77
import asyncio
import base64
import os
import time
from io import BytesIO

import torch
from fastapi import APIRouter

from diffusers import StableDiffusion3Pipeline
from src.config.gbl import MODEL_CONTROLLER
from src.model.RequestModel import TextToImageRequest
from src.model.ResponseModel import TextToImageResponse
from src.utils import logs

generate_router = APIRouter()
logger = logs.logger
text_to_image_configs = MODEL_CONTROLLER.text_to_image_configs['text-to-image']
style_configs = MODEL_CONTROLLER.style_configs
engines = MODEL_CONTROLLER.get_sd35_engines()


@generate_router.post("/words_to_imgs", response_model=TextToImageResponse)
async def text2img_proc(request: TextToImageRequest):
    """文生图"""
    cur_time = int(time.time())
    try:
        promptEnglish = request.promptEnglish
        style = request.style if request.style else "natural"
        style_config = style_configs[style]
        positive_prompt = style_config.positive_prompt.format(promptEnglish)
        logger.info(f"positive_prompt: {positive_prompt}")

        if request.size:
            width = int(request.size.split("x")[0])
            height = int(request.size.split("x")[1])
        else:
            width = style_config.width
            height = style_config.height
        with torch.no_grad():
            loop = asyncio.get_event_loop()
            scheduler = engines.scheduler.from_config(engines.scheduler.config)
            pipeline = StableDiffusion3Pipeline.from_pipe(engines, scheduler=scheduler)
            image = await loop.run_in_executor(None, lambda: pipeline(
                prompt=positive_prompt,
                width=width,
                height=height,
                negative_prompt=style_config.negative_prompt,
                num_inference_steps=text_to_image_configs.num_inference_steps,
                guidance_scale=text_to_image_configs.guidance_scale,
                max_sequence_length=text_to_image_configs.max_sequence_length,
            ))
            image = image.images[0]
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            # 释放显存
            torch.cuda.empty_cache()
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            if not os.path.exists(text_to_image_configs.save_path):
                os.makedirs(text_to_image_configs.save_path)

            file_path = os.path.join(text_to_image_configs.save_path, str(cur_time) + '.png')
            with open(file_path, "wb") as f:
                f.write(buffered.getvalue())
            logger.info(f"{file_path}保存成功...")

            response_data = TextToImageResponse(id="", object="image", created=cur_time,
                                                data=[{"b64_image": img_str, "index": 0, "object": "Image"}])
            return response_data
    except Exception as e:
        response_data = TextToImageResponse(id="", object="image", created=cur_time,
                                            data=[{"b64_image": "", "index": 0, "object": "Image"}])
        logger.error(f"Error in text2img_proc: {str(e)}")
        return response_data
