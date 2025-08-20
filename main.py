import json, time
from pathlib import Path
from data_extractor_excel import get_sheet_data_by_prefix
from analisador_gemini_solo import analyze_video
from data_loader import find_path_by_prefix
from tabulate import tabulate

EXCEL_PATH = r"C:\Users\PC\Downloads\DS_JA_Translation_Updated.xlsx"

project_prefix = "002-036"

video_folder = Path(find_path_by_prefix(project_prefix))
video_found = [video for video in video_folder.iterdir() if video.name.startswith(f"DS-V-{project_prefix}")]
video_path = Path(video_found[0])
rules = get_sheet_data_by_prefix(EXCEL_PATH, project_prefix).get("proposals")
print(f"\n{video_path.name:.^125}\n")
print(tabulate(rules, headers="keys",tablefmt="github"))
print("\n")  

start = time.time()
result = analyze_video(Path(video_path), rules)
end = time.time()
print(tabulate(result.get("validation_results"), headers="keys",tablefmt="github"))
print(f"\nTempo de análise: {end - start}")