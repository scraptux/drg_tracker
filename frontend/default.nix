{ pkgs ? import <nixpkgs> {} }:

pkgs.buildNpmPackage {
  pname = "drg-tracker-frontend";
  version = "0.1.0";
  src = ./.;

  npmDepsHash = "sha256-wkuhE/7TfFbvvti/S5unzoUzRN5/g3rBSsbdwJSV6YU=";

  npmBuildScript = "build";

  installPhase = ''
    runHook preInstall
    cp -r dist/ $out
    runHook postInstall
  '';

  meta = with pkgs.lib; {
    description = "Web-Frontend for DRG-Tracker";
    homepage = "https://drg-tracker.de";
    license = licenses.gpl3Plus;
    maintainers = [ maintainers.scraptux ];
  };
}
