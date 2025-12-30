# conftest.py
import pytest

@pytest.fixture(scope="session")
def new_data_collector():
    """Фикстура-контейнер для сбора данных по неудачным тестам."""
    collector = {}
    # Эта фикстура просто возвращает изменяемый объект (список), который живет всю сессию
    yield collector
    
    # Код ПОСЛЕ yield выполняется как teardown (после тестов)
    print(f'\n--- Сводка данных по неудачным тестам ---')
    if not collector:
        print("Данные не собраны.")
    else:
        for test, dic in collector.items():
            print(f'Добавьте в словарь {test} следующие значения, если они корректны:')
            for record  in dic:
                print(f'{record}')
            print(f'-----------------------------------------')
