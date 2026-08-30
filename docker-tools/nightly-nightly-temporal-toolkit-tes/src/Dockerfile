FROM ubuntu:22.04

LABEL maintainer="ApocalypsAI Nightly Integrator"
LABEL description="A containerized development environment with essential CLI tools for rapid deployment and temporal anomaly response."

ENV DEBIAN_FRONTEND=noninteractive

# Install core utilities and Python for pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    jq \
    vim \
    tmux \
    htop \
    net-tools \
    iputils-ping \
    python3 \
    python3-pip \
    software-properties-common \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install yq (using pip for simplicity)
RUN pip3 install yq

# Install Ansible
RUN pip3 install ansible-core

# Install Terraform
# Add HashiCorp GPG key and repository
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list

# Install Terraform
RUN apt-get update && apt-get install -y terraform

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

WORKDIR /app

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
