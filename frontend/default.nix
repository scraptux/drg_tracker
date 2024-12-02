{ pkgs ? import <nixpkgs> {} }:
let
  pname = "drg-tracker-frontend";
  version = "0.1.0";
  src = ./.;
in
pkgs.mkYarnPackage {
  inherit pname version src;
  
  packageJSON = "${src}/package.json";
  offlineCache = pkgs.fetchYarnDeps {
    yarnLock = "${src}/yarn.lock";
    hash = "sha256-sM9z7nHuTV35tmVaIfGRtsmAUT4s10OpBDSswtMWWn0=";
  };

  configurePhase = ''
    cp -r $node_modules node_modules
    chmod +w node_modules
  '';

  buildPhase = ''
    yarn --offline build
  '';

  installPhase = ''
    cp -r dist/ $out
  '';

  doDist = false;

  meta = with pkgs.lib; {
    description = "Web-Frontend for DRG-Tracker";
    homepage = "drg-tracker.de";
    license = licenses.gpl3Plus;
    maintainers = [ maintainers.scraptux ];
  };
}
