# TFDocs
*Read Terraform provider documentation in the terminal*

TFDocs is a command-line tool that lets you view provider documentation from the terminal.

## Usage
### Setup
Before you can view any documentation, you need to initialise the cache. First, navigate to a directory with terraform initialised and run the following command:
```
  tfdocs init
```
This will create a cache file called `.tfdocs.db` in the directory that the command was run. When TFDocs runs, it searches for a cache in the local directory. If you want to run tfdocs from another directory you can move the cache in the filesystem.
<!-- If you want to run tfdocs from another directory you can either pass the -c flag, or you can move the cache in the filesystem. -->

### Commands
- `tfdocs`: Top-level entrypoint for the interface. Running this command will open the graphical view of the program
  - `init`: Sub-command that must be run at least once in a working directory in order to generate the local cache
  <!-- - `<provider-name>`: Opens the graphical view directly to the specified provider -->

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
