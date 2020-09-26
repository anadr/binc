#!/usr/bin/env python

import base64
import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='Provide a path to  a binary file', required=True)
    parser.add_argument('-o', '--output', type=str,
                        help='Provide a path to save output file', required=True)
    parser.add_argument('-t', '--type', type=str,
                        help='Provide b64, xor or aes', required=True)
    parser.add_argument('-l', '--length', type=int,
                        help='Provide the length of each string', default=0)

    return parser


def get_binary(args):
    binary_string = args.input

    with open(args.input, "rb") as fh:
        binary_string = fh.read().strip()

    return binary_string


def save_file(file_path, data):
    if os.path.exists(file_path):
        while True:
            user_input = input(
                "\n[!] File '" + file_path + "' already exists. Overwrite? (y|n): ").lower()
            if user_input == "no" or user_input == "n":
                print("Qutting.")
                exit(0)
            elif user_input == "yes" or user_input == "y":
                break
            else:
                print("[!] Invalid response.")
                continue

    with open(file_path, 'w') as fh:
        for line in data:
            fh.write(line + "\n")


def convert_b64(binary):
    base64_binary = base64.b64encode(binary).decode("ascii")
    return base64_binary


def main():
    parser = get_parser()
    args = parser.parse_args()

    binary = get_binary(args)
    length = args.length

    if args.type == "b64":
        converted_binary = convert_b64(binary)

    if length:
        converted_binary_list = [(converted_binary[i:i+length])
                                 for i in range(0, len(converted_binary), length)]
    else:
        converted_binary_list = [converted_binary]

    final_binc = ['"' + s + '"' for s in converted_binary_list]

    save_file(args.output, final_binc)
    print("\n[*] Saved file as: %s" % args.output)


if __name__ == "__main__":
    main()
