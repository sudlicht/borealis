{
  description = "Borealis -- an abstraction layer over gtk4.0 and pygobject";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: 
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {    
    # Development shell environment for running a borealis application
    devShells.${system} = {
      default = pkgs.mkShell {
        name = "borealis-dev";
        packages = with pkgs; [
          python313
          python313Packages.pygobject3
          python313Packages.pygobject-stubs
          gtk4
          gtk4-layer-shell
        ];

        shellHook = ''
          export LD_PRELOAD="${pkgs.gtk4-layer-shell}/lib/libgtk4-layer-shell.so"
          echo -e '\033[0;31mStarted Borealis development environment.'
          echo -e '\033[0;37mNote: VS-Code will not work properly in this environment (try vscode devShell).'
          echo -e 'Please use this environment in a wayland terminal.'
        '';
      };

      vscode = pkgs.mkShell {
        name = "borealis-vscode-dev";
        packages = with pkgs; [
          python313
          python313Packages.pygobject3
          python313Packages.pygobject-stubs
          gtk4
          gtk4-layer-shell
        ];

        shellHook = ''
          echo -e '\033[0;31mStarted Borealis development environment.'
          echo -e '\033[0;37mNote: with gtk4-layer-shell loading you cannot run an application.'
          echo -e 'Please use the default devShell for that in a wayland terminal (non-vscode integrated).'
          code .
        '';
      };
    };
  };
}