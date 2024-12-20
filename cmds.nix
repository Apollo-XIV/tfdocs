{pkgs}:
let 
  cmds = ''
		#!/usr/bin/env bash

		################
		# BUILD COMMANDS
		################

		build() {
		  pushd $root >> /dev/null

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

		  popd >> /dev/null
		}

		build-appimage() {
		  nix bundle --bundler github:ralismark/nix-appimage $root#default
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

		###############
		# TEST COMMANDS
		###############    

		py-test() {
		  python <<-EOF
				from tfdocs.db.test_handler import MockDb
				MockDb.delete()
			EOF
		  mypy tfdocs
		}


		py-test-cov() {
		  python <<-EOF
				from tfdocs.db.test_handler import MockDb
				MockDb.delete()
			EOF
			status=0
			{
			  mypy tfdocs
			} || status=1
			{
			  pytest --cov-report term:skip-covered --cov=tfdocs --no-cov-on-fail
			} || status=1

		  echo CLEANUP
		  python <<-EOF
				from tfdocs.db.test_handler import MockDb
				MockDb.delete()
			EOF
			exit $status
		}

		py-test-cov-full() {
		  python <<-EOF
				from tfdocs.db.test_handler import MockDb
				MockDb.delete()
			EOF
			status=0
			{
			  mypy tfdocs
			} || status=1
			{
			  pytest --cov-report term-missing --cov=tfdocs --cov-fail-under=80
			} || status=1
		  echo CLEANUP
		  python <<-EOF
				from tfdocs.db.test_handler import MockDb
				MockDb.delete()
			EOF
			exit $status
		}

		py-test-int() {
		  mypy tfdocs
		  pytest --cov-report html --cov=tfdocs
		  xdg-open htmlcov/index.html
		}

		###############
		# LINTING COMMANDS
		###############    

		lint() {
		  py-lint
		  tf-lint 
		}

		py-lint() {
		  black --check .
		}

		tf-lint() {
		  tflint || true
		}

		lint-fix() {
		  py-lint-fix
		}

		py-lint-fix() {
		  black .
		}

		###############
		# UTILITY COMMANDS
		###############    

		repeat() {
		  cmd="$1"
		  cmd="''${cmd:-echo}"

		  trap 'echo "Exiting..."; exit' INT # Clean exit on Ctrl+C

		  while true; do
		    bash -c "$cmd"
		    read -p "Press Enter to run '$cmd' again..." choice
		    [[ "$choice" == "q" ]] && break
		  done
		}

		update-env() {
		  env="$1"
		  env="''${env:-dev}"
		  cd envs
		  echo "> initialising terraform"
		  terraform init >> /dev/null
		  echo "> syncing backend and environment-based inputs"
		  terraform apply --auto-approve -var ENV=$env >> /dev/null
		  echo "> backend updated successfully"
		}

		refmt() {
			local in; read in;
			# takes STDIN json input and outputs it via STDOUT formatted
			python3 - <<-EOF
				import json
				import sys
				raw = json.loads("''${in}")
				fmt_json = json.dumps(raw, indent = 2)
				sys.stdout.write(f"{fmt_json}\n")
			EOF
		}

		watchlog() {
			python3 - <<-EOF
				from tfdocs.logging.watch_logs import main
				main()
			EOF
		}

		website() {
			python3 -m web
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
