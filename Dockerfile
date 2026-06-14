FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建临时目录
RUN mkdir -p /tmp/subtitles_uploads /tmp/subtitles_output

# 暴露端口
EXPOSE 5000

# 环境变量
ENV PORT=5000

# 启动 Web 服务
CMD ["python", "web.py"]