import csv

csv_reader = csv.reader(open('languages.csv', encoding='utf-8'))

with open("lang.xml", "w") as f:
    for row in csv_reader:
        data = row[0].split('\t')
        content = """
        <language country="{}">
              <name>{}</name>
              <code>{}</code>
            </language>
        """.format(data[0], data[1], data[2])
        f.writelines(content)

