#!/bin/python3
# it's gonchaya.py

#   *** Классическая предобработка данных ***
class GonchayaException(Exception):
    pass

# декоратор для pandas
# источник идеи https://tirinox.ru/class-decorator/
def pandas_with_added_functions(cls):
    class pandas_upd:
        def __init__(self, *args, **kwargs):
            self._obj = cls(*args, **kwargs)
        def __getattribute__(self, s):
            try:
                x = super().__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            
            attr = self._obj.__getattribute__(s)
            # это метод?
            if isinstance(attr, type(self._obj.__init__)):
                return attr
            else:
                # не метод, что-то другое
                return attr
        def test(self):
            self.abirvalg.__annotations__['return'] = 'test'
            return 'test'
        def __str__(self):
            # позволяет использовать print
            return self._obj.__str__()
        def __repr__(self):
            # формирует текстовое представление в функциях display,
            # интерактивном выводе значения переменной и пр.
            return self._obj.__repr__()
        #def __format__(self, format_spec):
            #if isinstance(format_spec, unicode):
            #    return unicode(str(self._obj))
            #else:
            #    return str(self._obj)
        #    return str(self._obj)
        
        # автоматически не подтягивается индексирование декорированного класса
        # укажем явно
        def __getitem__(self, s):
            return self._obj.__getitem__(s)
    return NewCls




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
        raise GonchayaException('В датасете присутствуют столбцы с одинаковым\
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
            else: raise GonchayaException('Автоматическое переименования столбцов\
 сгенерировало два новых имени, которые совпадают между собой. Требуется\
 предварительное ручное вмешательство. "'+str(name)+'"')
    dataframe = dataframe.rename(columns=columns)
    if dataframe.columns.nunique() != len(dataframe.columns):
        raise GonchayaException('Автоматическое переименование столбцов\
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

if __name__ == '__main__':
from gonchaya import _gonchaya
