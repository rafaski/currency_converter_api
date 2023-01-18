#
FROM python:3.10

#
WORKDIR /code

#
COPY requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./currency_converter_api /code/currency_converter_api

#
CMD ["uvicorn", "currency_converter_api.main:app", "--host", "127.0.0.1", "--port", "8080"]