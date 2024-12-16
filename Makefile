run:
	streamlit run Home.py

docker_run:
	docker build -t rnadvisor_interface .
	docker run -it -p 8501:8501 -v ${PWD}/src_st:/app/src_st rnadvisor_interface