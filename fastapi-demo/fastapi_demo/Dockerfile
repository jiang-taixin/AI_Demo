# 使用官方的 Python 运行时作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制应用程序的依赖文件到工作目录
COPY requirements.txt .

# 安装应用程序的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码到工作目录
COPY . .

# 声明 FastAPI 应用程序的端口
EXPOSE 8000

# 启动 FastAPI 应用程序
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]