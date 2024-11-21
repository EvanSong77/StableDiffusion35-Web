## Introduction 
官方的StableDiffusion3.5模型部署，本项目实现了并发推理。

## Quick Start
在执行代码前，你需要先下载[StableDiffusion3.5](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium)模型，并放置在`./models`目录下。

### Setup
使用pip安装依赖
```shell
pip install -r requirements.txt
```

### dokcer部署
```shell
sh image_builder.sh

docker-compose up -d
```

### 本地部署
```shell
python app.py
```

你可以将positive_prompt和negative_prompt放置在config下，模型相关配置在models.yml中。