# Building TFDocs
## Evaluating Build Tools
Python is a notoriously hard language to distribute, but over it's many years in use a few stand-out solutions have emerged:
- PyInstaller
- Setuptools
- PyOxidizer
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

## Nix
The environment management tool I'm using (nix with `poetry2nix`) makes building the project for other nix systems trivial. Very simply, a user can add the flake as an import to theirs and then reference the default package.

[1]: While this may sound ironic upon first read, in its defence I do use a rather niche linux distribution so I'm not shocked to see it missing. All this means is that I'd have to package it myself, but it's a skill I've been learning anyways.
