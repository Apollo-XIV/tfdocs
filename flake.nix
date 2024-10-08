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
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ nixpkgs-terraform.overlays.default poetry2nix.overlays.default ];
          config.allowUnfree = true;
          config.extra-substituters = "https://nixpkgs-terraform.cachix.org";
          config.extra-trusted-public-keys = "nixpkgs-terraform.cachix.org-1:8Sit092rIdAVENA3ZVeH9hzSiqI/jng6JiCrQ1Dmusw=";
        };

        myEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
        };

        terraform = nixpkgs-terraform.packages.${system}."1.9.5";
        python = pkgs.stdenv.mkDerivation rec {
          pname = "python";
          version = "3.13.0";
          src = pkgs.fetchurl {
            url = "https://www.python.org/downloads/release/python-3130/";
            sha256 = "sha256-UX/MHzWnD5BOoIEmaZ9YvUEzCQg2oqKTkS426C2N2A8=";
          };
          dontUnpack = true;
          nativeBuildInputs = pkgs.lib.optionals (!pkgs.stdenv.isDarwin) [
            pkgs.autoPatchelfHook
          ];
          sourceRoot = ".";
          installPhase = ''
            runHook preInstall
            install -m755 -D ${src} $out/bin/python
            runHook postInstall
          '';
        };
      in {
        packages.default = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };

        devShells.default = pkgs.mkShellNoCC {
          packages = with pkgs; [
            myEnv
            just
            poetry
            zsh
            tflint
            mypy
            direnv
            commitlint
            husky
            nodejs_22
            terraform
            python
          ];
        };
      }
    );
}
