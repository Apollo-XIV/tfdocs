{pkgs}:
let 
  cmds = ''
    #!/usr/bin/env bash
    build() {
      curr_dir=$(pwd)
      cd $root
      nix build
      mkdir -p $root/build
      sudo cp -rL $root/result/* $root/build
      sudo chown -R $(whoami) $root/build
      cd $curr_dir
    }

    pyinstaller-build() {
      pyinstaller \
      --noconfirm \
      $root/tfdocs.spec
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
pkgs.tfdocsUtils.mkCmdRunner cmds
