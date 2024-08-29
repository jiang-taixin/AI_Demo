# 使用Python官方镜像作为基础镜像
FROM python:3.12
 
# 设置工作目录
WORKDIR /app
 
# 复制当前目录下的内容到容器的/app目录
COPY . /app
 
# 安装FastAPI和依赖
RUN pip install --no-cache-dir fastapi uvicorn gunicorn
 
# 暴露端口
EXPOSE 80
 
# 定义环境变量
ENV PORT=80
 
# 运行Gunicorn服务器，使用4个工作进程，绑定端口到PORT环境变量
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "main:app", "--workers", "4"]
