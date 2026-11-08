from dz_simple_database_vikulin_m25_555.utils.console.db_console_colors import Color


class Primitive:
    INPUT   = f"{Color.OKGREEN} ВВОД ⮞ {Color.ENDC}"
    OUTPUT  = f"{Color.OKBLUE } [*] {Color.ENDC}"

    ERROR   = f"{Color.FAIL   } ⭕ {Color.ENDC}"
    HINT    = f"{Color.WARNING} ⬛ {Color.ENDC}"
    LOG     = f"{Color.WARNING} ~ {Color.ENDC}"

    END_OUTPUT = f"{Color.OKBLUE }---{Color.ENDC}"
    END_ERROR = f"{Color.FAIL   }---{Color.ENDC}"
    END_HINT = f"{Color.WARNING}---{Color.ENDC}"
