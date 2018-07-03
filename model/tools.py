import os
import json
import xml.etree.ElementTree as ET


def init():
    path = os.path.dirname(__file__)
    xml_path = os.path.join(path, 'base.xml')
    tree = ET.parse(xml_path)
    return tree.getroot()


def base_dict():
    ds = {}
    root = init()
    for child in root:
        if child.tag == 'class':
            obj_key = child.attrib['acronym']
            obj_value = {}
            for son in child:
                if son.tag == 'attributes':
                    for sson in son:
                        attr_key = sson.attrib['acronym']
                        attr_value = {}
                        for ssson in sson:
                            if ssson.tag == 'enums':
                                values = []
                                for xx in ssson:
                                    enum_dict = {}
                                    for x in xx:
                                        enum_dict.setdefault(x.tag, x.text)
                                        values.append(enum_dict)
                                attr_value.setdefault(ssson.tag, values)
                            else:
                                attr_value.setdefault(ssson.tag, ssson.text)
                        obj_value.setdefault(attr_key, attr_value)
                elif son.tag == 'languages':
                    languages_key = son.tag
                    languages = {}
                    for sson in son:
                        attr_key = sson.attrib['acronym']
                        attr_value = {}
                        for ssson in sson:
                            attr_value.setdefault(ssson.tag, ssson.text)
                        languages.setdefault(attr_key, attr_value)
                    obj_value.setdefault(languages_key, languages)
                else:
                    obj_value.setdefault(son.tag, son.text)
            ds.setdefault(obj_key, obj_value)
    return ds


def db_config():
    path = os.path.dirname(__file__)
    db_path = os.path.join(path, 'database.json')
    try:
        with open(db_path, "r") as f:
            d = json.load(f)
    except OSError:
        d = {}
    return d


d = base_dict()


def obj_dict():
    return list(base_dict().values())[0]


d = obj_dict()
print(d)


print(d.keys())
