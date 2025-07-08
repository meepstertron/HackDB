import argparse
import time
import requests
import uuid
import os
import json

config_path = os.path.expanduser("~/.hexagonical/hackdb/config.json")
config = {}


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception:
        print(Warning("Config file empty or nonexistent"))
        config = {}
else:
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

if config.get("instanceid") is None:
    config["instanceid"] = str(uuid.uuid4())
if config.get("api_url") is None:
    config["api_url"] = "https://hackdb.hexagonical.ch/api/sdk/v1"
    print(f"{color.YELLOW}No API URL found in config, using default: {config['api_url']} set your own using 'hackdb config url'{color.END}")
    
with open(config_path, "w") as f:
    json.dump(config, f, indent=4)

# - Helpers -
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
        print(color.CYAN + r"""
╔════════════════════════════╗
║      HackDB CLI Tool       ║
╚════════════════════════════╝
""" + color.END)

def show_credits(used=0, total=10, change=0, unlimited=False, extra_credits=0):
    bar_length = 20
    filled = int((used / total) * bar_length)
    bar = '█' * filled + '-' * (bar_length - filled)
    icon = "▼" if change < 0 else "▲"
    
    if unlimited:
        bar = 'x' * bar_length  # Full bar for unlimited credits
    
        
    change_text = f"{icon} {abs(change)}% {color.GREEN+'less' if change < 0 else color.RED+'more'} than last week"
    if change == 0:
        change_text = "— "+ color.PURPLE+"No change in credits this week"
    

    if used > total and not unlimited:
        used = total
        print(f"{color.RED}Overdrawn!{color.END}")
    
    if unlimited:
        print(f"{color.GREEN}Unlimited!{color.END}")
    extra_credits_text = f"| {color.GREEN}+{extra_credits} extra {color.END}" if extra_credits > 0 else ''
    print(f"{color.YELLOW}Credits Used:{color.END} {used}/{total if not unlimited else '∞'} {extra_credits_text}")
    print(f"[{bar}]")
    print("\n")
    print(f"{change_text}{color.END}")

# - helpers -


def login(args):
    print_header()
    print("""What method would you like to use to login?
        1. SDK Token (offers limited access)
        2. Slack OAUTH (requires a hackclub slack account)

 """)
    
    choice = input("Enter your choice (1-2): ")
    

    if choice == '3':

        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print(f"Logging in with username: {username} and password: {password}")
        config['method'] = "username_password"
        config['username'] = username
        config['password'] = password
    elif choice == '1':
        token = input("Enter your SDK Token: ")
        if not token.startswith("hkdb_tkn_"):
            print("Invalid SDK Token format. Exiting...")
            exit(1)

        print(f"Logging in with SDK Token")
        

        

        response = requests.get(config['api_url']+"/validatetoken", headers={
            "Authorization": f"Bearer {token}"
        })
        
        if response.status_code == 500:
            print("Server error. Please try again later.")
            exit(1)
        
        if response.status_code != 200:
            print("Invalid SDK Token. Please try again.")
            exit(1)


        if response.json().get("valid") is True:
            config['method'] = "sdk_token"
            config['token'] = token
            print(f"{color.GREEN}Success! :){color.END}")
        
        else:
            print(f"{color.RED}Invalid SDK Token.{color.END}")
            exit(1)
    elif choice == '2':

        #open page with redirect to hackdb.hexagonical.ch/api/cli/slackauth?instanceid={config.instanceid}
        
        
        result = requests.get(config['api_url']+"/cli/slackauthresult", params={"instanceid": config["instanceid"]})
        try:
            result_json = result.json()
        except Exception:
            result_json = {}
        if result_json.get("token") is not None:
            print(f"{color.GREEN}There was a record already associated with this account. Use?{color.END}")
            answer = input("(y/n): ").strip().lower()
            if answer == 'y':
                config['method'] = "slack_oauth"
                config['token'] = result_json['token']
                config['slack_user_id'] = result_json['slack_id']
                config['user_id'] = result_json['user_id']
                print(f"{color.GREEN}Success! :){color.END}")
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=4)
                exit(0)
                
        
        print("Redirecting to Slack OAUTH...")
        print("Please follow the instructions in your browser to complete the Slack OAUTH process.")
        print("After completing the process, return here to continue.")
        
                #open webpage in browser
        try:
            os.system(f'start {config["api_url"]}/cli/slackauth?instanceid={config["instanceid"]}')
        except Exception as e:
            print(f"Error opening browser: {e}")
            print("Please open the following URL in your browser:")
            print(f"{config['api_url']}/cli/slackauth?instanceid={config['instanceid']}")
            
        


        shouldPoll = True # value to tell it if it should poll server for oauth data
        pollcount = 0
        while shouldPoll:
            print("Polling server...")
            result = requests.get(config['api_url']+"/cli/slackauthresult", params={"instanceid": config["instanceid"]})
            time.sleep(2)
            pollcount += 1
            if pollcount > 20:
                print("Polling timed out. Please try again.")
                exit(1)
            if result.status_code == 200 and result.json().get("token") is not None:
                config['method'] = "slack_oauth"
                config['token'] = result.json()['token']
                config['slack_user_id'] = result.json()['slack_id']
                config['user_id'] = result.json()['user_id']
                print(f"{color.GREEN}Success! :){color.END}")
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=4)
                shouldPoll = False
                exit(0)
            elif result.status_code == 500:
                print("Server error. Please try again later.")
                exit(1)


        print(f"{color.RED}Unexpected error.{color.END}")
        exit(1)

        
    elif choice == '4':
        print("Redirecting to Hexagonical Auth...")
        print("Please follow the instructions in your browser to complete the Hexagonical Auth process.")
        print("After completing the process, return here to continue.")
        config['method'] = "hexagonical_auth"
    
    else:
        print("Invalid choice. Please try again.")
    #save config file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def status(args):
    print_header()
    invalid = False
    if config.get("method") is None:
        print(f"{color.RED}You are not logged in!{color.END}")
        print("Please login using 'hackdb login'")
        return
    
    print(f"{color.YELLOW}Current Method:{color.END} {config['method']}")
    
    if config['method'] == "sdk_token":
        
        response = requests.get(config['api_url']+"/validatetoken", headers={
            "Authorization": f"Bearer {config['token']}"
        })
        if response.status_code == 500:
            print("Server error. Please try again later.")
            return

        print(f"{color.YELLOW}SDK Token:{color.END} {config['token'][:16] + '*' * 16} (Valid: {not invalid})")
    elif config['method'] == "slack_oauth":
        print(f"{color.YELLOW}Slack User ID:{color.END} {config.get('slack_user_id', 'Not set')}")

def credits(args):
    if config.get("method") is None:
        print(f"{color.RED}You are not logged in!{color.END}")
        print("Please login using 'hackdb login'")
        return

    response = requests.get(config['api_url']+"/cli/credits?method="+config['method'], headers={
        "Authorization": f"Bearer {config['token']}"
    })
    
    if response.status_code == 500:
        print("Server error. Please try again later.")
        return
    if response.status_code != 200:
        print(f"{color.RED}Error fetching credits: {response.json().get('error', 'Unknown error')}{color.END}")
        return
    data = response.json()

    print_header()
    show_credits(used=data.get("used_this_week"), total=data.get('credits'), change=data.get("change_percent"), unlimited=data.get('unlimited', False), extra_credits=data.get('extra_credits', 0))
    
    
def configure(args):
    if args.option == 'url':
        new_url = input("Enter the new API URL: ")
        config['api_url'] = new_url
        print(f"API URL updated to: {new_url}")
    elif args.option == 'logout':
        olduuid = config.get("instanceid")
        oldurl = config.get("api_url")
        config.clear()
        config["instanceid"] = olduuid
        config["api_url"] = oldurl
        print("Logged out successfully. Configuration cleared.")
    else:
        print("Invalid option. Use 'url' to set API URL or 'logout' to clear configuration.")
    
    #save config file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
        
def databases(args):
    return

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
    parser_credits.set_defaults(func=credits)
    
    # hackdb config
    parser_config = subparsers.add_parser('config', help='Configure HackDB CLI')
    parser_config.add_argument('option', choices=['url', 'logout'], help='Configuration option to set')
    parser_config.set_defaults(func=configure)
    
    # hackdb databases
    parser_databases = subparsers.add_parser('databases', help='Show databases')
    parser_databases.set_defaults(func=databases)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()