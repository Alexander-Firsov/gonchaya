'''
В этом пакете располагаются функции общего назначения, которые будут
импортированы в глобальную зону видимости
'''
# src/gonchaya/global_scope/__init__.py

# пока мало всего, описываю прям тут

def isna(n):
    if str(type(n)) == "<class 'NoneType'>": return True
    if str(type(n)) == "<class 'pandas._libs.missing.NAType'>": return True
    if n == None: return True
    if n != n: return True
    return False

def notna(n): return not isna(n)

symtab = '	' # в Юпитере вставить символ табуляции проблематично. Записал в переменную
