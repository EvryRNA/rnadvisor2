FROM sayby77/rnadvisor
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/EvryRNA/rnadvisor.git lib/rnadvisor
RUN mv lib/rnadvisor/src src
COPY . .
RUN python3 -m tests.test_tf # To download the model weights for TB-MCQ
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.baseUrlPath=/RNAdvisor"]
