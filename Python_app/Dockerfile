FROM python:3.12-slim-bookworm
RUN pip install --upgrade pip && \
    pip install PyQt5 && \
    pip install requests flask && \
    mkdir mypyapp
COPY myapp.py mypyapp/
WORKDIR mypyapp
EXPOSE 3000
CMD ["python", "myapp.py"]