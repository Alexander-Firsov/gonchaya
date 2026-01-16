# $HOME/projects/gonchaya/Makefile
TARGET ?= src
GONCHAYA_DIR := src/gonchaya
DEV_MARKER := .installed_dev
# Определяем Escape-символ и коды, используя printf для создания реального ESC-символа
# Используем := для простого расширения, чтобы значение было фиксированным
ESC := $(shell printf '\033')
COLOR_GREEN := $(ESC)[1;32m
COLOR_YELLOW := $(ESC)[1;33m
COLOR_RESET := $(ESC)[0m
PACKAGE ?= gonchaya
PYPROJECT = pyproject.toml

help: # Вывод этой информации.
	@echo -e "Tasks in $(COLOR_GREEN)gonchaya$(COLOR_RESET):"
	@grep -E "^[a-zA-Z_-].*[a-zA-Z_-]:" Makefile| sed \
	    "s@\\(.*\\):\\s*[^#]*#\\(.*\\)@$(COLOR_YELLOW)\\1$(COLOR_RESET) \\2@" \
	    | grep -v "##$$"
	@echo -e "\n\texample:"
	@echo "make lint"
	@echo -e "\tor:"
	@echo "make lint TARGET=setup.py"
	@echo -e "\tor:"
	@echo "export TARGET=setup.py"
	@echo "make lint"


lint:  # проверка соответствию PEP8, синтаксическая корректность, корректность строк документации
	autopep8 --recursive --diff --aggressive --aggressive $(TARGET)
	mypy $(TARGET) --ignore-missing-imports # статический анализатор типов
	@# Удобно за раз исправлять вместе flake8 с pydocstyle, поэтому по ошибке продолжаем (все равно еще раз запускать после исправлений).
	flake8 $(TARGET) || true # контроль кодстайла.
	pydocstyle $(TARGET) # статический анализ для проверка соответствия соглашениям о строках документации Python (PEP 257)
	@echo -e "\t\t$(COLOR_GREEN)Успешно.$(COLOR_RESET)"


dev: $(DEV_MARKER)  # перевод в режим разработчика, если еще не перевели.

# Правило для создания файла-маркера
$(DEV_MARKER): Pipfile # Добавьте сюда зависимости, которые должны обновляться
	@echo "Устанавливаю режим разработчика (dev) через pipenv..."
	@# Должно запустить установку режима разработчика при смене версии pipenv
	pipenv graph 2>/dev/null | grep gonchaya || pipenv install -e .
	@echo "Создаю файл-маркер $(DEV_MARKER)"
	touch $(DEV_MARKER) # Создаем пустой файл-маркер после успешного выполнения

# Добавьте цель для очистки, чтобы можно было переустановить dev режим принудительно
clean_dev:  # Отключить режим разработчика
	rm -f $(DEV_MARKER)
	pipenv uninstall gonchaya
	@echo "Файл-маркер $(DEV_MARKER) удален. Следующий вызов make dev выполнит установку."

.PHONY: help lint dev clean_dev test PEP8 clean pyi get_the_latest_version_from_PyPi publish_new_version

test: dev # запуск pytest
	pytest --doctest-modules --junitxml=junit/test-results.xml
	bandit -r $(TARGET) -f xml -o junit/security.xml || true # поиск распространенных проблем безопасности

PEP8: lint test

#build: clean
	#sudo apt install python3-setuptools sudo apt install python3-wheel
	#export PIPENV_VENV_IN_PROJECT=1
	#pip install wheel twine setuptools
#	python3 ./setup.py bdist_wheel
	#pipenv install --pypi-mirror https://test.pypi.org/simple/ gonchaya
	#pipenv run pip install -i https://test.pypi.org/simple/ gonchaya

# пароли для pypi должны лежать в ~/.pypirc
# пример: https://stackoverflow.com/questions/57935191/twine-is-asking-for-my-password-each-time-how-to-use-the-pypirc
#pypi:
#	twine upload -r pypi dist/*

#pypitest:
#	twine upload --verbose -r gonchaya dist/*

clean:  # очистка от кеша и временных файлов
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete
	# Удаляем сгенерированные заглушки
	@rm -f $(GONCHAYA_DIR)/superfast.pyi \
	       $(GONCHAYA_DIR)/debug.pyi \
	       $(GONCHAYA_DIR)/__init__.pyi \
	       $(GONCHAYA_DIR)/__init__.pyi.tmp


# --------------------------------------------------
# Цели генерации и слияния заглушек (.pyi)
# --------------------------------------------------
# Оформляются тут, т.к. есть неявное требование к минимуму файлов.

# 1. Генерируем superfast.pyi
$(GONCHAYA_DIR)/superfast.pyi: $(GONCHAYA_DIR)/superfast.py
	@stubgen --include-private $< -o src

# 2. Генерируем debug.pyi
$(GONCHAYA_DIR)/debug.pyi: $(GONCHAYA_DIR)/debug.py
	@stubgen --include-private $< -o src

# 3. Генерируем временный файл-заглушку для __init__.py (используем .tmp расширение)
#    Он нужен как "основа", к которой мы добавим определения из других файлов.
$(GONCHAYA_DIR)/__init__.pyi.tmp: $(GONCHAYA_DIR)/__init__.py
	# Генерируем базовый __init__.pyi
	@stubgen --include-private $< -o src
	# Переименовываем сгенерированный файл в .tmp, чтобы не конфликтовать с итоговым
	@mv $(GONCHAYA_DIR)/__init__.pyi $(GONCHAYA_DIR)/__init__.pyi.tmp


# Итоговая цель сборки заглушек:
# Зависит от всех сгенерированных частей.
# Итоговый файл: src/gonchaya/__init__.pyi
pyi: $(GONCHAYA_DIR)/superfast.pyi $(GONCHAYA_DIR)/debug.pyi $(GONCHAYA_DIR)/__init__.pyi.tmp # Сборка заглушек *.pyi
	@#echo "Объединение .pyi файлов в финальный $(GONCHAYA_DIR)/__init__.pyi"
	@cat $(GONCHAYA_DIR)/__init__.pyi.tmp \
	    $(GONCHAYA_DIR)/superfast.pyi \
	    $(GONCHAYA_DIR)/debug.pyi \
	    > $(GONCHAYA_DIR)/__init__.pyi
	@#echo "Первичное форматирование файла"
	@# Форматируем итоговый файл на месте
	@autopep8 --in-place --aggressive --aggressive $(GONCHAYA_DIR)/__init__.pyi
	@sed -i '/get_time_import: Any/,/def initialize_functions/ {/def initialize_functions/!d}' $(GONCHAYA_DIR)/__init__.pyi
	@sed -i '/from \. import/d' $(GONCHAYA_DIR)/__init__.pyi
	@awk '/default: dict\[str, Any\]/ && ++count == 2 {next} 1' src/gonchaya/__init__.pyi > temp.pyi
	@mv temp.pyi $(GONCHAYA_DIR)/__init__.pyi
	@echo "$(GONCHAYA_DIR)/__init__.pyi собран."

get_the_latest_version_from_PyPi: # проверка последней версии пакета на PyPi
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Ошибка: Укажите пакет, например: make get_the_latest_version_from_PyPi PACKAGE=requests"; \
		exit 1; \
	fi
	@VERSION=$$(curl -s https://pypi.org/pypi/$(PACKAGE)/json | jq -r '.info.version' 2>/dev/null); \
	if [ "$$VERSION" = "null" ] || [ -z "$$VERSION" ]; then \
		echo "Ошибка: Пакет '$(PACKAGE)' не найден на PyPI"; \
		exit 1; \
	else \
		echo "Последняя версия $(PACKAGE): $$VERSION"; \
	fi

publish_new_version: pyi # Публикация новой версии на PyPi
	@# 1. Получаем текущую версию из pyproject.toml (убираем кавычки и пробелы)
	@CURRENT_LOCAL=$$(grep '^version =' $(PYPROJECT) | cut -d '"' -f 2); \
	echo "Локальная версия в $(PYPROJECT): $$CURRENT_LOCAL"; \
	\
	# 2. Получаем версию из PyPI (вызываем вашу цель и сохраняем результат)
	# Мы используем ту же логику curl, что и в get_the_latest_version_from_PyPi
	CURRENT_PYPI=$$(curl -s https://pypi.org/pypi/$(PACKAGE)/json | jq -r '.info.version' 2>/dev/null); \
	if [ "$$CURRENT_PYPI" = "null" ] || [ -z "$$CURRENT_PYPI" ]; then CURRENT_PYPI="0.0.0"; fi; \
	echo "Версия на PyPI: $$CURRENT_PYPI"; \
	\
	# 3. Вычисляем новую версию (инкремент последней цифры)
	# Берем максимальную из двух и прибавляем 1 к последнему числу
	#NEW_VERSION=$$(echo "$$CURRENT_LOCAL\n$$CURRENT_PYPI" | sort -V | tail -n 1 | awk -F. '{$$(NF)++; print $$1"."$$2"."$$3}'); \
	#echo "Будет установлена новая версия: $$NEW_VERSION"; \
	#\
	# 3. Вычисляем новую версию
	# Используем printf для гарантированного переноса строки
	NEW_VERSION=$$(printf "%s\n%s" "$$CURRENT_LOCAL" "$$CURRENT_PYPI" | sort -V | tail -n 1 | awk -F. '{ \
		OFS="."; \
		$$NF = $$NF + 1; \
		print $$0 \
	}'); \
	echo "Будет установлена новая версия: $$NEW_VERSION";
	
	# 4. Обновляем версию в pyproject.toml
	sed -i "s/^version = \".*\"/version = \"$$NEW_VERSION\"/" $(PYPROJECT); \
	\
	# 5. Git: commit, tag, push
	git add $(PYPROJECT); \
	git commit -m "Bump version to $$NEW_VERSION"; \
	git tag v$$NEW_VERSION; \
	git pull --rebase; \
	echo "Отправка в GitHub..."; \
	git push origin main --tags
