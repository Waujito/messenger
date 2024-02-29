FROM python:3.11-alpine as bulid

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

RUN pip install waitress

RUN mkdir /prj
COPY --from=bulid /prj/* /prj/

RUN pip install /prj/$(ls /prj)

ENTRYPOINT [ "waitress-serve",  "--call", "flaskr:create_app" ]