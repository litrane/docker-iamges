# Diffusion Model

This repository utilizes [stable-diffusion-webui-docker](https://github.com/aoirint/stable-diffusion-webui-docker) to build Docker images for running a diffusion model.

## Usage

### Setting Up Persistent Directories

Create permanent directories with user and group IDs set to 1000:

```bash
mkdir -p ./data ./log ./cache/huggingface
sudo chown -R 1000:1000 ./data ./log ./cache
```

### Running the Docker Container

To run the Docker container with GPU support:

```bash
sudo docker run --gpus all --rm -it \
    -v "./data:/data" \
    -v "./log:/code/stable-diffusion-webui/log" \
    -v "./cache/huggingface:/home/user/.cache/huggingface" \
    -p "127.0.0.1:7860:7860/tcp" \
    aoirint/sd_webui --enable-insecure-extension-access --api
```

#### Web UI

Access the web interface by navigating to [http://localhost:7860/](http://localhost:7860/). API documentation is available at [http://localhost:7860/docs](http://localhost:7860/docs).

#### API

Use `chat_test.py` to interact with the API and generate text-to-image results.

### Kubernetes Deployment

For deploying on Kubernetes, the YAML configuration is provided below:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sd-webui-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sd-webui
  template:
    metadata:
      labels:
        app: sd-webui
    spec:
      containers:
      - name: sd-webui
        image: aoirint/sd_webui
        args: ["--enable-insecure-extension-access", "--api"]
        resources:
          limits:
            nvidia.com/gpu: 1
        ports:
        - containerPort: 7860
```

Note: Kubernetes does not support GPU resources by default. You must have a GPU device plugin installed in your cluster.

# Large Language Model (LLM)

We build Docker images for the Large Language Model using [serge](https://github.com/serge-chat/serge).

## Usage

Run the Docker container as follows:

```bash
docker run -d \
    --name serge \
    -v weights:/usr/src/app/weights \
    -v datadb:/data/db/ \
    -p 8008:8008 \
    ghcr.io/serge-chat/serge:latest
```

#### Web UI

The web interface can be accessed at [http://localhost:8008/](http://localhost:8008/). API documentation can be found at [http://localhost:8008/api/docs](http://localhost:8008/api/docs).

#### API

Retrieve the chat ID with the following command:

```bash
curl -X 'GET' \
  'http://localhost:8008/api/chat/' \
  -H 'accept: application/json'
```

Then, utilize the chat ID with `chat_test.py` to send messages via the API.

### Kubernetes Deployment

For Kubernetes, the YAML configuration is as follows:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: serge-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: serge
  template:
    metadata:
      labels:
        app: serge
    spec:
      containers:
        - name: serge
          image: ghcr.io/serge-chat/serge:latest
          ports:
            - containerPort: 8008
```

# FastChat

FastChat is an open platform designed for training, serving, and evaluating large language model-based chatbots. It has successfully served over 6 million chat requests for more than 50 LLMs. FastChat features both a `gradio_web_server` and an `openai_api_server`.

## Usage

### 1. Create Docker Images

To build the Docker image, run the following command at FastChat/docker/:

```bash
docker build -f Dockerfile -t fastchat .
```

### 2. Run the Docker Container

Execute the Docker container with the following command:

```bash
docker run -it --gpus all -p 8000:8000 -p 7860:7860 -p 21001:21001 -v /root/.cache/huggingface/hub/:/root/.cache/huggingface/hub/ fastchat /bin/bash
```

### 3. Run the FastChat Server

First, log into the container:

```bash
docker exec -it fastchat /bin/bash
```

Then, start the server by running the following commands:

```bash
python3.9 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5
python3.9 -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8000
python3.9 -m fastchat.serve.controller --host 127.0.0.1 --port 21001
python3.9 -m fastchat.serve.gradio_web_server --host 127.0.0.1 --port 7860
```

If you encounter an error with `python3.9 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5`, try the alternative command:

```bash
python3.9 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5 --host 127.0.0.1 --port 21002
```

### Using VLLM

To use VLLM, replace the `model_worker` command with:

```bash
python3.9 -m fastchat.serve.vllm_worker --model-path lmsys/fastchat-t5-3b-v1.0
```

### Potential Issues

FastChat may fail on machines with a GPU such as the Tesla T4 or if there is insufficient memory.

## To-Do

- Package into Kubernetes Docker images.
- Modify the Dockerfile accordingly.
