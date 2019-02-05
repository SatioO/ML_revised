import argparse
import os
import shutil
from simple_idml import idml
import xml.etree.ElementTree as ET
import decode_color


def get_alignment(args):
    # Function to get text alignment : defaults to left
    switcher = {
        "CenterAlign": "text-align: center",
        "RightAlign": "text-align: right",
        "LeftAlign": "text-align: left",
    }

    return switcher.get(args, switcher["LeftAlign"])


def get_font_weight(args):
    # Function to get font weight : defaults to normal
    switcher = {
        "Bold": "font-weight: bold",
        "Italics": "font-weight: italics",
        "Normal": "font-weight: normal",
    }

    return switcher.get(args, switcher["Normal"])


def get_font_size(args):
    # Function to get font size : defaults to 12pt
    return "font-size: " + args + "pt" if args else "font-size: 12pt"


def get_font_family(args):
    # Function to get font family: defaults to minion pro
    return "font-family:" + args if args else "font-family: Minion Pro"


def get_line_height(args):
    # Function to get line height: defaults to 14.4pt
    return "line-height:" + args + "pt" if args else "line-height: 14.4pt"


def process_stories(args, package):
    for story in package.stories:
        tree = ET.parse(args.extract + story)
        root = tree.getroot()

        htmlContent = ""
        paragraphStyleRanges = root.iter("ParagraphStyleRange")

        for paragraphStyleRange in paragraphStyleRanges:
            alignment = paragraphStyleRange.attrib.get("Justification")
            alignment = get_alignment(alignment)
            paragraghStyle = "<p style='" + alignment + ";'>"

            for characterStyleRange in paragraphStyleRange.iter(
                    "CharacterStyleRange"):

                characterStyle = ""

                # Get the font style
                fontStyle = characterStyleRange.attrib.get("FontStyle")
                fontStyle = get_font_weight(fontStyle)

                # Get the font size
                fontSize = characterStyleRange.attrib.get("PointSize")
                fontSize = get_font_size(fontSize)

                # Get the font color
                fontColor = characterStyleRange.attrib.get("FillColor")
                fontColor = decode_color.get_color(fontColor, package, args)

                # Get the font family
                fontFamily = get_font_family(None)
                # Get the line height
                lineHeight = get_line_height(None)

                for child in characterStyleRange.iter():
                    if child.tag == "Properties":
                        for properties in child.iter():
                            if properties.tag == "Leading":
                                lineHeight = get_line_height(properties.text)

                            if properties.tag == "AppliedFont":
                                fontFamily = get_font_family(properties.text)

                    if child.tag == "Content":
                        characterStyle += "<span style='" + fontStyle + ";" if fontStyle else ""
                        characterStyle += fontColor + ";" if fontColor else ""
                        characterStyle += fontFamily + ";" if fontFamily else ""
                        characterStyle += lineHeight + ";" if lineHeight else ""
                        characterStyle += fontSize + ";" if fontSize else ""
                        characterStyle += "'>" + child.text if child.text else "'>"
                        characterStyle += "</span>"

                    if child.tag == "Br":
                        characterStyle += "<br />"

                # Append character style to paragraph style
                paragraghStyle += characterStyle

            # Close the paragraph style
            paragraghStyle += "</p>"
            htmlContent += paragraghStyle

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
