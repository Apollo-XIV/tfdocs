# TFDocs
*Read Terraform provider documentation in the terminal*

TFDocs is a command-line tool that lets you view provider documentation from the terminal.

## Installation
> ### Coming Soon: Install Script (trivial, not recommended for secure environments)
> Too busy to fuss with any of the more involved methods? Run this command in a Linux or Mac terminal to install the program:
> `curl tfdocs.crease.sh | bash`

### PipX (simple, requires Python and PipX)
Tfdocs is published on PyPI under the name `tfdocs-cli`. You can add Tfdocs to a project by running `pip install tfdocs-cli`. If you want to install Tfdocs system-wide in a reliable fashion, it's recommended to use *pipx* instead of `pip install -U tfdocs-cli`. You can use *pipx* like so:
```bash
pipx install tfdocs-cli
```

### Manual Installation (no requirements)
This is the current primary method of installation for different platforms. In the future, different repositories for different platforms will be provided.
1. Download the relevant binary from the 'Releases' section on GitHub
   ```
     curl https://github.com/Apollo-XIV/tfdocs/releases/latest/PLATFORM 
   ```
2. 

\*The NUR is the Nix-User-Repository
