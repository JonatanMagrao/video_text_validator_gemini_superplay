import os, json, time, sys, time
from pathlib import Path
import google.generativeai as genai
from data_extractor_excel import get_sheet_data_by_prefix

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
EXCEL_PATH = r"C:\Users\PC\Downloads\DS_JA_Translation_Updated.xlsx"

def upload_video(path: Path):
    f = genai.upload_file(path=str(path))
    while f.state.name == "PROCESSING":
        time.sleep(10)
        f = genai.get_file(f.name)
    if f.state.name == "FAILED":
        raise RuntimeError(f"Upload falhou: {f.state}")
    return f

def analyze_video(video_path: Path, rules: list):
    video_res = upload_video(video_path)
    schema = {
        "type": "object",
        "properties": {
            "video_name": {"type": "string"},
            "validation_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "status": {"type": "string", "enum": ["PASS", "FAIL", "ERROR"]},
                "found":  {"type": "string"},
                "expected":{"type": "string"},
                "reason":  {"type": "string"}
                },
                "required": ["status", "found", "expected"]
            }
            }
        },
        "required": ["video_name", "validation_results"]
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": schema,
            "temperature": 0,
            "top_p": 0,
            "top_k": 1,
            "candidate_count": 1,
            # opcional: "max_output_tokens": 1024,
        }
    )

    prompt = f"""
    You are a video QA auditor focused on *exact* transcription of visible Japanese text.
    Follow the rules strictly. Never guess or infer text that is not visible on screen.
    Process the rules in the same order they are provided. 
    If no match is found, set "status" = "ERROR" and "reason" = "Not Found"

    Analyze the video and validate it using the rules below (JSON):

    {json.dumps(rules, ensure_ascii=False, indent=2)}

    Rules:
    1) Ignore "EN".
    2) If "ja_new_proposal" yhas a value, it is the expected text; if "JA" is found instead, it is a failure.
    3) If "ja_new_proposal" is null/absent, the expected text is "JA".
    4) If the expected text is not found, status = "ERROR".

    Respond ONLY with a JSON object containing:
    - "video_name": "{video_path.name}"
    - "validation_results": a list of items, each with:
    - "status": "PASS" | "FAIL" | "ERROR"
    - "found": the text actually found in the video that led to the decision
    - "expected": the target text
    - If "FAIL", also include "reason": "Old version found in the video."
    """

    resp = model.generate_content([video_res, prompt])
    return json.loads(resp.text)

