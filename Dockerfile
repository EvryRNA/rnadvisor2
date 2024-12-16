FROM sayby77/rnadvisor
WORKDIR /app
RUN pip install streamlit streamlit_molstar plotly
RUN git clone https://github.com/EvryRNA/rnadvisor.git --branch dev_interface lib/rnadvisor
RUN mv lib/rnadvisor/src src
EXPOSE 8501
COPY . .
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]