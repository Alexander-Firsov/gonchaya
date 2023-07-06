'''
Требует заполнения
'''
# gonchaya/gonchaya_scope/_src_functions/pandas_DataFrame.py

from types import FunctionType, MethodType
import pandas as pd
from gonchaya.gonchaya_scope.exceptions import *

def decorator_add_property(method):
    def wrapper(*args, **kwargs):
        tmp=method(*args, **kwargs)
        args[0].dic=None
        args[0].title=None
        #print(f'Создание класса. {id(args[0])=} {id(tmp)=}')
        pd.DataFrame.preprocessing__normalization_of_column_names = MethodType(_preprocessing__normalization_of_column_names, args[0])
        return tmp
    return wrapper

def _preparing_string_for_column_names(string:'Строка, которую надо исправить (str)')->'исправленная строка (str)':
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
    @param string: строка (str), которую надо исправить
    @return: исправленная строка (str)
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

def _preprocessing__normalization_of_column_names(self, report=None):
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
    if self.columns.nunique() != len(self.columns):
        raise GonchayaException('В датасете присутствуют столбцы с одинаковым\
 именем. Требуется предварительное ручное вмешательство.')
    columns = {}
    for name in list(self.columns):
        preparing_string = _preparing_string_for_column_names(name)
        if name != preparing_string:
            if name not in columns:
                columns[name] = preparing_string
                report_string = 'Столбец "'+name+'" был переименован в "'+preparing_string+'"'
                if report == 'con': print(report_string)
                elif report == 'stderr': sys.stderr.write(report_string+'\n')
                elif report == 'jupyter': display(Markdown('* '+report_string))
            else: raise GonchayaException('Автоматическое переименования столбцов\
 сгенерировало два новых имени, которые совпадают между собой. Требуется\
 предварительное ручное вмешательство. "'+str(name)+'"')
    dataframe = self.rename(columns=columns)
    if dataframe.columns.nunique() != len(dataframe.columns):
        raise GonchayaException('Автоматическое переименование столбцов\
 сгенерировало имя, которое совпадает с уже используемым. Требуется\
 предварительное ручное вмешательство.')
    return dataframe.rename(columns=columns)
