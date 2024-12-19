final: prev:
let 
  attrsToBashFns = i: if builtins.isAttrs i then
    builtins.concatStringsSep "\n" (
      builtins.mapAttrsToList (name: value: "function ${name}() { ${value} }") i
    )
    else
    i;

  mkCmdRunner = cmds:
    let fmtCmds = attrsToBashFns cmds; in
    prev.writeShellScriptBin "run" ''
      #!/usr/bin/env bash
      set -e

      ${fmtCmds}

      root=$(git rev-parse --show-toplevel || pwd)
      # Parse the first argument as the function name
      command="$1"
      shift # Remove the first argument to pass the rest to the function

      # Check if the function exists and call it
      if declare -f "$command" > /dev/null; then
        "$command" "$@"
      else
        echo "Error: '$command' is not a valid command."
        # echo "Available commands: build, test, clean"
        exit 1
      fi
    '';
in
{
  tfdocsUtils = {
    inherit mkCmdRunner;
  };
}
