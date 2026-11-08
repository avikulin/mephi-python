from dz_simple_database_vikulin_m25_555.core import init_db_context

if __name__ == "__main__":
    processor = init_db_context()
    processor.run()