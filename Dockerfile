FROM python:3

RUN pip install asciinema

WORKDIR /app/target
RUN mkdir /app/out

COPY dist/ /opt
COPY e2e/entrypoint.sh /app/

RUN pip install /opt/*.tar.gz

ENTRYPOINT ["/app/entrypoint.sh"]