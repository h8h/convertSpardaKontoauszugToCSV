import re


class spardaKontoauszugAlt(list):
    ###
    ### Liste mit Kontoauszuegen
    ### der alten Sparda Version
    ### < 11/2019
    ###

    # Mit dieser Regex werden die Transaktionen zerlegt.
    # Es hat sich bewaehrt nach Datumangaben zu suchen
    # xx.xx.xxxx
    splitTransactionRegex = re.compile(r"[0-3][0-9]\.[0-1][0-9]\.[1-9][0-9][1-9][0-9]")
    
    # Hier wird eine Dezimalzahl gesucht
    # -xx,xx
    # xx,xx
    # xxx.xxx,xx
    # -xxx.xxx,xx
    betragRegex = re.compile(r"^[0-9\.\-]+,[0-9][0-9]")

    # Beim Seitenumbruch wird der Text Übertrag hinzugefuegt.
    # Dieser wird bis zum Zeilenende entfernt
    uebertragRegex = re.compile(r"\sÜbertrag.*?$")

    # So wie oben
    # Zusaetzlich wird noch ermittelt welche Version des Kontoauszug es ist
    kontostandRegex = re.compile(r"Kontostand\sneu\sam")

    # Hier wird eine Transaktion in einen Zahlungsempfaenger und in Buchungstext getrennt
    # Bei diesem wird erwartet das in der Buchung folgender Text auftaucht
    # xxxxxx xx.xx.xxxx xx.xx.xx
    # Der erste Part ist dann der Zahlungsempfaenger
    # Der zweite Part (ab dem ersten Leerzeichen) ist Datum + Uhrzeit und bezieht sich auf den Buchungstext
    matchpayeememoRegex = re.compile(r"(.+)([0-3][0-9]\.[0-1][0-9]\.[1-9][0-9][1-9][0-9]\s[0-2][0-9]\.[0-5][0-9]\.[0-5][0-9].+)")

    # Ueberschriften die rausgeloescht werden
    headerRegex = re.compile(r"00.00 Uhr bis|24.00 UhrSeite")

    def __getPayeeMemo__(self, text):
        # Die Methode versucht den Text in Zahlungsempfaenger und in Buchungstext 
        # aufzuteilen

        payee, memo = "", ""
        sepa = text.split('SEPA', 1)
        if len(sepa) > 1:
           # Alle Ueberweisungen fangen mit SEPA an
           return sepa[0].rstrip(), f"SEPA{sepa[1]}"
        else:
           # Wenn das nicht funkzt dann wird es wohl
           # eine Barabhebung sein, somit wird das 
           # Format Datum + Uhrzeit (siehe oben) erwartet
           match = re.match(self.matchpayeememoRegex, text)
           if match != None and match.lastindex == 2:
               return match.group(1), match.group(2)
           else:
               # Auch schon gesehen, das mit : getrennt wird
               column = text.split(':', 1)
               if len(column) == 2 :
                   return column

        # Falls wir aus dem Text nicht schlau werden
        # ist der Zahlungsempfaenger Unbekannt und 
        # muss manuell aus dem Text herausgeparst 
        # werden
        return "Unbekannt", text

    def __init__(self, text):

        list.__init__([])
        self.text = text


    def parse(self):
        if not re.search(self.kontostandRegex, self.text):
            # Der Kontoauszug hat eine falsche Version
            return False

        lastmatch = -1
        transactionText = ""

        for match in re.finditer(self.splitTransactionRegex, self.text):
            # Wir hangeln uns von Datum zu Datum xx.xx.xxxx
            if lastmatch >= 0:
                #Von letztem Datum bis kurz vor neuem Datum
                currentText = self.text[lastmatch:match.start()]

                if re.search(self.betragRegex, currentText[10:]):
                    # Haben wir ein Datum, wird nun der Betrag gesucht
                    # Erwartung:
                    # xx.xx.xxxxEUR
                    # 01.01.202013,12
                    
                    # Der Betrag entspricht den aktuellen Pointer der Schleife
                    # von diesem werden noch Textreste entfernt
                    umsatz = re.sub(self.uebertragRegex, '' , currentText[10:])
                    umsatz = re.sub(self.kontostandRegex, '', umsatz)
                    umsatz = umsatz.rstrip()

                    # Das Datum muesste an den ersten 10 Zeichen stehen
                    date = transactionText[:10]

                    # Der Buchungstext ab den 10ten Zeichen bis zum Schluss
                    payee, memo = self.__getPayeeMemo__(transactionText[10:])


                    self.append({"Date": date,"Payee": payee, "Memo": memo,"Umsatz": umsatz})
                    transactionText = ""
                else:
                    # wurde kein Betrag gefunden
                    # dann wird der Buchungstext zum vorherigen hinzugefuegt
                    if not re.search(self.headerRegex, currentText):
                        # Hier werden Text und Fusszeilen uebersprungen
                        # und nur das zum Buchungstext hinzugefuegt
                        # was dazugehoert
                        transactionText += currentText

            lastmatch = match.start()

        # Erste und letzter Eintrag erhaelt Salden
        del self[0]
        del self[-1]

        return True

class spardaKontoauszugNeu(list):
    ###
    ### Liste mit Kontoauszuegen
    ### der neuen Sparda Version
    ### >= 11/2019
    ###

    # Es fehlen leider die Jahresangaben bei den Buchungen. Daher wird einmal das aktuelle Jahr ermittelt
    currentYearRegex = re.compile(r"neuer\sKontostand\svom\s[0-3][0-9]\.[0-1][0-9]\.([1-9][0-9][0-9][0-9])")

    # Mit dieser Regex werden die Transaktionen zerlegt.
    # Es hat sich bewaehrt nach folgenden Datumangaben zu suchen
    # xx.xx. xx.xx.
    # 01.01. 01.01.
    splitTransactionRegex = re.compile(r'[0-3][0-9]\.[0-1][0-9]\.\s[0-3][0-9]\.[0-1][0-9]\.')

    # Hier wird dann die gefundene Transaktion zerlegt.
    # Nach folgenden Format
    # xx.xx. xx.xx. xxxxxxxxxxx xx,xx X
    # xx.xx. xx.xx. xxxxxxxxxxx -xx,xx X
    # 01.01. 01.01. buchungstext 13,37 S
    # 01.01. 01.01. buchungstext 13,37 H
    transactionRegex = re.compile("^([0-3][0-9]\.[0-1][0-9])\.\s([0-3][0-9]\.[0-1][0-9])\.\s+(.+)\s+([0-9\.,]+)\s([S|H])\s+(.+)$")

    # Ausserdem wird dies benoetigt um die neue Version der Kontostaende zu detektieren 
    kontostandRegex = re.compile(r'neuer\sKontostand')

    # Beim Seitenumbruch wird der Text Uebertrag hinzugefuegt.
    # Dieser wird bis zum Zeilenende entfernt
    uebertragRegex = re.compile(r"Übertrag.*?$")

    # Textueberbleibsel
    kontostandperRegex = re.compile(r"\s*Kontostand per.*")

    def __getPayeeMemo__(self, text):
        # Die Methode versucht den Text in Zahlungsempfaenger und in Buchungstext 
        # aufzuteilen
        payee, memo, cnt = [], [], 0
        for part in text.split(' '):
            if cnt <= 2:
                if part == "":
                    cnt += 1
                else:
                    payee.append(part)
            else:
                if part != "":
                    memo.append(part)

        return " ".join(payee), " ".join(memo)


    def __init__(self, text):
 
        list.__init__([])
        self.text = text


    def parse(self):
        if not re.search(self.kontostandRegex, self.text):
            # Der Kontoauszug hat eine falsche Version
            return False


        # Ermittlung des Jahres auf den sich der Kontoauszug bezieht
        currentYearMatch = re.search(self.currentYearRegex, self.text)
        if currentYearMatch == None:
            return

        currentYear = currentYearMatch.group(1)

        lastmatch = -1
        raw_transactions = []
        for match in re.finditer(self.splitTransactionRegex, self.text):
            if lastmatch >= 0:
                raw_transactions.append(self.text[lastmatch:match.start()])

            lastmatch = match.start()

        # die letzte Transaction bis zum Stichwort neuer Kontostand
        lasttransaction = self.text[lastmatch:]
        theend = re.search(self.kontostandRegex, lasttransaction)

        if not theend:
            print("Error processing ... Sentence not found 'neuer Kontostand'")
            return

        raw_transactions.append(lasttransaction[:theend.start()])

        for transaction in raw_transactions:
            # Uebertrage mit Salden ignorieren
            trans = re.sub(self.uebertragRegex, '', transaction)
            trans = re.sub(self.kontostandperRegex, '', trans)

            # Hier wird nun die einzelne Transaktion aufgeteilt
            # 1 - Datum 1 BuTag
            # 2 - Datum 2 Wertstellungstag
            # 3 - Luecke
            # 4 - Umsatz 
            # 5 - Soll / Haben
            # 6 - Buchungstext
            expense = re.match(self.transactionRegex, trans)
            if expense == None or expense.lastindex < 6:
                continue

            # Simple Datumsumwandlung von Punkt zu Minus 
            date = f"{expense.group(1).replace('.','-')}-{currentYear}"

            payee, memo = self.__getPayeeMemo__(expense.group(6))
 
            # Je nachdem ob Soll oder Haben Minus hinzufuegen
            umsatz = 0
            if expense.group(5) == "S":
                umsatz = f"-{expense.group(4)}"
            elif expense.group(5) == "H":
                umsatz = expense.group(4)

            self.append({"Date": date,"Payee": payee, "Memo": memo,"Umsatz": umsatz})

        return True
