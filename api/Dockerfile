FROM condaforge/mambaforge as env
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y 


FROM env as build

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install build
COPY requirements.txt .
COPY pyproject.toml .

COPY flaskr flaskr

RUN python -m build --wheel

RUN mkdir /prj

RUN cp dist/$(ls dist | head -1) /prj/



FROM python:3.11-alpine as prod

# RUN pip install pyuwsgi
RUN apk update && apk add gcc openssl openssl-dev python3-dev build-base linux-headers pcre-dev

RUN CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" \
  UWSGI_PROFILE_OVERRIDE=ssl=true pip3 install uwsgi -Iv

RUN mkdir /prj
COPY --from=build /prj/* /prj/

RUN pip install /prj/$(ls /prj)

COPY uwsgi.ini .

ENTRYPOINT [ "uwsgi", "uwsgi.ini"]




FROM env as dev
RUN conda create -n cenv python=3.11

COPY requirements.txt .
RUN conda run --no-capture-output -n cenv pip install -Ur requirements.txt