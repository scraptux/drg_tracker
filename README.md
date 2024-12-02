# DRG-Tracker

This is the source code powering [drg-tracker.de](https://www.drg-tracker.de), a site dedicated to tracking changes in ICD-10-GM and OPS codes.
Tracking these changes is useful to manage medical coding efficiently and to retrospectively analyse coded data.

## Features

- **Change Tracking**: Stay updated on modifications, additions, and removals of ICD-10-GM and OPS codes.
- **Search & Browse**: Quickly search for specific codes or browse categories.
- **Compare Versions**: Easily compare different versions of the ICD-10-GM and OPS standards.
- **User-Friendly Interface**: Built with Vue.js for a responsive and intuitive frontend.
- **Scalable Backend**: Django powers a robust and scalable backend to handle data processing and API requests.

## Technologies Used

- **Frontend**: Vue
- **Backend**: Django
- **Database**: PostgreSQL

## Getting Started

Currently, deployment to a NixOS server is supported.
The frontend and the backend can be built using standard tools or using nix.

If help is needed to deploy the codebase in other ways, feel free to reach out.

### Installation

1. Include this repository in your NixOS flake and import the module:
    ``` nix
    inputs = {
        ...
        drgtracker.url = "github:scraptux/drg_tracker";
        drgtracker.inputs.nixpkgs.follows = "nixpkgs";
        ...
    };
    
    ```
    ``` nix
    imports = [
        ...
        inputs.drgtracker.nixosModules.default
        ...
    ];
    ```
2. Add the module specific configuration to your config:
    ``` nix
    services.drgtracker = {
        enable = true;
        environmentFile = /path/to/.env
        frontend = {
            enable = true;
            host = "127.0.0.1";
            port = 80;
        };
        backend = {
            enable = true;
            host = "127.0.0.1";
            port = 8000;
        };
    };
    ```
3. Make sure PostgreSQL is enabled and ensure a user and a database called `drgtracker`.
4. Run migrations:
    ``` bash
    nix run github:scraptux/drg_tracker -- migrate
    ```
5. Import ICD-10 and OPS data:
    ``` bash
    nix run github:scraptux/drg_tracker -- runscript import_<icd/ops> --script_args=<year>
    ```

## License

This project is licensed under [GPL-3.0](LICENSE).

