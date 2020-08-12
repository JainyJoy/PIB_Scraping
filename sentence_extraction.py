import requests
import pandas as pd
import json
import os
import winsound
import re

def tokenize_eng_file(mainString):
    sentences = []
    e = '((?<=[^A-Z])\. +(?=[^a-z0-9 ])|\n|\*|\([MDCLXVImdclxvi]+\)|^[0-9]+\.[^0-9])'
    mainString = mainString.replace('.','. ')
    mainString = mainString.replace('Prof. ','Prof.')
    mainString = mainString.replace('Dr. ','Dr.')
    mainString = mainString.replace('Mr. ','Mr.')
    mainString = mainString.replace('Mrs. ','Mrs.')
    mainString = mainString.replace('Ms. ','Ms.')
    mainString = mainString.replace('viz. ','viz.')
    mainString = mainString.replace('Hon. ','Hon.')
    mainString = mainString.replace('i.e. ','i.e.')
    mainString = mainString.replace('Smt. ','Smt.')
    mainString = mainString.replace('Shri. ','Shri.')
    splitString = re.split(e,mainString)
    # print(splitString)
    for i,s in enumerate(splitString):
        if(s.strip() == ''):
            continue
        if(s == '\n'):
            continue
        if(re.search('\([MDCLXVImdclxvi]+\)$',s) is not None):
            splitString[i+1] = s + splitString[i+1]
            continue
        if(re.search('\. +$',s) is not None):
            sentences[-1] += s[0]
            # splitString[i+1] = s[2] + splitString[i+1]
            continue
        if(re.search('^[0-9]+\.[^0-9]',s) is not None):
            continue
        if('*' in s):
            break
        sentences.append(s.strip())
    return sentences

def tokenize_hi_file(mainHinString):
    e = '(। +|\n|\*|\([MDCLXVImdclxvi]+\)|[0-9]+\.[^0-9])'
    sentences = []
    splitString = re.split(e,mainHinString)
    for i,s in enumerate(splitString):
        if(s.strip() == ''):
            continue
        if(s == '\n'):
            continue
        if(re.search('\([MDCLXVImdclxvi]+\)$',s) is not None):
            splitString[i+1] = s + splitString[i+1]
            continue
        if(re.search('। +$',s) is not None):
            sentences[-1] += s[0]
            continue
        if('*' in s):
            break
        sentences.append(s.strip())
    return sentences


def tokenize_file(month,year):
    # month = 'February'
    file_base_path = "C:\\Users\\Dhanvi\\PIB_Scraping-3\\"
    file_tokenized_path = "C:\\Users\\Dhanvi\\PIB_Scraping-3\\"+year+"\\"+month+"\\Tokenized-Mine\\"
    df = pd.read_csv("C:\\Users\\Dhanvi\\PIB_Scraping-3\\"+month+"-"+year+"-Parallel-Hindi.csv")

    total_en_sentences = []
    total_hi_sentences = []

    base_url = "https://www.pib.gov.in/PressReleasePage.aspx?PRID="

    header_en = ["English_Sentences","File No"]
    header_hi = ["Hindi_Sentences","File No"]

    for i in range(len(df)):
            print('Handling file with id ',i)
            en = df['English_Filename'][i]
            hi = df['Hindi_Filename'][i]
            print(en)
            file_en_path = file_tokenized_path+en.split("\\")[-1]
            file_hi_path = file_tokenized_path+hi.split("\\")[-1]
            with open(file_base_path+en,'r',encoding='utf-8') as file_en:
                sentences = tokenize_eng_file(file_en.read())
                with open(file_en_path,'w',encoding='utf-16') as file_en_w:
                    for s in sentences:
                        if(len(s.split()) <= 4 or 'Posted On:' in s):
                            continue
                        file_en_w.write(s+"\n")
                        total_en_sentences.append([s,i])
            with open(file_base_path+hi,'r',encoding='utf-8') as file_hi:
                sentences = tokenize_hi_file(file_hi.read())
                with open(file_hi_path,'w',encoding='utf-16') as file_hi_w:
                    for s in sentences:
                        if(len(s.split()) <=4 or 'Posted On:' in s):
                            continue
                        file_hi_w.write(s+"\n")
                        total_hi_sentences.append([s,i])

    csv_path = os.getcwd()+"\\CSV_Files\\"+month+"-2020"
    df_en = pd.DataFrame(total_en_sentences)
    df_en.to_csv(csv_path+'-Total-English-Sentences.csv',header=header_en,index=False)

    df_hi = pd.DataFrame(total_hi_sentences)
    df_hi.to_csv(csv_path+'-Total-Hindi-Sentences.csv',header=header_hi,index=False)

    winsound.Beep(2500,1000)


if __name__ == "__main__":
    tokenize_file('February')
