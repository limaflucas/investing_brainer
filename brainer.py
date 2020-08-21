from bs4 import BeautifulSoup

import requester
import csv


def __populate_brain(ticker, exclude=['Oscilações', 'Indicadores fundamentalistas', 'Dados Balanço Patrimonial', 'Dados demonstrativos de resultados', 'Últimos 12 meses', 'Últimos 3 meses', '']):

    print('Retrieving ticker ' + ticker + ' data...')

    base_url = 'http://www.fundamentus.com.br/detalhes.php?papel='
    page = requester.get_content(base_url + ticker)
    data = {}
    header = ''
    for e in BeautifulSoup(page, 'html.parser').select('table.w728 tr td'):
        content = e.contents[-1].text.strip()
        if content in exclude:
            header = ''
            continue

        if not header:
            header = content
        elif header:
            data[header] = content
            header = ''

    return data


def __to_csv(header, data, filename):
    print('Writing data out')
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for d in data:
            row = []
            for h in header:
                row.append(d[h] if h in d.keys() else '-')
            writer.writerow(row)


def __extract_headers(data):
    headers = set()
    for d in data:
        for h in set(d.keys()) - headers:
            headers.add(h)

    return headers


def brainer():

    page = requester.get_content('http://www.fundamentus.com.br/detalhes.php')
    souped = BeautifulSoup(page, 'html.parser')

    tickers = []
    for s in souped.find(id='test1').select('tr td a'):
        tickers.append(s.text.strip())

    print('Found ' + str(len(tickers)) + ' tickers')

    brain = []
    for t in tickers:
        brain.append(__populate_brain(t))

    __to_csv(__extract_headers(brain), brain, 'assets.csv')


if __name__ == '__main__':
    brainer()
