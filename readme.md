# TFDocs
*Read Terraform provider documentation in the terminal*

TFDocs is a command-line tool that lets you view provider documentation from the terminal.

## Usage
### Setup
### Commands

## Installation
> ### Coming Soon: Install Script (trivial, not recommended for secure environments)
> Too busy to fuss with any of the more involved methods? Run this command in a Linux or Mac terminal to install the program:
> `curl tfdocs.crease.sh | bash`

### PipX (simple, requires Python and PipX, works for any platform)
Tfdocs is published on PyPI under the name `tfdocs-cli`. You can add Tfdocs to a project by running `pip install tfdocs-cli`. If you want to install Tfdocs system-wide in a reliable fashion, it's recommended to use *pipx* instead of `pip install -U tfdocs-cli`. You can use *pipx* like so:
```bash
pipx install tfdocs-cli
```

### Manual Installation on Linux (any distro, no requirements)
This is the current primary method of installation for different platforms. In the future, different repositories for different platforms will be provided.
1. Download the AppImage file from the 'Releases' section on GitHub
   ```
     curl https://github.com/Apollo-XIV/tfdocs/releases/latest/PLATFORM.AppImage
   ```
2. Move the executable somewhere on your PATH, typically `/usr/bin`
  ```
    mv tfdocs.AppImage /usr/local/bin
  ```
3. Start a new terminal session, or source your .<shell>rc file again
  ```
    source ~/.bashrc
  ```
