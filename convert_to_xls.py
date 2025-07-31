import re
import sys
import pandas as pd


BUSINESS_REGEX = re.compile(
    r"Business:\s*(?P<business>.+?)\n"
    r"Name:\s*(?P<name>.+?)\n"
    r"Address:\s*(?P<address>.+?)\n"
    r"Phone:\s*(?P<phone>.+?)\n"
    r"Industry:\s*(?P<industry>.+?)\n"
    r"Amount:\s*\$?(?P<amount>[0-9,\.]+)",
    re.IGNORECASE | re.MULTILINE,
)


def parse_text(text):
    rows = []
    for match in BUSINESS_REGEX.finditer(text):
        rows.append(match.groupdict())
    return rows


def main(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    rows = parse_text(text)
    if not rows:
        print("No business entries found.")
    df = pd.DataFrame(rows, columns=['business', 'name', 'address', 'phone', 'industry', 'amount'])
    df.to_excel(output_path, index=False)
    print(f"Wrote {len(df)} rows to {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python convert_to_xls.py input.txt output.xlsx')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
