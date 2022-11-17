#FROM mcr.microsoft.com/dotnet/sdk:7.0-jammy

# This image sets the user as 'vscode' and uses mcr.microsoft.com/dotnet/sdk:7.0-bullseye-slim
# along with a .devcontainer configuration. See https://github.com/devcontainers/images/tree/main/src/dotnet
FROM mcr.microsoft.com/devcontainers/dotnet:0-7.0-jammy

COPY ./.bash_aliases /root/.bash_aliases
COPY ./.bash_aliases $HOME/.bash_aliases

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
  ripgrep \
  fd-find \
  dnsutils \
  build-essential \
  ca-certificates \
  openssl

## nvm is installed in the base image
# node LTS is setup in the devcontainer.json file

## Python
RUN apt update && apt install -y python3

## Setup other software, including Rust - all done in the devcontainer.json file
# if using a tool that doesn't support devcontainers then you can use the devcontainer CLI
# at https://github.com/devcontainers/cli
# Install it using
#    $> npm install -g @devcontainers/cli
# From the project root directory run
#    $> devcontainer up --workspace-folder .