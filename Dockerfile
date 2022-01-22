FROM python:3.10.2-buster

LABEL version="2021.1" maintainer="petr.cezner@factorio.cz"

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update -y && apt-get install tesseract-ocr -y && apt-get install tesseract-ocr-all -y
RUN pip install -r requirements.txt

COPY document_reader/. /app/document_reader

ENTRYPOINT [ "streamlit", "run" ]
EXPOSE 8501
CMD [ "document_reader/streamlit_app.py"]
