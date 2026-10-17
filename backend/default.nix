{ pkgs ? import <nixpkgs> {} }:
let
  pname = "drg-tracker-backend";
  version = "0.1.0";
  src = ./.;
in
pkgs.python3Packages.buildPythonApplication rec {
  inherit pname version src;
  pyproject = false;

  nativeBuildInputs = [
    pkgs.gettext
  ];

  dependencies = with pkgs.python3Packages; [
    django
    django-extensions
    djangorestframework
    django-cors-headers
    progressbar
    psycopg2
  ];

  postBuild = ''
    ${pkgs.python3.pythonOnBuildForHost.interpreter} -OO -m compileall .
  '';

  installPhase = let
    pythonPath = pkgs.python3Packages.makePythonPath dependencies;
  in ''
    runHook preInstall

    mkdir -p $out/lib/drg-tracker/src
    cp -r . $out/lib/drg-tracker/src/
    chmod +x $out/lib/drg-tracker/src/manage.py

    makeWrapper $out/lib/drg-tracker/src/manage.py $out/bin/drg-tracker \
      --prefix PYTHONPATH : "${pythonPath}"
    makeWrapper ${pkgs.python3Packages.gunicorn}/bin/gunicorn $out/bin/gunicorn \
      --prefix PYTHONPATH : "${pythonPath}:$out/lib/drg-tracker/src" \
      --set DJANGO_SETTINGS_MODULE "backend.settings"

    runHook postInstall
  '';

  meta = with pkgs.lib; {
    description = "Backend for DRG-Tracker";
    homepage = "https://drg-tracker.de";
    license = licenses.gpl3Plus;
    maintainers = [ maintainers.scraptux ];
  };
}
