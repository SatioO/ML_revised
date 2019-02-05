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


def get_color(color, package, args):
    tree = ET.parse(
        args.extract + package.graphic.name)

    currentColor = "rgb(0, 0, 0)"

    for i in tree.getroot().iter("Color"):
        if i.attrib["Self"] == color:
            colorValue = i.attrib["ColorValue"].split(" ")
            currentColor = "rgb" + str(decode_color.cmyk_to_rgb(
                float(colorValue[0]), float(colorValue[1]), float(colorValue[2]), float(colorValue[3])))

    return "color:" + currentColor
