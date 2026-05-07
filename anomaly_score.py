import pandas as pd
import numpy as np
from typing import List

def make_time_windows(df: pd.DataFrame, window: str = "10min") -> List[pd.DataFrame]:
    """
    Формує часові вікна фіксованої тривалості.
    Повертає список DataFrame, по одному на вікно.
    """
    df = df.sort_values("Datetime")
    windows = []
    for _, w in df.groupby(pd.Grouper(key="Datetime", freq=window)):
        if len(w) == 0:
            continue
        windows.append(w)
    return windows

def compute_anomaly_score(windows: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Розраховує індекс аномальності A(W) для кожного вікна:
      A(W) = евклідова норма відхилення розподілу TemplateId всередині вікна.
    """
    results = []
    print("Обчислення індексу аномальності для", len(windows), "вікон...")

    for w in windows:
        freq = w["TemplateId"].value_counts(normalize=True)

        if len(freq) > 1:
            mean_freq = freq.mean()
            deviation = np.sqrt(((freq - mean_freq) ** 2).sum())
        else:
            deviation = 0.0

        results.append(
            {
                "WindowStart": w["Datetime"].iloc[0],
                "WindowEnd": w["Datetime"].iloc[-1],
                "A": deviation,
                "Events": len(w),
                "UniqueTemplates": freq.size,
            }
        )

    anomaly_df = pd.DataFrame(results)
    print("✅ Обчислено індекс аномальності для всіх вікон.")
    return anomaly_df

def compute_window_labels(windows: List[pd.DataFrame]) -> pd.Series:
    """
    Вікно вважається аномальним (Label=1), якщо в ньому є хоч один лог з Label=1.
    """
    labels = []
    for w in windows:
        labels.append(int((w.get("Label", 0) == 1).any()))
    return pd.Series(labels, name="WindowLabel")

def quality_metrics(y_true: pd.Series, y_score: pd.Series, threshold: float):
    """
    Обчислює precision, recall, F1 для заданого порогу по вікнах.
    """
    y_pred = (y_score >= threshold).astype(int)

    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())

    precision = tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = tp / (tp + fn) if tp + fn > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0

    return {
        "threshold": threshold,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }
