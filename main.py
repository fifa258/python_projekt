import os
import sys
import csv
import json
import matplotlib

from datetime import datetime

from rich.console import Console
from rich.table import Table

console = Console()


def file_reader(filename):
    dochazka = []

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            dochazka.append(row)

    return dochazka


def file_printer(dochazka):
    table = Table(title="Docházka zaměstnanců")
    table.add_column("Číslo čipu", justify="right")
    table.add_column("Zaměstnanec", justify="left")
    table.add_column("Příchod", justify="right")
    table.add_column("Odchod", justify="right")

    for zaznam in dochazka:
        table.add_row(
            zaznam["číslo čipu"],
            zaznam["zaměstnanec"],
            zaznam["příchod"],
            zaznam["odchod"],
        )

    console.print(table)


def nejkratsi_a_nejdelsi_smena(dochazka):
    if not dochazka:
        console.print("Žádná data k analýze.")
        return

    seznam_smen = []

    for zaznam in dochazka:
        prichod = datetime.strptime(zaznam["příchod"], "%Y-%m-%d %H:%M")
        odchod = datetime.strptime(zaznam["odchod"], "%Y-%m-%d %H:%M")

        smena = odchod - prichod

        seznam_smen.append({
            "zaměstnanec": zaznam["zaměstnanec"],
            "délka": smena
        })

    nejkratsi = seznam_smen[0]
    nejdelsi = seznam_smen[0]

    for zaznam in seznam_smen:
        if zaznam["délka"] < nejkratsi["délka"]:
            nejkratsi = zaznam
        if zaznam["délka"] > nejdelsi["délka"]:
            nejdelsi = zaznam

    console.print()
    console.rule("Statistika směn")
    console.print(f"Nejkratší směna: {nejkratsi['zaměstnanec']} ({nejkratsi['délka']})")
    console.print(f"Nejdelší směna: {nejdelsi['zaměstnanec']} ({nejdelsi['délka']})")
    console.rule()


def ziskej_delku(zaznam):
    return zaznam["délka"]


def serazene_smeny(dochazka):
    if not dochazka:
        console.print("Žádná data k analýze.")
        return

    seznam_smen = []

    for zaznam in dochazka:
        prichod = datetime.strptime(zaznam["příchod"], "%Y-%m-%d %H:%M")
        odchod = datetime.strptime(zaznam["odchod"], "%Y-%m-%d %H:%M")

        smena = odchod - prichod

        seznam_smen.append({
            "zaměstnanec": zaznam["zaměstnanec"],
            "příchod": zaznam["příchod"],
            "odchod": zaznam["odchod"],
            "délka": smena
        })

    seznam_smen.sort(key=ziskej_delku)

    table = Table(title="Seřazené směny podle délky")
    table.add_column("Zaměstnanec", justify="left")
    table.add_column("Příchod", justify="right")
    table.add_column("Odchod", justify="right")
    table.add_column("Délka", justify="right")

    for zaznam in seznam_smen:
        table.add_row(
            zaznam["zaměstnanec"],
            zaznam["příchod"],
            zaznam["odchod"],
            str(zaznam["délka"]),
        )

    console.print(table)


def menu():
    console.print()
    console.rule()
    console.print(" ANALYZA DOCHAZKY", justify="center")
    console.rule()
    console.print()

    console.print("1 - zobrazit vsechny zaznamy")
    console.print("2 - ulozit jako json")
    console.print("3 - nejkratší a nejdelší směna")
    console.print("4 - seřadit směny podle délky")
    console.print("0 - ukonceni programu")


def main():
    dochazka = file_reader("dochazka.csv")

    while True:
        menu()
        volba = input("\nVolba: ").strip()
        if volba == "1":
            file_printer(dochazka)
        elif volba == "2":
            pass
        elif volba == "3":
            nejkratsi_a_nejdelsi_smena(dochazka)
        elif volba == "4":
            serazene_smeny(dochazka)
        elif volba == "0":
            break


if __name__ == "__main__":
    main()