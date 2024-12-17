# RNAdvisor2 

This repository is the source code for RNAdvisor2: web interface of RNAdvisor. 


## Installation

To run this code, you need to use docker with:

```bash
docker build -t rnadvisor_interface
docker run -it -p 8501:8501 -v ${PWD}/data:/app/data rnadvisor_interface
```

You can also directly run the code using the docker image from dockerhub: 
```bash
docker run -it -p 8501:8501 -v ${PWD}/data:/app/data sayby77/rnadvisor_interface
```