import os
import xml.etree.ElementTree as ET


def init():
    PATH = os.path.dirname(__file__)
    XML_PATH = os.path.join(PATH, 'base.xml')
    tree = ET.parse(XML_PATH)
    return tree.getroot()


def get_class_name():
    root = init()
    class_name = root[0].attrib['name']
    return class_name


def class_display(class_name):
    root = init()
    for child in root:
        if child.tag != 'class':
            continue
        if child.attrib['name'] != class_name:
            continue
        for son in child:
            if son.tag == 'display_name':
                return son.text
    return None


# print(class_display('objnam'))


def attribute_display(class_name, attribute_name):
    root = init()
    for child in root:
        if child.tag != 'class':
            continue
        if child.attrib['name'] != class_name:
            continue
        for son in child:
            if son.tag != 'attributes':
                continue
            for subson in son:
                if subson.attrib['name'] != attribute_name:
                    continue
                for ssubson in subson:
                    if ssubson.tag == 'display_name':
                        return ssubson.text

    return None


# print(attribute_display(get_class_name(), 'level'))


def objl_type():
    root = init()
    d = {}
    class_name = get_class_name()
    for child in root:
        if child.tag != "class" or child.attrib['name'] != class_name:
            continue
        for son in child:
            if son.tag != "attributes":
                continue
            for subson in son:
                if subson.attrib['name'] != 'objl':
                    continue
                for ssubson in subson:
                    if ssubson.tag != 'enums':
                        continue
                    for x in ssubson:
                        d[int(x[0].text)] = x[1].text
    return d


# print(objl_type())


def all_languages():
    root = init()
    d = {}
    class_name = get_class_name()
    for child in root:
        if child.tag != "class" or child.attrib['name'] != class_name:
            continue
        for son in child:
            if son.tag != 'languages':
                continue
            for sson in son:
                d[str(sson.attrib['country'])] = sson[0].text
    return d


# print(all_languages())
