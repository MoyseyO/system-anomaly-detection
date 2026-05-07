import matplotlib.pyplot as plt

def plot_anomaly_score(
    anomaly_df,
    score_col: str = "A",
    threshold: float | None = None,
    title: str = "",
    figsize=(12, 4),
    save_path: str | None = None,
):
    """
    Малює графік значення score_col у часі. Якщо threshold заданий – малює горизонтальну лінію.
    Якщо save_path заданий – зберігає графік у файл.
    """
    plt.figure(figsize=figsize)
    plt.plot(anomaly_df.index, anomaly_df[score_col], label=score_col)
    if threshold is not None:
        plt.axhline(threshold, linestyle="--", label=f"Поріг = {threshold}")
    plt.xlabel("Часовий інтервал")
    plt.ylabel(score_col)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
