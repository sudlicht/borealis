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
    # Development shell environment for developing borealis
    devShells.${system}.default = pkgs.mkShell {
      name = "borealis-dev";
      packages = with pkgs; [
        python313
        python313Packages.pygobject3
        python313Packages.pygobject-stubs
        gtk4
        gtk4-layer-shell
      ];

      shellHook = ''
        echo -e '\033[0;31mStarted Borealis development environment.'
      '';
    };

  };
}