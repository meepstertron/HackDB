# How to use the CLI

The HackDB CLI lets you manage your databases and tables directly from your terminal.

## Installation

Install the CLI using pip:

```sh
pip install hackdb-cli
```

## Getting Started

1. Log in to your account:
   ```sh
   hackdb login
   ```
   Select your preferred login method (Slack is recommended).

2. Check your instance status:
   ```sh
   hackdb status
   ```

## Common Commands

- `hackdb status`  
  Get the status of your HackDB instance.

- `hackdb credits`
  Get the ammound of availible credits.

- `hackdb databases`  
  List all your databases and their IDs.

- `hackdb drop <database id>`  
  **Irreversibly** drop a database.

- `hackdb table list -d <database name>`  
  List all tables in a database.

- `hackdb table`  
  (See `hackdb table --help` for more options.)

## Tips

- Use `hackdb --help` or `hackdb <command> --help` for detailed usage info.
- Make sure you are logged in before running commands.

## Troubleshooting

If you encounter issues, check your network connection and authentication status. For bugs or feature requests, see the [contributing guide](contributing.md).
