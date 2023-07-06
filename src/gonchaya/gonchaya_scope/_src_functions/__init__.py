'''
Требует заполнения
'''
# gonchaya/gonchaya_scope/_src_functions/__init__.py

from types import FunctionType, MethodType

from gonchaya.gonchaya_scope._src_functions.pandas_DataFrame import *

pd.DataFrame.__init__ = decorator_add_property(pd.DataFrame.__init__)
