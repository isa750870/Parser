import sys
import xml.etree.ElementTree as ET
import re

COMMENT_BLOCK = r"{{!--(.*?)--}}"
ARRAY = r"\(\s*(.*?)\s*\)"
STRING = r'@"(.*?)"'
NUMBER = r"\b\d+\b"
CONST_DECLARATION = r"var\s+([a-zA-Z]+)\s*=\s*(.*?);"
CONST_EVALUATION = r"\!\[([a-zA-Z]+)\]"

constants = {}

def parse_xml(input_xml):
    xml_root = ET.fromstring(input_xml)
    output_lines = []

    for elem in xml_root:
        if elem.tag == "comment":
            comment_text = elem.text.strip()
            comment_lines = comment_text.splitlines()
            output_lines.append("{{!--")
            for line in comment_lines:
                output_lines.append(f"    {line.strip()}")
            output_lines.append("--}}")
        elif elem.tag == "constant":
            name = elem.attrib["name"]
            value = elem.text.strip()
            output_lines.append(f"var {name} = {value}")
        elif elem.tag == "array":
            name = elem.attrib["name"]
            values = [item.text for item in elem.findall("item")]
            output_lines.append(f"var {name} = ({', '.join(values)})")
        elif elem.tag == "evaluation":
            name = elem.attrib["name"]
            value = elem.text.strip()
            output_lines.append(f"![{name}]")
        else:
            output_lines.append(f"Неправильный синтаксис: {elem.tag}")

    return "\n".join(output_lines)

def convert_xml_to_custom_language(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_xml = file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file_path}' не найден.")
        sys.exit(1)

    try:
        output_text = parse_xml(input_xml)
        output_text = re.sub(r'\"(.*?)\"', r'@"\1"', output_text)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)
        print(f"Вывод успешно сохранён в {output_file_path}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Использование: python config_converter.py <input_xml_file> <output_config_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    convert_xml_to_custom_language(input_file_path, output_file_path)

if __name__ == "__main__":
    main()