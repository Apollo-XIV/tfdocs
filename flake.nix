{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-terraform.url = "github:stackbuilders/nixpkgs-terraform";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix, nixpkgs-terraform, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        tfdocs-utils = import ./lib.nix;
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ 
            tfdocs-utils
            nixpkgs-terraform.overlays.default 
            poetry2nix.overlays.default 
          ];
          config.allowUnfree = true;
          config.extra-substituters = "https://nixpkgs-terraform.cachix.org";
          config.extra-trusted-public-keys = "nixpkgs-terraform.cachix.org-1:8Sit092rIdAVENA3ZVeH9hzSiqI/jng6JiCrQ1Dmusw=";
        };

        pypkgs-build-requirements = {
          nh3 = [ "maturin" ];
          textual_dev = [ "setuptools" "hatchling" ];
          textual-serve = [ "hatchling" ];
          propcache = [ "cython" "setuptools" "expandvars" ];
        };

        poetry_overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend
          (final: prev: 
            builtins.mapAttrs (package: build-requirements: 
              (builtins.getAttr package prev).overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or []) ++ (builtins.map(pkg: 
                  if builtins.isString pkg then builtins.getAttr pkg prev else pkg) 
                build-requirements);
              })
          ) pypkgs-build-requirements );

        myEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          python = pkgs.python311Full;
          preferWheels = true;
        };

        terraform = nixpkgs-terraform.packages.${system}."1.9.5";

        deps =  with pkgs; [
            myEnv
            poetry
            zsh
            sqlite
            tflint
            mypy
            direnv
            commitlint
            husky
            nodejs_22
            gh
            terraform
            python311Full
            docker
            docker-buildx
            vscode-langservers-extracted
            awscli2
            checkov
            appimagekit
            checkov
            # Command Scripts Alias
            (import ./cmds.nix {inherit pkgs;})
            nodePackages.semver
          ];
      in {
        packages.default = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          overrides = poetry_overrides;
          meta.mainProgram = "tfdocs";
          # extrsa
          preferWheels = true;
        };
        # packages.default = import ./build.nix {inherit pkgs deps;};
        packages.buildDeps = pkgs.stdenv.mkDerivation {
          name = "build-deps";
          buildInputs = with pkgs; [
            python311Full
            gcc
            poetry
          ];
        };

        devShells.default = pkgs.mkShellNoCC {
          packages = deps;
          AWS_PROFILE="personal-aws";
          GLIBC_PATH=pkgs.glibc;
          ZLIB_PATH=pkgs.zlib;
        };
      }
    );
}
