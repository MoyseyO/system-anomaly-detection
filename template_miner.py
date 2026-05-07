import re
from typing import Dict, Tuple
import pandas as pd

NUMBER_REGEX = re.compile(r"^-?\d+(\.\d+)?$")
IP_REGEX = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
HEX_REGEX = re.compile(r"^[0-9a-fA-F]{6,}$")

def normalize_token(token: str) -> str:
    """Заміна змінних токенів (IP, числа, hex) на <*>."""
    t = token.strip()
    if not t:
        return t
    if NUMBER_REGEX.match(t) or IP_REGEX.match(t) or HEX_REGEX.match(t):
        return "<*>"
    return t

def build_templates(
    df: pd.DataFrame,
    content_col: str = "Content",
    templates: Dict[str, int] | None = None,
    start_id: int | None = None,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Проходить по колонці content_col, будує шаблони і словник template->id.
    Повертає:
      df_out: df + Template, TemplateId
      templates: оновлений словник шаблонів.
    """
    if templates is None:
        templates = {}
    if start_id is None:
        start_id = len(templates)

    template_ids = []
    template_texts = []

    for content in df[content_col]:
        tokens = str(content).split()
        norm_tokens = [normalize_token(tok) for tok in tokens]
        template = " ".join(norm_tokens)

        if template not in templates:
            templates[template] = start_id
            start_id += 1

        tid = templates[template]
        template_ids.append(tid)
        template_texts.append(template)

    df_out = df.copy()
    df_out["Template"] = template_texts
    df_out["TemplateId"] = template_ids
    return df_out, templates
