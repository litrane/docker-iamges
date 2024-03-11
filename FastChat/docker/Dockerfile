FROM nvidia/cuda:12.2.0-runtime-ubuntu20.04

COPY start_services.sh .

RUN apt-get update -y && apt-get install -y python3.9 python3.9-distutils curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
RUN pip3 install fschat
RUN pip3 install fschat[model_worker,webui] pydantic==1.10.09
RUN pip3 install vllm

EXPOSE 8000

EXPOSE 7860

EXPOSE 21001

# ENTRYPOINT ["./start_services.sh"]