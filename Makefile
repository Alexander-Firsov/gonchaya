TARGET ?= src

help:
	@echo "Tasks in \033[1;32mgonchaya\033[0m:"
	@cat Makefile

lint:  # проверка соответствию PEP8, синтаксическая корректность, корректность строк документации
	autopep8 --recursive --diff --aggressive --aggressive $(TARGET)
	mypy $(TARGET) --ignore-missing-imports # статический анализатор типов
	flake8 $(TARGET) --ignore=$(shell cat .flakeignore) # контроль кодстайла
	pydocstyle $(TARGET) # статический анализ для проверка соответствия соглашениям о строках документации Python (PEP 257)

dev:
	pip install -e .

test: dev
	pytest --doctest-modules --junitxml=junit/test-results.xml
	bandit -r $(TARGET) -f xml -o junit/security.xml || true # поиск распространенных проблем безопасности

build: clean
	#pip install wheel twine
	python setup.py bdist_wheel

# пароли для pypi должны лежать в ~/.pypirc
# пример: https://stackoverflow.com/questions/57935191/twine-is-asking-for-my-password-each-time-how-to-use-the-pypirc
pypi:
	twine upload -r pypi dist/*

pypitest:
	twine upload --verbose -r gonchaya dist/*

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete

#   example:
#
#>make lint
#
#   or:
#
#>make lint TARGET=setup.py
#
#   or:
#
#>export TARGET=setup.py
#>make lint
