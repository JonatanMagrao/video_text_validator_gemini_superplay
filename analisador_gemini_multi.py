import os
import json
import google.generativeai as genai
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- (Funções `videos_from_path` e `upload_video_if_needed` continuam iguais) ---


def videos_from_path(folder_path: str) -> list:
    folder_path_normalized = Path(folder_path)
    lista_videos = [
        item for item in folder_path_normalized.iterdir() if item.suffix.lower() == ".mp4"]
    return lista_videos


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def upload_video_if_needed(path: Path):
    print(f"Processing video file: {path.name}...")
    video_file = genai.upload_file(path=str(path))

    while video_file.state.name == "PROCESSING":
        print(f'({path.name}) Processing...', end=' ', flush=True)
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(
            f"Video processing failed for {path.name}: {video_file.state}")

    print(
        f"\nUpload complete for {path.name}! Resource name: {video_file.name}")
    return video_file
# --------------------------------------------------------------------------------


def analyze_single_video(video_path: Path, validation_data: list):
    """Analyzes a single video against a structured list of rules."""
    print(f"\n{'='*50}")
    print(f"STARTING ANALYSIS FOR: {video_path.name}")
    print(f"{'='*50}")

    try:
        video_file_resource = upload_video_if_needed(video_path)

        generation_config = {
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=generation_config
        )

        prompt_data = json.dumps(validation_data, ensure_ascii=False, indent=2)

        # 2. MUDANÇA NO PROMPT
        prompt = f"""
        Você é um auditor de QA de vídeo, focado exclusivamente em validar textos em japonês.
        Analise o vídeo fornecido e valide o conteúdo com base na seguinte lista de regras em JSON:
        {prompt_data}

        Siga esta lógica estrita para cada item da lista:
        1. O campo "EN" é para referência humana e DEVE ser ignorado na sua análise.
        
        2. Verifique se o campo "ja_new_proposal" tem um valor válido.
           - SIM: O texto esperado é o de "ja_new_proposal". Verifique se ele está no vídeo. Se, em vez dele, o texto "JA" for encontrado, é uma falha.
           - NÃO: O texto esperado é o de "JA". Verifique se ele está no vídeo.

        3. Se o texto esperado não for encontrado, o status é 'ERROR'.

        Sua resposta DEVE ser um objeto JSON com uma chave "video_name" (use o nome '{video_path.name}') e uma chave "validation_results".
        
        Para cada item na lista de resultados, inclua os seguintes campos:
        - "status": 'PASS', 'FAIL', ou 'ERROR'.
        - "found": O texto que foi efetivamente encontrado no vídeo para tomar a decisão. Para 'PASS', será o texto esperado. Para 'FAIL', será o texto antigo/incorreto.
        - "expected": O texto que era o alvo correto da validação.

        SE E SOMENTE SE o status for 'FAIL', inclua também o seguinte campo adicional:
        - "reason": "Versão antiga encontrada no vídeo."

        Sua resposta DEVE ser apenas o objeto JSON final.
        """

        print(f"Sending prompt for {video_path.name}...")
        response = model.generate_content([video_file_resource, prompt])
        parsed_json = json.loads(response.text)
        return parsed_json

    except Exception as e:
        print(
            f"\nAn unexpected error occurred for video {video_path.name}: {e}")
        return {"video_name": video_path.name, "error": str(e)}


# --- SCRIPT STARTING POINT ---
if __name__ == "__main__":
    folder_path = r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-015_Scenes_ToyStory_Revised_JA_30s"
    lista_de_videos = videos_from_path(folder_path)

    # 1. MUDANÇA NA ESTRUTURA DOS DADOS
    dados_para_validar = [
        {
            "EN": "DISCOVER THE MAGIC OF DISNEY SOLITAIRE",
            "JA": "ディズニーソリティアの魔法を見つけ出そう",
            "ja_new_propostal": "ディズニーソリティアの魔法を体感しよう"
        },
        {
            "EN": "RECREATE UNFORGETTABLE MEMORIES",
            "JA": "忘れられない思い出を再現しよう",
            "ja_new_propostal": "あの感動が、今ふたたび！"
        },
        {
            "EN": "tale as old as time",
            "JA": "テイル・アズ・オールド・アズ・タイム",
            "ja_new_propostal": "素晴らしい物語"
        },
        {
            "EN": "YOU'VE GOT A FRIEND IN ME",
            "JA": "君はともだち",
            "ja_new_propostal": None
        },
        {
            "EN": "UNDER THE SEA",
            "JA": "アンダー・ザ・シー",
            "ja_new_propostal": None
        },
        {
            "EN": "YOU DID IT",
            "JA": "やったね！",
            "ja_new_propostal": None
        },
        {
            "EN": "SCENE COMPLETE",
            "JA": "シーンクリア",
            "ja_new_propostal": None
        },
        {
            "EN": "PLAY NOW",
            "JA": "今すぐプレイ",
            "ja_new_propostal": None
        }
    ]

    MAX_WORKERS = 4

    print(
        f"Found {len(lista_de_videos)} videos to analyze. Starting parallel processing with {MAX_WORKERS} workers...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(analyze_single_video, video_path,
                                   dados_para_validar): video_path for video_path in lista_de_videos}

        for future in as_completed(futures):
            video_name = futures[future].name
            try:
                final_report_json = future.result()

                print(f"\n{'='*60}")
                print(f"FINAL VALIDATION REPORT FOR: {video_name}")
                print(f"{'='*60}")
                print(json.dumps(final_report_json,
                      ensure_ascii=False, indent=2))
                print("-" * 60)

            except Exception as exc:
                print(
                    f"\n!!! An error occurred while processing the result for {video_name}: {exc}")

    print("\nAll analyses are complete.")
