FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN python -m pip install --upgrade pipenv wheel pytest
RUN pipenv install -e .

CMD [ "python", "-m", "hexagon" ]