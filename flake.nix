{
  description = "ICD-/OPS-Code change tracking";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    backend = system: nixpkgs.legacyPackages.${system}.callPackage ./backend/default.nix {};
    frontend = system: nixpkgs.legacyPackages.${system}.callPackage ./frontend/default.nix {};
  in {
    nixosModules.drgtracker = (import ./module.nix) { inherit self; };
    nixosModules.default = self.nixosModules.drgtracker;

    packages."x86_64-linux".backend = backend "x86_64-linux";
    packages."x86_64-linux".frontend = frontend "x86_64-linux";
  };
}
