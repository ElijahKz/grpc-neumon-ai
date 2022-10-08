FROM python:3.9

RUN apt-get update \
  && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential

WORKDIR /home/src

RUN wget "https://www.dropbox.com/s/d7loj89txe1sowb/WilhemNet_86.h5?dl=0"  -o WilhemNet_86.h5


COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend/src .
COPY protos/backend.proto .
RUN mv ./WilhemNet_86.h5 /Inference/

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./backend.proto