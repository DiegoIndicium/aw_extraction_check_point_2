FROM hashicorp/terraform:latest

RUN apk add --no-cache \
    curl \
    jq \
    python3 \
    py3-pip

RUN pip3 install databricks-cli --break-system-packages

WORKDIR /workspace

COPY terraform/ /workspace/

ENTRYPOINT ["terraform"]