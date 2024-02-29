FROM python:3.11-alpine as bulid

COPY flaskr flaskr
COPY requirements.txt .
COPY pyproject.toml .

# RUN pip install -r requirements.txt

RUN pip install build
RUN python -m build --wheel

RUN mkdir /prj

RUN cp dist/$(ls dist | head -1) /prj/
RUN ls /prj && sleep 2

FROM python:3.11-alpine as prod

RUN pip install waitress

RUN mkdir /prj
COPY --from=bulid /prj/* /prj/

RUN pip install /prj/$(ls /prj)

ENTRYPOINT [ "waitress-serve",  "--call", "messenger_api:create_app" ]