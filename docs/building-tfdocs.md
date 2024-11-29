# Building TFDocs
## Evaluating Build Tools
Python is a notoriously hard language to distribute, but over it's many years in use a few stand-out solutions have emerged:
- PyInstaller
- Shiv
- PyOxidizer

### PyInstaller
PyInstaller is a mature and widely used tool for packaging Python programs into standalone executables. It works by analyzing your Python application and bundling all necessary modules, libraries, and a Python interpreter into a single package. PyInstaller supports a variety of platforms, including Windows, macOS, and Linux, and is known for its robustness and ease of use.

The primary advantage of PyInstaller is its ability to work seamlessly with standard Python environments without requiring significant changes to your code or project structure. However, the resulting executable isn't as portable as PyOxidizer's static binary; PyInstaller bundles the Python interpreter as a dependency, so the output may include multiple files, depending on the configuration.

Key considerations for PyInstaller include:

+ Mature tool with an established reputation
+ Strong cross-platform support
+ Large and active community for support and troubleshooting
+ Relatively simple configuration and workflow
+ Produces executables that retain the same functionality as the original Python script 
but,
- Resultant executables may include several files unless explicitly bundled into a single file
- Not as fast or modern compared to newer tools like PyOxidizer
- Can lead to large executables due to bundled dependencies
- Requires Python on the host system for building, though not for running the packaged executable
- May require additional troubleshooting for certain Python packages, particularly those using C extensions

### Shiv
Shiv is a less conventional packaging tool that creates zipapp-based executables for Python applications. These executables contain all dependencies but rely on the presence of a Python interpreter on the target system to run. Shiv's approach offers a lightweight and flexible alternative to tools like PyInstaller or PyOxidizer.

One of Shiv's standout features is its support for hermetic builds, which allow you to create highly controlled Python environments for your applications. However, because it doesn't produce true standalone binaries, it may not be the best choice if portability to systems without Python is a requirement.

Key considerations for Shiv include:

+ Lightweight and minimalistic packaging
+ Hermetic builds ensure consistent environments
+ Suitable for applications deployed in Python-rich environments, such as servers or developer tools
+ Flexible and integrates well with other Python packaging tools
+ Simple and Pythonic configuration but,

- Requires Python on the target system to execute
- Not suitable for truly standalone deployment scenarios
- Relatively niche and less widely adopted than PyInstaller or PyOxidizer
- Outputs aren't as user-friendly for non-developers due to reliance on an existing Python runtime
- Limited to environments where zipapp executables are practical

### PyOxidizer
This is a relatively new python build-tool that was created with the specific intention of simplifying the build process. The impressive part of PyOxidizer is that it produces a static binary, meaning no external dependencies whatsoever are required. This makes the resultant program incredibly portable. 

The downside to this is that the final interpreter is written in rust, but all testing is done with the CPython backend. While in theory the final binaries should be identical in functionality, the reality is that divergence is possible and would not be caught by testing. A solution to this could be building a version of the binary with a self-testing command built in, which could then be ran in a CI pipeline to catch any potential differences. But again, if we're being realistic, I can probably leave this out in the early stages and implement it later as an added layer of security.Plus, the portability of the binary means I don't have to test on each and every platform (though I still may do for major releases).

Nevertheless, with these considerations in mind, PyOxidizer has some very compelling bonuses that make it a likely candidate:
+ Static Binary compilation
+ End-users don't even need python installed
+ Fast and Modern
+ Relatively easy distribution to Windows targets
+ Thorough Documentation
but,
- Too new to have an established history and reputation
- Uses a python dialect called *Starlark* for build definitions
- No package on my distro/package-manager of choice[1]

### Conclusion
In conclusion, while PyOxidizer is an impressive project with promising capabilities, it's relatively new status and added complexity makes it a bad fit for this project in this stage.

## Using PyInstaller
PyInstaller is distributed as a Python library, and is listed as a dev dependency in poetry. A basic configuration file is created using the command below:
```
  poetry run pyinstaller --name tfdocs tfdocs/__main__.py
```
The final build command for the binary can be run as follows:
```
  poetry run pyinstaller tfdocs.spec
```
however, I prefer using the alias provided in the nix environment. If running with nix enabled you can simply execute:
```
  run pyinstaller-build
```
or, full the fully deterministic build experience[2]:
```
  nix build
```

On that note, I highly recommend installing nix if trying to build this project from scratch, as it'll allow you to avoid a lot of dependency fetching. Or, you can just download the prebuilt binary from GitHub.

## Nix
The environment management tool I'm using (nix with `poetry2nix`) makes building the project for other nix systems trivial. Very simply, a user can add the flake as an import to theirs and then reference the default package.

[1]: While this may sound ironic upon first read, in its defence I do use a rather niche linux distribution so I'm not shocked to see it missing. All this means is that I'd have to package it myself, but it's a skill I've been learning anyways.

[2]: Only a very small group of nerds - myself included - will think this is cool, and even less will think it's important.
