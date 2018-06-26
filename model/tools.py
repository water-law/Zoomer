import os
import xml.etree.ElementTree as ET
PATH = os.path.dirname(__file__)
XML_PATH = os.path.join(PATH, 'data.xml')
tree = ET.parse(XML_PATH)
root = tree.getroot()


def class_display(class_name):
    for child in root:
        if child.tag != 'class':
            continue
        if child.attrib['name'] != class_name:
            continue
        for son in child:
            if son.tag == 'display_name':
                return son.text
    return None


print(class_display('objnam'))


def attribute_display(class_name, attribute_name):
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


print(attribute_display('objnam', 'level'))


def objl_type():
    d = {}
    for child in root:
        if child.tag != "class" or child.attrib['name'] != 'objnam':
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


print(objl_type())


def all_languages():
    d = {}
    for child in root:
        if child.tag != "class" or child.attrib['name'] != 'objnam':
            continue
        for son in child:
            if son.tag != 'languages':
                continue
            for sson in son:
                d[str(sson.attrib['country'])] = sson[0].text
    return d


print(all_languages())
