import runpy

STAGES = {
    "stage_1": "Разминка: переменные, числа, `math`",
    "stage_2": "Условия и `match`",
    "stage_3": "Циклы",
    "stage_4": "Строки",
    "stage_5": "Списки",
    "stage_6": "Словари",
    "stage_7": "Множества",
    "stage_8": "Итераторы и генераторы",
}

MODULE_PREFIX = "catalog_analysis.demo."


def _run_stage(name: str) -> None:
    print(f"\n{'=' * 60}\n>>> Запуск: `{name}.py`\n{'=' * 60}")
    runpy.run_module(MODULE_PREFIX + name, run_name="__main__")


def _print_menu() -> None:
    print("\n================ ДЕМО-МЕНЮ ================")
    for idx, name in enumerate(STAGES.values(), start=1):
        print(f"  {idx}. {name}")
    print("  a. Запустить все по порядку")
    print("  q. Выход")
    print("=" * 44)


def main() -> None:
    while True:
        _print_menu()
        choice = input("Выберите пункт: ").strip().lower()

        if choice == "q":
            print("До встречи!")
            break

        if choice == "a":
            for name in STAGES.keys():
                _run_stage(name)
            continue

        if choice.isdigit() and 1 <= int(choice) <= len(STAGES):
            module_names = list(STAGES.keys())
            _run_stage(module_names[int(choice) - 1])
            continue

        print(f"Неизвестный пункт: {choice!r}, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
