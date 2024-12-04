{pkgs}:
let 
  cmds = ''
    #!/usr/bin/env bash
    build() {
      curr_dir=$(pwd)
      cd $root


      mkdir -p $root/build
      ${pkgs.docker-buildx}/bin/docker-buildx build . \
        -f build-containers/static-build.dockerfile \
        -t tmp/static-build

      ${pkgs.docker}/bin/docker run \
        --rm \
        -v $root/build:/result \
        $@ \
        tmp/static-build

      
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
      rm .tfdocs.db || true
      rm .test.tfdocs.db || true
      rm -rf dist
      rm -rf build
    }
  '';
in
pkgs.tfdocsUtils.mkCmdRunner cmds
