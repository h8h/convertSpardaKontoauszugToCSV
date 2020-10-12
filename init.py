#!/usr/bin/env python3
from pdfminer.high_level import extract_text
from lib.spardaKontoauszug import spardaKontoauszugAlt, spardaKontoauszugNeu
from lib.homebank import homebank
import sys

transactions = []
for filename in sys.argv[1:]:
    extractedText = extract_text(filename)
    kontoauszug = spardaKontoauszugNeu(extractedText)
    if kontoauszug.parse():
        transactions += kontoauszug
    else:
        kontoauszug = spardaKontoauszugAlt(extractedText)
        if kontoauszug.parse():
            transactions += kontoauszug
        else:
            print (f"Error parsing file: {filename}")
            print (extractedText)

homebank = homebank(transactions)
homebank.write("homebank.csv")
