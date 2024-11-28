FROM python:3.13

WORKDIR /app

COPY . /app/

RUN python3.13 -m venv prompt_analysis
CMD source prompt_analysis/bin/actiavte
RUN pip install -r /app/requirements.txt


CMD [ "python", "/app/run.py"]

EXPOSE 8000