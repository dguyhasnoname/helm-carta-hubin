FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /
RUN pip3 install --no-cache --upgrade -r requirements.txt

# Install helm (latest release)
ENV HELM_VERSION=3.1.2
ENV BASE_URL="https://storage.googleapis.com/kubernetes-helm"
ENV BASE_URL="https://get.helm.sh"
ENV TAR_FILE="helm-v${HELM_VERSION}-linux-amd64.tar.gz"
RUN apt-get update && apt-get install -y --no-install-recommends curl  && \
    curl -L ${BASE_URL}/${TAR_FILE} |tar xvz && \
    mv linux-amd64/helm /usr/bin/helm && \
    chmod +x /usr/bin/helm && \
    rm -rf linux-amd64 

COPY ./ /app
WORKDIR /app/carta-hubin

CMD ["/app/carta-hubin/hubin.py"]
ENTRYPOINT ["python"]