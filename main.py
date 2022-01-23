import pandas as pd
import lxml
import requests


def first_index(s):
    characters = "(abcdefghijklmnopqrstuvwxyzō"
    i = []
    for c in characters:
        try:
            if c is "(":
                if s[s.index(c)+1] not in characters:
                    pass
            i.append(s.index(c))
        except ValueError:
            pass
    if not i:
        print(s)
    if len(i) is 0:
        print(s)
    return min(i)


def download_kanji():
    page = requests.get("https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji")
    table = pd.read_html(page.text.replace('<br>', ' :: '))
    table = table[1]
    table = table.drop(columns=["#", "Old (Kyūjitai)", "Radical", "Strokes", "Year added"])
    # table.to_csv(path_or_buf="kanji.csv", index=False)
    table.loc[table['Grade'] == "1"].to_csv(path_or_buf="public/kanjiGrade1.csv", index=False)
    table.loc[table['Grade'] == "2"].to_csv(path_or_buf="public/kanjiGrade2.csv", index=False)
    table.loc[table['Grade'] == "3"].to_csv(path_or_buf="public/kanjiGrade3.csv", index=False)
    table.loc[table['Grade'] == "4"].to_csv(path_or_buf="public/kanjiGrade4.csv", index=False)
    table.loc[table['Grade'] == "5"].to_csv(path_or_buf="public/kanjiGrade5.csv", index=False)
    table.loc[table['Grade'] == "6"].to_csv(path_or_buf="public/kanjiGrade6.csv", index=False)
    table.loc[table['Grade'] == "S"].to_csv(path_or_buf="public/kanjiGradeS.csv", index=False)


def download_hira():
    page = requests.get("https://simple.wikipedia.org/wiki/Hiragana")
    table = pd.read_html(page.text)
    table = table[0].fillna("")
    table = table.drop(index=0)
    table = table.drop(index=2)
    table = table.drop(index=13)
    table = table.reset_index(drop=True)
    table.to_csv(path_or_buf="public/Hiragana.csv", index=False)


def download_kata():
    page = requests.get("https://simple.wikipedia.org/wiki/Katakana")
    table = pd.read_html(page.text)
    table = table[0].fillna("")
    table = table.drop(index=0)
    table = table.drop(index=18)
    table = table.drop(index=2)
    table = table.reset_index(drop=True)
    table.to_csv(path_or_buf="public/Katakana.csv", index=False)


def fix_hira():
    table = pd.read_csv("public/Hiragana.csv").fillna("")
    hiras = []
    hiraTable = pd.DataFrame(columns=["Hiragana", "Readings"])
    for index, row in table.iterrows():
        values = [value for value in row.values if value != ""]
        for value in values:
            hiras.append(value)
            tableValue = {"Hiragana": value[0:first_index(value)],
                          "Readings": value[first_index(value):len(value)]}
            hiraTable = hiraTable.append(tableValue, ignore_index=True)
    hiraTable["Hiragana"] = hiraTable["Hiragana"].str.strip()
    hiraTable["Readings"] = hiraTable["Readings"].str.strip()
    hiraTable["Readings"] = hiraTable["Readings"].str.replace(",", "、 ")
    hiraTable = hiraTable.drop(index=5)
    hiraTable = hiraTable.drop(index=6)
    hiraTable = hiraTable.drop(index=7)
    hiraTable = hiraTable.reset_index(drop=True)
    hiraTable.to_csv("public/Hiragana.csv", index=False)


def fix_kata():
    table = pd.read_csv("public/Katakana.csv").fillna("")
    hiras = []
    hiraTable = pd.DataFrame(columns=["Katakana", "Readings"])
    for index, row in table.iterrows():
        values = [value for value in row.values if value != ""]
        for value in values:
            hiras.append(value)
            tableValue = {"Katakana": value[0:first_index(value)],
                          "Readings": value[first_index(value):len(value)]}
            hiraTable = hiraTable.append(tableValue, ignore_index=True)
    hiraTable["Katakana"] = hiraTable["Katakana"].str.strip()
    hiraTable["Readings"] = hiraTable["Readings"].str.strip()
    hiraTable["Readings"] = hiraTable["Readings"].str.replace(",", "、 ")
    hiraTable.to_csv("public/Katakana.csv", index=False)


def fix_kanji_readings(filename):
    table = pd.read_csv(filename)
    table["Readings"] = table["Readings"].str.replace(" ", "")
    table["Readings"] = table["Readings"].str.replace(",", " ")
    table["Readings"] = table["Readings"].str.replace("、", " ")
    index = 0
    for row in table["Readings"]:
        sample = first_index(row)
        hiraRow = row[0:sample].split(" ")
        romaRow = row[sample:len(row)].split(" ")

        newRow = []

        for hira, roma in zip(hiraRow, romaRow):
            newRow.append(hira + " " + roma)
        table.loc[index, "Readings"] = "、 ".join(newRow)
        index += 1
    index = 0
    for index, row in table.iterrows():
        meanings = row["English meaning"]
        table.loc[index, "English meaning"] = "、 ".join(meanings.split(", "))
    # for row in table["English meaning"]:
    #     sample = row.split(", ")
    #     table.loc[index, "English meaning"] = "、 ".join(row)

    table.to_csv(path_or_buf=filename, index=False)


def remove_r(filename):
    table = pd.read_csv(filename)
    with open(filename, mode='w', newline='\n', encoding="utf-8") as f:
        table.to_csv(f, sep=",", index=False, line_terminator='\n')


def fix_kanji():
    fix_kanji_readings("public/kanjiGrade1.csv")
    fix_kanji_readings("public/kanjiGrade2.csv")
    fix_kanji_readings("public/kanjiGrade3.csv")
    fix_kanji_readings("public/kanjiGrade4.csv")
    fix_kanji_readings("public/kanjiGrade5.csv")
    fix_kanji_readings("public/kanjiGrade6.csv")
    fix_kanji_readings("public/kanjiGradeS.csv")


download_kanji()
download_hira()
download_kata()
fix_hira()
fix_kata()
fix_kanji()
