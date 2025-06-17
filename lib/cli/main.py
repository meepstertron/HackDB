import argparse
import requests
import uuid
import os
import json

config_path = os.path.expanduser("~/.hackdb/config.json")
config = {}

if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception:
        raise Warning("Config file empty or nonexistent")
        config = {}

config["instanceid"] = uuid.uuid4()

def login(args):
    print("HackDB " + "indev1" + " - CLI")
    print("""What method would you like to use to login?
        1. (WIP)Username and Password
        2. SDK Token (offers limited access)
        3. Slack OAUTH (requires a hackclub slack account)
        4. (WIP)Hexagonical Auth
 """)
    
    choice = input("Enter your choice (1-4): ")
    

    if choice == '1':

        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print(f"Logging in with username: {username} and password: {password}")
        config['method'] = "username_password"
        config['username'] = username
        config['password'] = password
    elif choice == '2':
        token = input("Enter your SDK Token: ")
        if not token.startswith("hkdb_tkn_"):
            print("Invalid SDK Token format. Exiting...")
            exit(1)
        
        print(f"Logging in with SDK Token: {"*"*token.count()}")
        
        config['method'] = "sdk_token"
        config['token'] = token
    elif choice == '3':
        print("Redirecting to Slack OAUTH...")
        print("Please follow the instructions in your browser to complete the Slack OAUTH process.")
        print("After completing the process, return here to continue.")
        #open page with redirect to hackdb.hexagonical.ch/api/cli/slackauth?instanceid={config.instanceid}
        
        shouldPoll = True # value to tell it if it should poll server for oauth data
        while shouldPoll:
            print("Polling server...")
            result = requests.get

        

        config['method'] = "slack_oauth"
    elif choice == '4':
        print("Redirecting to Hexagonical Auth...")
        print("Please follow the instructions in your browser to complete the Hexagonical Auth process.")
        print("After completing the process, return here to continue.")
        config['method'] = "hexagonical_auth"
    
    else:
        print("Invalid choice. Please try again.")
    #save config file
    open("~/.hackdb/config.json", mode="rw") 

def status(args):
    print("Status: OK")

def credits():
    print("You have 1 credit remaining.")

def main():
    parser = argparse.ArgumentParser(prog='hackdb', description='HackDB CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # hackdb login
    parser_login = subparsers.add_parser('login', help='Login to HackDB')
    parser_login.set_defaults(func=login)

    # hackdb status
    parser_status = subparsers.add_parser('status', help='Show status')
    parser_status.set_defaults(func=status)

    # hackdb credits
    parser_credits = subparsers.add_parser('credits', help='Show user credits')

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()