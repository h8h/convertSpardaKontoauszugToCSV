#!/usr/bin/env python3
from pdfminer.high_level import extract_text
from lib.spardaKontoauszug import spardaKontoauszugAlt, spardaKontoauszugNeu
from lib.homebank import homebank
import sys
from subprocess import Popen, PIPE


transactions = []
for filename in sys.argv[1:]:
    extractedText = extract_text(filename)
    kontoauszug = spardaKontoauszugNeu(extractedText)
    if kontoauszug.parse():
        transactions += kontoauszug
    else:
        # pdfminer extrahiert keine CR, somit nutzen wir fuer die alten Kontoausz.
        # ein anderes Programm
        #with Popen(["/usr/bin/pdftotext", filename, "-"], stdout=PIPE) as proc:
        #    extractedText = proc.stdout.read().decode('UTF-8')

        #if extractedText == None:
        #    print(f"Error while reading {filename}")
        #    continue

        kontoauszug = spardaKontoauszugAlt(extractedText)
        if kontoauszug.parse():
            transactions += kontoauszug
        else:
            print (f"Error parsing file: {filename}")
            print (extractedText)

homebank = homebank(transactions)
homebank.write("homebank.csv")
