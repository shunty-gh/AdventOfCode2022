##
# From https://github.com/codespaces-examples/base/blob/main/.devcontainer/setup.sh
##

## add bits needed for GitHub CLI
apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
apt-add-repository https://cli.github.com/packages
apt-get update
apt-get install -y gh

##
# From https://github.com/codespaces-examples/rust/blob/main/.devcontainer/setup.sh
##

## Rust
## Install rustup and common components
curl https://sh.rustup.rs -sSf | sh -s -- -y 
rustup install nightly
rustup component add rustfmt
rustup component add rustfmt --toolchain nightly
rustup component add clippy 
rustup component add clippy --toolchain nightly

cargo install cargo-expand
cargo install cargo-edit

##
# From https://github.com/codespaces-examples/dotnetcore/blob/main/.devcontainer/setup.sh
## 

## Install nvm
#curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash

## Install Docker CE
#curl -fsSL https://get.docker.com | bash

## Update to the latest PowerShell
curl -sSL https://raw.githubusercontent.com/PowerShell/PowerShell/master/tools/install-powershell.sh | bash

## Install Azure Functions Core Tools v3
#wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
#dpkg -i packages-microsoft-prod.deb
#apt-get update
#apt-get install azure-functions-core-tools-3

## Enable local HTTPS for .NET Core
dotnet dev-certs https --trust

## Setup and install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
cp -R /root/.oh-my-zsh /home/$USERNAME
cp /root/.zshrc /home/$USERNAME
sed -i -e "s/\/root\/.oh-my-zsh/\/home\/$USERNAME\/.oh-my-zsh/g" /home/$USERNAME/.zshrc
chown -R $USER_UID:$USER_GID /home/$USERNAME/.oh-my-zsh /home/$USERNAME/.zshrc