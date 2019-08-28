FROM python:3.6.8
MAINTAINER Your Name "ammaralterra"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "ecommerce.py" ]
