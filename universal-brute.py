import argparse
from sys import stdout
from unittest import result
from numpy import array
from termcolor import colored, cprint
from argparse import RawTextHelpFormatter
import csv
from os.path import exists
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description="Universal Brute Forcer, brute forcer of last resort",
        formatter_class=RawTextHelpFormatter)
    
    parser.add_argument(
        "-u",
        dest="usernames",
        default=None,
        help="Individual or comma-separated list of usernames")

    parser.add_argument(
        "-U",
        dest="usernames_file",
        metavar="[USERNAME FILE]",
        default=None,
        help="Path to usernames file")

    parser.add_argument(
        "-p",
        dest="passwords",
        default=None,
        help="Individual or comma-separated list of usernames")
    
    parser.add_argument(
        "-P",
        dest="passwords_file",
        metavar="[PASSWORD FILE]",
        default=None,
        help="Path to passwords file")

    parser.add_argument(
        "-t",
        dest="targets",
        default=None,
        help="Individual or comma-separated list of targets")
    
    parser.add_argument(
        "-T",
        dest="targets_file",
        metavar="[TARGETS FILE]",
        default=None,
        help="Path to targets file")
    
    parser.add_argument(
        "-c",
        dest="command_template",
        required=True,
        help="The command to be executed. eg: 'mysql -h {TARGET} -u {USER} -p{PASS}'")
    
    parser.add_argument(
        "-f",
        dest="failure_string",
        help="Output string of the command which signifies failure")

    parser.add_argument(
        "-s",
        dest="success_string",
        help="Output string of the command which signifies success")
    
    parser.add_argument(
        "-q",
        dest="quiet",
        default=False,
        action="store_true",
        help="If set, suppress any failure messages and only show successes")

    
    args = parser.parse_args()
    usernames_list = values_from_parameters(args.usernames, args.usernames_file)
    passwords_list = values_from_parameters(args.passwords, args.passwords_file)
    targets_list = values_from_parameters(args.targets, args.targets_file)

    command_template = args.command_template

    commands = generate_commands(
        usernames=usernames_list,
        passwords=passwords_list,
        targets=targets_list,
        command_template=command_template)

    for command in commands:
        result = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode().strip() + "|" + result.stderr.decode().strip()
        if args.success_string:
            if args.success_string in output:
                cprint("[✅] {}".format(output),"green")
        if args.failure_string and not args.quiet:
            if args.failure_string in output:
                cprint("[❌] {}".format(output),"red")



def generate_commands(usernames:set, passwords:set, targets:set, command_template:str):
    commands = set()
    # Checking to avoid screwing up command template
    if "{USER}" in command_template:
        if usernames == None:
            cprint("Command template requires usernames, but none were provided")
            quit()
    if "{PASS}" in command_template:
        if passwords == None:
            cprint("Command template requires password, but none were provided")
            quit()
    if "{TARGET}" in command_template:
        if targets == None:
            cprint("Command template requires target, but none were provided")
            quit()

    for username in usernames:
        for password in passwords:
            for target in targets:
                commands.add(command_template.replace("{USER}",username).replace("{PASS}",password).replace("{TARGET}",target))
    
    return commands

    
def values_from_parameters(argument_string, argument_file):
    output = set()

    # Handle Argument String as Properly Formatted CSV
    if argument_string:
        if "," in argument_string:
            print("#[i] One of the provided arguments included a comma, it is being processed as a CSV. If this is not desired, wrap the parameter in doublequotes")

        lines = argument_string.splitlines()
        reader = csv.reader(lines)
        parsed_csv = list(reader)
        for parsed_csv_line in parsed_csv[0]:
            output.add(parsed_csv_line.strip())
    
    # Handle argument file
    if argument_file: 
        if exists(argument_file):
            file = open(argument_file)
            file_lines = file.readlines()
            for file_line in file_lines:
                output.add(file_line.strip())

    if output:
        return output
    else:
        return None



if __name__ == "__main__":
    main()
