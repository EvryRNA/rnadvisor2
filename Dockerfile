FROM sayby77/rnadvisor
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/EvryRNA/rnadvisor.git lib/rnadvisor
RUN mv lib/rnadvisor/src src
COPY tests/test_tf.py tests/test_tf.py
RUN python3 tests/test_tf.py # To download the model weights for TB-MCQ
EXPOSE 8501
COPY . .
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.baseUrlPath=/RNAdvisor"]
