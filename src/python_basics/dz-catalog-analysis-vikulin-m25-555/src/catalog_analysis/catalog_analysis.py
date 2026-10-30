from catalog_analysis.data_samples import get_data
from catalog_analysis.func.composers import build_report


def main():
    movies = get_data()
    print(build_report(movies))

if __name__ == "__main__":
    main()