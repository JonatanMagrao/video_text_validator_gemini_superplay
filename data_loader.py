import os
import json
from pathlib import Path


# Sua lista de projetos e os caminhos das pastas de vídeo
projects_database = [
    {"prefix": "DS-V-024-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025\Creative Projects\DS-V-024_Puzzle_LiloStitch\Render\(Internal Review)\DS-V-024-001_Puzzle_LiloStitch_30s_LOC\DS-V-024-001_Puzzle_LiloStich_JA_30s\01"},
    {"prefix": "DS-V-002-015", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-015_Scenes_ToyStory_Revised_JA_30s/04"},
    {"prefix": "DS-V-027-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-027_Overstack\Render\(Internal Review)\DS-V-027-001_Overstack_JA_30s"},
    {"prefix": "DS-V-018-005", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-018_NewWorld\Render\(Internal Review)\DS-V-018-005_NewWorld_JA_15s\1"},
    {"prefix": "DS-V-002-026", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-026_Scenes_Beast_Revised_NoFrames_JA_60s\1"},
    {"prefix": "DS-V-011-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-011_AsoGrand\Render\(Internal Review)\DS-V-011-001_AsoGrand_JA_30s"},
    {"prefix": "DS-V-013-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-013_MagicalLevel\Render\(Internal Review)\DS-V-013-001_MagicalLevel_JA_30s"},
    {"prefix": "DS-V-011-003", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-011_AsoGrand\Render\(Internal Review)\DS-V-011-003_ASOGrand_JA_60s"},
    {"prefix": "DS-V-002-025", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-025_Scenes_LionKing_Revised_JA_60s/023"},
    {"prefix": "DS-V-002-032", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-032_Scenes_Beast_Revised_DS-H-001-001_JA_30s\1"},
    {"prefix": "DS-V-002-035", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-035_Scenes_Beast_Revised_DS-H-001-001_JA_60s\1"},
    {"prefix": "DS-V-002-036", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-036_Scenes_ToyStory_Revised_JA_60s\1"},
    {"prefix": "DS-V-002-039", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-039_Scenes_ToyStory_Revised_H-004-001_JA_35s\1"},
    {"prefix": "DS-V-002-040", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-040_Scenes_ToyStory_Revised_DS-H-004-001_JP_20s\1"},
    {"prefix": "DS-V-002-041", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-002_Scenes\Render\(Internal Review)\DS-V-002-041_Scenes_ToyStoryRevised_DS-V-017-016_JA_60s\1"},
    {"prefix": "DS-V-017-020", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-017_HookLaunch\Render\(Internal Review)\DS-V-017-020_HookLaunch_GameplayLumiereMusic_DS-V-011-007_JA_34s"},
    {"prefix": "DS-V-012-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-012_Classic\Render\(Internal Review)\DS-V-012-001_Classic_JA_30s"},
    {"prefix": "DS-V-011-007", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-011_AsoGrand\Render\(Internal Review)\DS-V-011-007_AsoGrand_Simba_JA_30s/03"},
    {"prefix": "DS-V-022-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-022_Mahjong\DS-V-022-001_Mahjong_30s\Render\(Internal Review)\DS-V-022-001_Mahjong_JA_30s"},
    {"prefix": "DS-V-022-002", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-022_Mahjong\DS-V-022-002_Mahjong_OG_30s\Render\(Internal Review)\DS-V-022-002_Mahjong_OG_JA_30s"},
    {"prefix": "DS-V-023-001", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-023_PuzzleSplit\Render\(Internal Review)\DS-V-023-001_PuzzleSplit_LadyTramp_JA_30s"},
    # {"prefix": "DS-V-017-018", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-017_HookLaunch\Render\(Internal Review)\DS-V-017-018_HookLaunch_WhatsGoingOn_DS-V-001-009_JA_36s\1"},
    {"prefix": "DS-V-017-018", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-017_HookLaunch\Render\(Internal Review)\DS-V-017-018_HookLaunch_WhatsGoingOn_DS-V-001-009_JA_36s\2"},
    # {"prefix": "DS-V-001-009", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-001_SimpleGameplay\Render\(Internal Review)\DS-V-001-009_SimpleGameplay_FTUEIntro_JA_30s\1"},
    {"prefix": "DS-V-014-004", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-014_BuildSplit\Render\(Internal Review)\DS-V-014-004_BuildSplit_Moana+LionKing_JA_60s\1"},
    {"prefix": "DS-V-014-013", "path": r"G:\Drives compartilhados\Marketing_DS_2025_H2\Creative Projects\Video\DS-V-014_BuildSplit\Render\(Internal Review)\DS-V014-013_BuildSplit_Moana_Reverse_JA_30s\1\1"}
]

def find_path_by_prefix(prefix:str) -> str|None:
    matches = [project["path"] for project in projects_database if project["prefix"].startswith(f"DS-V-{prefix}")]
    return matches[0] if matches else None

