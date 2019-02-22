import argparse
import os
import shutil
from simple_idml import idml
import process_story as process


def process_stories(args, package):
    for story in package.stories:
        htmlContent = process.process_story(story, package, args)
        file = open(args.extract + "text.html", "w")
        file.write(htmlContent)
        file.close()


def process_file(args):
    # Read provided idml file
    package = idml.IDMLPackage(args.path)

    # if document does not exist
    if not os.path.exists(args.extract):
        print("Extracting xml files from indesign ...")
        package.extractall(args.extract)

    # if document does exist, remove current folder and extract files again
    if os.path.exists(args.extract):
        shutil.rmtree(args.extract)
        package.extractall(args.extract)

    process_stories(args, package)


def main():
    parser = argparse.ArgumentParser(description="Process file arguments")
    parser.add_argument('--path', type=str, help='Path of the file')
    parser.add_argument('--extract', type=str, default="./documents/",
                        help='Folder to extract idml structure')
    args = parser.parse_args()
    process_file(args)


main()
