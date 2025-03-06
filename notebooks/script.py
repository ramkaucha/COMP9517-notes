import json
import re
import sys
import os

def extract_outlien(ipynb_file, output_file=None):
    if output_file is None:
        output_file = os.path.splitext(ipynb_file)[0] + '_outline.txt'

    try:
        with open(ipynb_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

            markdown_cells = [cell for cell in notebook.get('cells', [])
                            if cell.get('cell_type') == 'markdown']

            header_pattern = re.compile(r'^(#{1,6})\s+(.*?)$', re.MULTILINE)

            outline = []
            for cell in markdown_cells:
                source = ''.join(cell.get('source', []))
                headers = header_pattern.findall(source)

                for level, text in headers:
                    indent = '    ' *  (len(level) - 1)
                    outline.append(f"{indent}{text.strip()}")


        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(outline))

        return output_file
    except Exception as e:
        print(f"{e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("<notebook> [output.txt]")
        return

    ipynb_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = extract_outlien(ipynb_file, output_file)

    if result:
        print(f"Successful")


if __name__ == "__main__":
    main()

