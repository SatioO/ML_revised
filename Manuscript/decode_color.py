import xml.etree.ElementTree as ET

rgb_scale = 255
cmyk_scale = 100


def get_color(color, package, args):
    tree = ET.parse(
        args.extract + package.graphic.name)

    currentColor = "rgb(0, 0, 0)"

    for i in tree.getroot().iter("Color"):
        if i.attrib["Self"] == color:
            colorValue = i.attrib["ColorValue"].split(" ")
            currentColor = "rgb" + str(cmyk_to_rgb(
                float(colorValue[0]), float(colorValue[1]), float(colorValue[2]), float(colorValue[3])))

    return "color:" + currentColor


def cmyk_to_rgb(c, m, y, k):
    r = rgb_scale*(1.0-(c+k)/float(cmyk_scale))
    g = rgb_scale*(1.0-(m+k)/float(cmyk_scale))
    b = rgb_scale*(1.0-(y+k)/float(cmyk_scale))
    return r, g, b


def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy)
    m = (m - min_cmy)
    y = (y - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale
