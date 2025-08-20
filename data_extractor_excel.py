import json
from pathlib import Path
from openpyxl import load_workbook

def get_sheet_data_by_prefix(file_path: str, prefix: str) -> dict | None:
    """
    Busca uma aba em um arquivo Excel cujo nome começa com 'DS-V-{prefix}' 
    (case-insensitive) e retorna os dados da aba em formato dict.
    
    :param file_path: Caminho para o arquivo .xlsx
    :param prefix: Sufixo a ser buscado após 'DS-V-'
    :return: dict com dados da aba ou None se não encontrado
    """

    def find_sheet_by_prefix(sheet_names: list, prefix: str) -> str | None:
        matches = [name for name in sheet_names if name.lower().startswith(f"ds-v-{prefix}")]
        return matches[0] if matches else None

    def read_sheet_data(sheet) -> dict:
        data = {"aba": sheet.title, "proposals": []}
        for row in sheet.iter_rows(values_only=True):
            if row[0] is None:
                continue
            if row[0] == "EN" and row[1] == "JA" and row[2] == "JA-NP":
                continue
            data["proposals"].append({
                "EN": row[0],
                "JA": row[1],
                "ja_new_proposal": row[2]
            })
        return data

    workbook = load_workbook(file_path, read_only=True)
    sheet_name = find_sheet_by_prefix(workbook.sheetnames[1:], prefix)

    if sheet_name:
        sheet = workbook[sheet_name]
        return read_sheet_data(sheet)
    return None


