{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
    nixpkgs-terraform.url = "github:stackbuilders/nixpkgs-terraform";
    # pre-commit-hooks.url = "github:cachix/git-hooks.nix";
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
      in {
        packages.default = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };

        devShells.default = pkgs.mkShellNoCC {
          packages = [
            myEnv
            pkgs.just
            pkgs.poetry
            pkgs.zsh
            pkgs.tflint
            pkgs.mypy
            pkgs.direnv
            pkgs.commitlint
            pkgs.husky
            pkgs.nodejs_22
            terraform
          ];
        };
      }
    );
}
#
