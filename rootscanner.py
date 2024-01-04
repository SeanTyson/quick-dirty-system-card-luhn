import os
import re

#This algorithm takes a card number and verifies it's possibly valid
def luhn_algorithm(card_number):
    # Reverse the card number and convert it to a list of integers
    digits = [int(digit) for digit in reversed(card_number)]

    # Double every second digit
    doubled_digits = [digit * 2 if index % 2 == 1 else digit for index, digit in enumerate(digits)]

    # Subtract 9 from doubled digits greater than 9
    subtracted_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]

    # Sum all the digits
    total = sum(subtracted_digits)

    # Check if the total is a multiple of 10
    return total % 10 == 0

#use pythons tandard library to open a file and get all the digits from it
def extract_digits_from_file(file_path):
    with open(file_path, 'r', errors='ignore') as file:
        content = file.read()
        #use regular expression to findall digits from file contents
        digits = re.findall(r'\d', content)
        return digits

#cba to wait for it to scan encoded files - they have lots of false positives
def is_valid_extension(filename):
    invalid_extensions = {'.zip', '.mp3', '.mp4', '.dll'}
    return not any(filename.lower().endswith(ext) for ext in invalid_extensions)

#go through each directory and file and pass to helper functions, build card digit sequence and verify
def scan_files_and_check_luhn():
    valid_numbers = []

    try:
        current_directory = os.getcwd()
        for foldername, subfolders, filenames in os.walk(current_directory, followlinks=True):
            print(foldername)
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                try:
                    if is_valid_extension(filename):
                        file_digits = extract_digits_from_file(file_path)

                        # Check Luhn algorithm on each 16-digit sequence
                        for i in range(len(file_digits) - 15):
                            sixteen_digits = ''.join(file_digits[i:i+16])
                            if luhn_algorithm(sixteen_digits):
                                valid_numbers.append((filename, sixteen_digits))
                except PermissionError as pe:
                    print(f"Permission error for {file_path}: {pe}")
    except Exception as e:
        print(f"Error processing: {e}")

    return valid_numbers

#entry point for running a python script where no code exists outside of a function
if __name__ == "__main__":
    valid_numbers = scan_files_and_check_luhn()

    # Print valid numbers and filenames
    print("Valid Numbers:")
    for filename, number in valid_numbers:
        print(f"Filename: {filename}, Valid Number: {number}")
