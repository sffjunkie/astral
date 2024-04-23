{
  description = "Astral - Calculations for the sun and moon.";

  inputs.pyproject-nix.url = "github:nix-community/pyproject.nix";
  inputs.pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

  nixConfig = {
    bash-prompt = ''\n\[\033[1;34m\][\[\e]0;\u@\h: \w\a\]\u@\h:\w]\\$\[\033[0m\] '';
  };

  outputs = {
    nixpkgs,
    pyproject-nix,
    ...
  }: let
    inherit (nixpkgs) lib;

    project = pyproject-nix.lib.project.loadPyproject {
      projectRoot = ./.;
    };

    forAllSystems = function:
      nixpkgs.lib.genAttrs [
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ] (system: function nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (pkgs: (
      let
        python = pkgs.python3;
        arg = project.renderers.withPackages {inherit python;};
        pythonEnv = python.withPackages arg;
      in {
        default = pkgs.mkShell {
          packages = [
            pkgs.pdm
            pkgs.ruff
            pythonEnv
          ];
          shellHook = ''
            export PYTHONPATH=${builtins.toString ./src}
          '';
        };
      }
    ));

    packages = forAllSystems (pkgs: (
      let
        python = pkgs.python3;
        attrs = project.renderers.buildPythonPackage {inherit python;};
      in {
        default = python.pkgs.buildPythonPackage attrs;
      }
    ));
  };
}
