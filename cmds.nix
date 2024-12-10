{pkgs}:
let 
  cmds = ''
    #!/usr/bin/env bash
    build() {
      pushd $root

      platform="''${1:-"debian"}"

      mkdir -p $root/build
      ${pkgs.docker-buildx}/bin/docker-buildx build . \
        -f build-containers/$platform-build.dockerfile \
        -t tmp/$platform-build

      ${pkgs.docker}/bin/docker run \
        --rm \
        -v $root/build:/result \
        tmp/$platform-build \
        sh -c "set -e; cp dist/tfdocs /result/tfdocs-$platform"

      popd
    }

    test-build() {
      PLATFORM="''${1:-"ubuntu"}"
      DOCKERFILE="build-containers/$PLATFORM.dockerfile"
      TAGNAME="tfdocs:$PLATFORM"

      build # run the build command first

      # add bin to container
      mkdir -p build-containers/executable
      cp build/bin/tfdocs build-containers/executable

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
      rm .tfdocs.db || true
      rm .test.tfdocs.db || true
      rm -rf dist
      rm -rf build
    }
  '';
in
pkgs.tfdocsUtils.mkCmdRunner cmds
