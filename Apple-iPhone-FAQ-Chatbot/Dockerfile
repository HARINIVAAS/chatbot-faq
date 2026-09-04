FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir streamlit pandas scikit-learn

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
