import pytest
import sys
def run_all_tests():
    print("Запуск автоматизированных тестов...")

    # Список аргументов для запуска:
    # -v: подробный вывод
    # -s: показывать print() в консоли во время тестов
    args = ["-v", "-s"]

    exit_code = pytest.main(args)

    if exit_code == 0:
        print("\n✅ Все тесты прошли успешно!")
    else:
        print(f"\n❌ Тесты упали с кодом: {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    run_all_tests()