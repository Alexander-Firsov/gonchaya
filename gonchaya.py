#!/bin/python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import hashlib
import sys                      # для разбора параметров командной строки
from IPython.display import display, Markdown # Для вывода форматированного текста
import traceback
import math
import re
import requests
import html


#   *** Классическая предобработка данных ***
class PadlasException(Exception):
    pass

def preparing_string_for_column_names(string:str):
    '''
    Подготовка строк для названий столбцов.
    Данная функция работает со строками:
      1) Проводит замену нежелательных символов:
         пробел на '_'
         табуляцию на '_tab_'
         '.' на '_dot_'
         ':' на '_colon_'
      2) переводит верблюжий стиль в змеиный;
      3) переводит названия в нижний регистр;
      4) удаляет начальные и конечные символы подчеркивания из получившихся названий;
      5) удаляет идущие подряд знаки подчеркивания;
    На входе: строка (str)
    На выходе: исправленная строка (str)
    '''
    table_of_replace = {' ': '_', '	': '_tab_', '.': '_dot_', ':': '_colon_'}
    for i in table_of_replace: string=string.replace(i, table_of_replace[i])
    for i in range(len(string)-1,-1,-1):
        if string[i].isupper(): string = string[:i]+'_'+string[i:]
    string = string.lower()
    while string[-1] == '_' : string = string[:-1]
    while string[0] == '_': string = string[1:]
    while string.find('__') != -1: string = string.replace('__', '_')
    return string

def preprocessing__normalization_of_column_names(dataframe, report=None):
    '''
    предобработка: нормализация названий столбцов.
    При обнаружении дубликатов названий генерирует исключение, с описанием ситуации.
    На входе: датафрейм, report (куда направлять отчет. По умолчанию - никуда.
      Возможны варианты: None, con, stderr, jupyter
    На выходе: датафрейм с нормализованными названиями. В консоль выводится
      информация о переименованных столбцах.
    '''
    # Вероятность словить 2 одинаковых имени столбца в датафрейме в ближайшем
    # обозримом будующем равна нулю, поэтому проще кинуть исключение, чем писать
    # обрабатывающую логику.
    if dataframe.columns.nunique() != len(dataframe.columns):
        raise PadlasException('В датасете присутствуют столбцы с одинаковым\
 именем. Требуется предварительное ручное вмешательство.')
    columns = {}
    for name in list(dataframe.columns):
        preparing_string = preparing_string_for_column_names(name)
        if name != preparing_string:
            if name not in columns:
                columns[name] = preparing_string
                report_string = 'Столбец "'+name+'" был переименован в "'+preparing_string+'"'
                if report == 'con': print(report_string)
                elif report == 'stderr': sys.stderr.write(report_string+'\n')
                elif report == 'jupyter': display(Markdown('* '+report_string))
            else: raise PadlasException('Автоматическое переименования столбцов\
 сгенерировало два новых имени, которые совпадают между собой. Требуется\
 предварительное ручное вмешательство. "'+str(name)+'"')
    dataframe = dataframe.rename(columns=columns)
    if dataframe.columns.nunique() != len(dataframe.columns):
        raise PadlasException('Автоматическое переименование столбцов\
 сгенерировало имя, которое совпадает с уже используемым. Требуется\
 предварительное ручное вмешательство.')
    return dataframe.rename(columns=columns)

symtab = '	' # в Юпитере вставить символ табуляции проблематично. Записал в переменную

def duplicated__set(dataset:pd.core.frame.DataFrame):
    '''
    Возвращает сет индексов строк, являющихся полными дубликатами
    '''
    result = []
    for i , v in enumerate(dataset.duplicated()):
        if v: result.append(i)
    return set(result)

def isna(n):
    if str(type(n)) == "<class 'NoneType'>": return True
    if str(type(n)) == "<class 'pandas._libs.missing.NAType'>": return True
    if n == None: return True
    if n != n: return True
    return False
