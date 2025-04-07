import pandas as pd

def convert_csv_to_excel(csv_file_path: str, excel_file_path: str) -> None:
    """
    Convert method a CSV file to an Excel file.
    """

    df = pd.read_csv(csv_file_path, sep=';')

    df.to_excel(excel_file_path, index=False)

convert_csv_to_excel('./csv/micromania_donnees_fictives.csv', './excel/micromania_donnees_fictives.xlsx')
