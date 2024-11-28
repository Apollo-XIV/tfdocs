{pkgs}:
let 
  cmds = ''
    build() {
      curr_dir=$(pwd)
      cd $root
      nix build
      mkdir -p $root/build
      sudo cp -rL $root/result/* $root/build
      sudo chown -R $(whoami) $root/build
      cd $curr_dir
    }

    test-build() {
      PLATFORM="''${1:-"ubuntu"}"
      DOCKERFILE="build-containers/$PLATFORM.dockerfile"
      TAGNAME="tfdocs:$PLATFORM"

      build # run the build command first

      docker build \
      -f $DOCKERFILE \
      -t $TAGNAME \
      --build-arg BASE_IMAGE="$PLATFORM:latest" \
      $root
      docker run -it $TAGNAME
    }

    # Example function for testing
    test() {
      echo "Running test task..."
      # Add your test commands here
    }

    # Example function for cleaning
    clean() {
      echo "Running clean task..."
      # Add your clean-up commands here
    }
  '';
in
pkgs.writeShellScriptBin "run" ''
  #!/usr/bin/env bash
  set -e

  ${cmds}

  root=$(git rev-parse --show-toplevel)
  # Parse the first argument as the function name
  command="$1"
  shift # Remove the first argument to pass the rest to the function

  # Check if the function exists and call it
  if declare -f "$command" > /dev/null; then
    "$command" "$@"
  else
    echo "Error: '$command' is not a valid command."
    echo "Available commands: build, test, clean"
    exit 1
  fi
''
