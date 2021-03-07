#!/usr/local/bin/python3
"""
Execute this command to get pw from json into clipboard.
Type "pw -h" to get help on all available commands.
Basic usage: "pw <entity>" -> Gets password of entity from main section.

The creds.json file should look like this:

"section": {
        "entity": {
            "password": "lorem",
            "username": "ipsum",
            "additional_info": "...",
            "website": "www.kuda.ai"
        }
    }
"""
import argparse
from pw_config import CREDS_DIR, CREDS_FILE_PATH
import pw_client
import pyperclip

HELP_TEXT = {
    'input': 'Name of entity that holds the password.',
    'all_sections': 'Print all available sections.',
    'section':
        '''Pass a section to print all entities of that section.
        The -s flag can be used together with other functions:
          Use it with "-add_new_password" to write pw to a specific section:
            "pw -n GitHub -s dev
          Use it with an argument without a flag to get a password from a specific section:
            "pw -s dev GitHub" -- Gets password for "GitHub" from the section "dev"''',
    'add_new_password': 'Pass an entity as arg and add a new password to the json file.',
    'generate_random_pw': 'Print a randomly generated password and add it to your clipboard.',
    'remove':
        '''Delete a password from the creds file. Combine together with -s 
        if the password you want to delete is in another section than "main".
        Example: "pw -d GitHub -s dev" -> Remove the password for GitHub
        from the section "dev".'''
}


def parse_args():
    parser = argparse.ArgumentParser(description='Manage your passwords from the terminal.')
    parser.add_argument('input', type=str, help=HELP_TEXT['input'], nargs='?')
    parser.add_argument('-as', '--all_sections', action='store_true', help=HELP_TEXT['all_sections'])
    parser.add_argument('-s', '--section', type=str, help=HELP_TEXT['section'])
    parser.add_argument('-r', '--generate_random_pw', action='store_true', help=HELP_TEXT['generate_random_pw'])
    parser.add_argument('-n', '--add_new_password', type=str, help=HELP_TEXT['add_new_password'])
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('-w', '--website', type=str)
    parser.add_argument('-rm', '--remove', type=str, help=HELP_TEXT['remove'])

    args = parser.parse_args()
    return args


def main(parsed_args):
    args = parsed_args
    pw = pw_client.PasswordClient(CREDS_DIR, CREDS_FILE_PATH)

    if args.all_sections:
        return pw.print_sections()

    if args.add_new_password:
        return pw.add_new_pw(entity=args.add_new_password, username=args.username, website=args.website)

    if args.remove:
        # TODO: Write a function in pw_client.py that deletes a password.
        pass

    if args.section and args.input:
        return pw.get_pw(args.input, args.section)

    if args.section:
        return pw.print_keys_of_section(args.section)

    if args.generate_random_pw:
        random_pw = pw.generate_random_password()
        print('Here is your random password:')
        print(random_pw)
        print('It has been copied into your clipboard.')
        pyperclip.copy(random_pw)
        return

    if args.input is None:
        return print('Nothing happened. No flags used. No args passed after pw command.')

    return pw.get_pw(args.input)


if __name__ == '__main__':
    args = parse_args()
    main(args)
