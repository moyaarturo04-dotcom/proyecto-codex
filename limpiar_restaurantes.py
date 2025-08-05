import csv
import zipfile
import xml.etree.ElementTree as ET

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

class SimpleDataFrame:
    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

    def head(self, n=5):
        preview = []
        for row in self.rows[:n]:
            row_extended = row + [''] * (len(self.headers) - len(row))
            preview.append(dict(zip(self.headers, row_extended)))
        return preview

    def to_csv(self, path, index=False):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)
            writer.writerows(self.rows)

def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            sroot = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in sroot.findall(f'{NS}si'):
                t = si.find(f'{NS}t')
                if t is None:
                    r = si.find(f'{NS}r')
                    if r is not None:
                        t = r.find(f'{NS}t')
                shared_strings.append(t.text if t is not None else '')
        sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        rows = []
        for row in sheet.findall(f'.//{NS}row'):
            row_data = []
            for c in row.findall(f'{NS}c'):
                t = c.get('t')
                v = c.find(f'{NS}v')
                value = ''
                if v is not None:
                    text = v.text
                    if t == 's':
                        if text.isdigit() and int(text) < len(shared_strings):
                            value = shared_strings[int(text)]
                        else:
                            value = ''
                    else:
                        value = text
                row_data.append(value)
            rows.append(row_data)
    headers = rows[0] if rows else []
    data_rows = rows[1:] if rows else []
    return SimpleDataFrame(headers, data_rows)

def main():
    df = read_xlsx('restaurantes_sucio.xlsx')
    print(df.head())
    df.to_csv('restaurantes_limpio.csv', index=False)

if __name__ == '__main__':
    main()
