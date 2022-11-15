#FROM ubuntu:22.04
FROM mcr.microsoft.com/dotnet/sdk:7.0-jammy

WORKDIR /home/

COPY . .

## General dev tools
RUN apt update && apt install -y --no-install-recommends \
  apt-transport-https \
  curl \
  wget \
  git \
  gnupg2 \
  jq \
  sudo \
  zsh \
  vim \
  mc \
  htop \
  dnsutils \  
  build-essential \
  ca-certificates \
  openssl

## nvm and node
SHELL ["/bin/bash", "--login", "-c"]
RUN apt update  \
  && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
#RUN nvm install 18.12.1

## Python
RUN apt update && apt install -y python3

## dotnet 7 - don't need this if using mcr dotnet image
#RUN wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
#RUN dpkg -i packages-microsoft-prod.deb
#RUN apt update && apt install -y dotnet-sdk-7.0

## Setup other software, including Rust
RUN bash ./setup.sh

ENV PATH="/root/.cargo/bin:$PATH"
