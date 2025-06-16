import argparse


def login(args):
    print("HackDB " + "indev1" + " - CLI")
    print("""What method would you like to use to login?
        1. (WIP)Username and Password
        2. SDK Token (offers limited access)
        3. Slack OAUTH (requires a hackclub slack account)
        4. (WIP)Hexagonical Auth
 """)
    
    choice = input("Enter your choice (1-4): ")
    config = {}

    if choice == '1':

        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print(f"Logging in with username: {username} and password: {password}")
        config['method'] = "username_password"
        config['username'] = username
        config['password'] = password
    elif choice == '2':
        token = input("Enter your SDK Token: ")
        print(f"Logging in with SDK Token: {token}")
        config['method'] = "sdk_token"
        config['token'] = token
    elif choice == '3':
        print("Redirecting to Slack OAUTH...")
        print("Please follow the instructions in your browser to complete the Slack OAUTH process.")
        print("After completing the process, return here to continue.")

        config['method'] = "slack_oauth"
    elif choice == '4':
        print("Redirecting to Hexagonical Auth...")
        print("Please follow the instructions in your browser to complete the Hexagonical Auth process.")
        print("After completing the process, return here to continue.")
        config['method'] = "hexagonical_auth"
    else:
        print("Invalid choice. Please try again.")

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

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()