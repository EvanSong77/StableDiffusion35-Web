# -*- coding: utf-8 -*-
# @Time    : 2024/11/1 9:46
# @Author  : codewen77
import os
from os import PathLike
from typing import Dict

import torch
import yaml
from pydantic import BaseModel

from diffusers import BitsAndBytesConfig, SD3Transformer2DModel, StableDiffusion3Pipeline
from src.config.config_model import TextToImageConfig, StyleConfig
from src.config.env import DEVICE
from src.utils import logs
from src.utils.data_util import read_txt

logger = logs.logger


class ModelController(BaseModel):
    text_to_image_configs: Dict[str, TextToImageConfig]
    style_configs: Dict[str, StyleConfig]

    @classmethod
    def from_yaml(cls, path: PathLike) -> "ModelController":
        with open(path, "r", encoding='utf-8') as fp:
            config = yaml.safe_load(fp)

        # text-to-image
        negative_prompts, positive_prompts = {}, {}
        text_to_image_configs = {}
        for alias, kwargs in config.get("sd35", {}).items():
            if alias in text_to_image_configs:
                logger.error(f"Duplicate sd35 alias: {alias}")
                exit(1)
            if alias == "text-to-image":
                for file in os.listdir(kwargs["negative_prompt_path"]):
                    if file.endswith(".txt"):
                        negative_prompts[file.split('.')[0]] = read_txt(
                            os.path.join(kwargs["negative_prompt_path"], file))
                for file in os.listdir(kwargs["positive_prompt_path"]):
                    if file.endswith(".txt"):
                        positive_prompts[file.split('.')[0]] = read_txt(
                            os.path.join(kwargs["positive_prompt_path"], file))
                text_to_image_configs[alias] = TextToImageConfig(alias=alias, **kwargs)
            else:
                raise NotImplementedError(f"Unsupported sd35 type: {alias}")

        # styles
        style_configs = {}
        for alias, kwargs in config.get("prompt_style", {}).items():
            if alias in style_configs:
                logger.error(f"Duplicate prompt_style alias: {alias}")
                exit(1)
            try:
                kwargs["negative_prompt"] = negative_prompts[alias] if alias in negative_prompts else ''
                kwargs["positive_prompt"] = positive_prompts[alias] if alias in positive_prompts else ''
                style_configs[alias] = StyleConfig(alias=alias, **kwargs)
            except TypeError:
                raise NotImplementedError(f"Unsupported prompt_style type: {alias}")

        return cls(text_to_image_configs=text_to_image_configs, style_configs=style_configs)

    def get_sd35_engines(self):
        """加载文生图模型:stable-diffusion-3.5-medium"""
        model_path = self.text_to_image_configs['text-to-image'].path
        logger.info(f"load stable-diffusion-3.5-medium model from {model_path}")

        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            model_path,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16
        )
        logger.info(f'device_count:{torch.cuda.device_count()}')
        logger.info(f"use device: {DEVICE}")
        model_nf4 = model_nf4.to(f'{DEVICE}')
        pipeline = StableDiffusion3Pipeline.from_pretrained(
            model_path,
            transformer=model_nf4,
            torch_dtype=torch.bfloat16
        )
        pipeline = pipeline.to(f'{DEVICE}')
        # 采用offload方式推理
        # pipeline.enable_model_cpu_offload()
        return pipeline
