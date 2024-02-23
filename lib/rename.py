#!/usr/bin/python

import os
import re


def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file[0].isupper() and file[-5:] == ".dart":
                old_path = os.path.join(root, file)
                # Convert CamelCase to snake_case
                snake_case = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", file)
                snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", snake_case).lower()
                new_path = os.path.join(root, snake_case)
                os.rename(old_path, new_path)


def modify_dart_line(line):
    if line.strip().endswith(".dart';"):
        index = line.rfind("/")
        if index != -1:
            # Extract the file name from the line
            file_name = line[index + 1 : -8]
            # Convert the file name to snake_case
            snake_case = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", file_name)
            snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", snake_case).lower()
            # Replace the file name in the line with the snake_case version
            modified_line = line[: index + 1] + snake_case + ".dart';\n"
            return modified_line
        else:
            index = line[:-5].rfind("'")
            file_name = line[index + 1 : -8]
            # Convert the file name to snake_case
            snake_case = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", file_name)
            snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", snake_case).lower()
            # Replace the file name in the line with the snake_case version
            modified_line = line[: index + 1] + "./" + snake_case + ".dart';\n"
            return modified_line
    return line


def fix_links(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:

            new_path = os.path.join(root, file)

            # Search and rename links to .dart files
            modified_lines = []
            with open(new_path, "r", encoding="ISO-8859-1") as file:
                for line in file:
                    modified_line = modify_dart_line(line)
                    modified_lines.append(modified_line)

            # Write the updated content to the file
            with open(new_path, "w", encoding="ISO-8859-1") as file:
                file.writelines(modified_lines)


# Aktuelles Verzeichnis durchlaufen
current_directory = os.getcwd()
rename_files(current_directory)
fix_links(current_directory)
