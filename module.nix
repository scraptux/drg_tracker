{ self }:
{ config, options, lib, pkgs, ... }:
with lib;
let
  cfg = config.services.drgtracker;
  defaultUser = "drgtracker";
in {
  options.services.drgtracker = {
    enable = mkEnableOption "Whether to enable the drg-tracker service.";
    virtualHost = mkOption {
      type = types.str;
      default = "drgtracker";
      description = "nginx virtualHost name";
    };
    environmentFile = lib.mkOption {
      type = lib.types.path;
      example = "/run/secrets/drgtracker";
      description = ''
        Path to the file containing environment variables, e.g. DRGTRACKER_SECRET.
      '';
    };

    frontend = {
      enable = mkEnableOption "Enable the drg-tracker frontend.";
      package = mkPackageOption self.packages.${pkgs.system} "frontend" { };
      host = mkOption {
        type = types.str;
        default = "127.0.0.1";
        description = "Host for the frontend to listen on.";
      };
      port = mkOption {
        type = types.port;
        default = 80;
        description = "Port for the frontend to listen on.";
      };
    };

    backend = {
      enable = mkEnableOption "Enable the drg-tracker backend.";
      package = mkPackageOption self.packages.${pkgs.system} "backend" { };
      host = mkOption {
        type = types.str;
        default = "127.0.0.1";
        description = "Host for the backend to listen on.";
      };
      port = mkOption {
        type = types.port;
        default = 8000;
        description = "Port for the backend to listen on.";
      };
      extraGunicornArgs = mkOption {
        type = types.listOf types.str;
        default = [];
        description = "Extra arguments to pass to Gunicorn.";
      };
    };
  };

  config = mkIf cfg.enable {
    # Ensure service user
    users.groups.drgtracker = {};
    users.users.${defaultUser} = {
      isSystemUser = true;
      description = "DRG Tracker Service User";
      home = "/var/lib/${defaultUser}";
      createHome = true;
      group = "drgtracker";
    };

    # Backend service using Gunicorn
    systemd.services.drgtracker-backend = mkIf cfg.backend.enable {
      description = "DRG Tracker Backend Service";
      after = [ "network.target" ];
      wants = [ "network.target" ];
      serviceConfig = {
        User = defaultUser;
        Group = defaultUser;
        WorkingDirectory = cfg.backend.package;
        EnvironmentFile = cfg.environmentFile;
        ExecStart = ''
          ${cfg.backend.package}/bin/gunicorn \
            ${concatStringsSep " " cfg.backend.extraGunicornArgs} \
            --bind ${cfg.backend.host}:${toString cfg.backend.port} \
            backend.wsgi
        '';
        Restart = "always";
      };
      wantedBy = [ "multi-user.target" ];
    };

    # Frontend service and reverse proxy
    services.nginx = mkIf cfg.frontend.enable {
      enable = true;
      virtualHosts."${cfg.virtualHost}" = {
        listen = [{ addr = cfg.frontend.host; port = cfg.frontend.port; }];
        root = cfg.frontend.package;
        extraConfig = ''
          location /api/ {
            proxy_pass http://${cfg.backend.host}:${toString cfg.backend.port};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
          }
          location / {
            try_files $uri $uri/ /index.html;
          }
        '';
      };
    };
  };
}
