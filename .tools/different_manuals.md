## Мои шпаргалочки

[Утверждение](https://pythonru.com/uroki/35-instrukcija-assert-dlja-nachinajushhih). `assert condition, message` 
Если condition равно True, то программа ничего не делает. Если ложь, то генерируется исключение AssertionError, с дополнительным сообщением message.  

`yield` - промежуточный return  

фикстуры. Используются в тестировании. [общие сведения](https://habr.com/ru/articles/731296/)
[пример с инициализацией движка браузера](https://habr.com/ru/articles/716248/)
Фикстуры позволяют тестовым функциям легко получать предварительно инициализированные объекты и работать с ними, не заботясь об импорте/установке/очистке.


[PyTest](https://habr.com/ru/articles/269759/)


[управление зависимостями python](https://menziess.github.io/howto/manage/virtual-environments/)
```
pip install pipenv
pipenv install toolz --python 3.12.3
pipenv shell
#deactivate
```

[Изначальные ноги, откуда ростет пустой проектъ(https://habr.com/ru/companies/piter/articles/700282/)  
[по мотивам](https://menziess.github.io/howto/create/python-packages/#1-packaging-setup)
```
python setup.py develop # don't generate anything, just install locally
python setup.py bdist_egg # generate egg distribution, doesn't include dependencies
python setup.py bdist_wheel # generate versioned wheel, includes dependencies
python setup.py sdist --formats=zip,gztar,bztar,ztar,tar # source code
```

`pipenv install -d mypy flake8 autopep8 pytest bandit pydocstyle`  
[mypy pyright](https://to.digital/typed-python/mypy/intro.html) `mypy ./weather`  
[autopep8 microtutorial](https://newtechaudit.ru/autopep8-spasatelnyj-krug-dlya-zelenyh-pitonistov/) `autopep8 --recursive --diff --aggressive --aggressive main.py`  
`flake8 my_project`
