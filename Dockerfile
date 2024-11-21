FROM pytorch:23.12-py3-nvcr
COPY . /app/
WORKDIR /app

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& yes|cp pip.conf /usr/ \
&& yes|cp pip.conf ~/.config/pip \
&& pip install --no-cache-dir -r requirements.txt