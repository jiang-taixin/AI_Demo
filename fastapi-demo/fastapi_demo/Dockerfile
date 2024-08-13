FROM python:3.12

WORKDIR fastapi_demo

COPY ./requirements.txt /fastapi_demo/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi_demo/requirements.txt
COPY ./example /fastapi_demo/example
COPY ./ORM_Example /fastapi_demo/ORM_Example

CMD ["python", "main.py"]