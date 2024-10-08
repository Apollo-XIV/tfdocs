# Interface Design
---
A key part of the user experience is the layout of the sub-commands and their options. A command that is overly-verbose or clunky isn't going to be comfortable to use, and developers (the target user) won't look to it as a tool for daily use.

```
tfman <sub-command> [options]
```
## Sub-commands & Options
These are all the sub-commands and options for the tool, with the main command itself being called `tfdocs`.
### `init`
Configures the tool for use if being run for the first time, and then loads any Terraform schemas from the local directory into the database. 
#### Options
- `--offline` Don't try to get extra information from the Terraform registry or the API.
- `--help` Show the help page for the sub-command.
### `[provider]`
The default command of the tool, this sub-command will try to load the manual page for the given provider. 
#### Options
- `--update` Update the list of providers in the database before opening the manual page.
- `-v | -vv` Verbosity
- `--serve-logs` whether to send logs to udp socket
### `watch-logs`
Creates a logging collection server that the main command and tests can use to send logs to. 
### `help`
Show the help page for the command

### `report`
Allows the user to submit a bug report

### `prune`
Empty the database for the tool
