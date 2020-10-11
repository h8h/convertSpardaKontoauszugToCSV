import csv

class homebank(object):
    #
    # Konvertiert in eine HOMEBANK konforme CSV-Datei
    #
    transactions = []

    def __init__(self, transactions):
        self.transactions = transactions


    def write(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';',
                         quotechar='"', quoting=csv.QUOTE_MINIMAL)


            for transaction in self.transactions:
                csvwriter.writerow([
                    transaction["Date"],
                    "",
                    "",
                    transaction["Payee"],
                    transaction["Memo"],
                    transaction["Umsatz"],
                    "",
                    "" ])

