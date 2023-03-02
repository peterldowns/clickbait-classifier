{
  description = "clickbait-classifier is an example text classifier";
  inputs = {
    nixpkgs.url = github:nixos/nixpkgs/nixos-unstable;

    flake-utils.url = github:numtide/flake-utils;

    flake-compat.url = github:edolstra/flake-compat;
    flake-compat.flake = false;

    nix-filter.url = github:numtide/nix-filter;

    poetry2nix.url = github:nix-community/poetry2nix;
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
    poetry2nix.inputs.flake-utils.follows = "flake-utils";
  };

  outputs = { ... }@inputs:
    inputs.flake-utils.lib.eachDefaultSystem
      (system:
        let
          overlays = [
            inputs.poetry2nix.overlay
          ];
          pkgs = import inputs.nixpkgs {
            inherit system overlays;
          };
          developerEnv = pkgs.poetry2nix.mkPoetryEnv
            {
              projectDir = ./.;
              python = pkgs.python3;
              extraPackages = (ps: [
                ps.pip
              ]);
              preferWheels = true;
            };
          packagedApp = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
            python = pkgs.python3;
            preferWheels = true;
          };
          programs.classifier = pkgs.writeShellScript "main.sh" ''
            ${packagedApp.dependencyEnv}/bin/python -m clickbait_classifier.classifier
          '';
          programs.interactive = pkgs.writeShellScript "main.sh" ''
            ${packagedApp.dependencyEnv}/bin/python -m clickbait_classifier.interactive
          '';
        in
        rec {
          packages = rec {
            clickbait-classifier = packagedApp;
            default = clickbait-classifier;
          };
          apps = rec {
            classifier = {
              type = "app";
              program = "${programs.classifier}";
            };
            interactive = {
              type = "app";
              program = "${programs.interactive}";
            };
            default = classifier;
          };
          devShells = rec {
            default = pkgs.mkShell {
              buildInputs = [
                pkgs.libxml2
                pkgs.libxslt
                pkgs.zlib
                pkgs.pkg-config
              ];
              packages = [
                pkgs.python3
                pkgs.poetry
                developerEnv
                ## other tools
                pkgs.just
                pkgs.rnix-lsp
                pkgs.nixpkgs-fmt
              ];

              shellHook = ''
                # The path to this repository
                if [ -z $WORKSPACE_ROOT ]; then
                  shell_nix=" ''${IN_LORRI_SHELL:-$(pwd)/shell.nix}"
                  workspace_root=$(dirname "$shell_nix")
                  export WORKSPACE_ROOT="$workspace_root"
                fi
                export TOOLCHAIN_ROOT="$WORKSPACE_ROOT/.toolchain"
              '';
            };
          };
        }
      );
}
