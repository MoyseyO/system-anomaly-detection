import os
from bgl_loader import load_bgl_structured
from template_miner import build_templates
from anomaly_score import (
    make_time_windows,
    compute_anomaly_score,
    compute_window_labels,
    quality_metrics,
)
from visualizer import plot_anomaly_score

def main(base_dir="."):
    # 1) Завантаження
    df = load_bgl_structured(base_dir=base_dir, filename="BGL.log_structured.csv", n_rows=None)
    print("Загальна кількість рядків:", len(df))

    # 2) Шаблонізація всього набору
    df_tpl, templates = build_templates(df, content_col="Content")
    print("Кількість унікальних шаблонів:", len(templates))

    # 3) Формування часових вікон (10 хвилин – можна змінити)
    windows = make_time_windows(df_tpl, window="10min")
    print("Кількість вікон:", len(windows))

    # 4) Розрахунок A(W)
    anomaly_df = compute_anomaly_score(windows)

    # 5) Нормалізація A(W) до [0, 1]
    A_min, A_max = anomaly_df["A"].min(), anomaly_df["A"].max()
    anomaly_df["A_norm"] = (anomaly_df["A"] - A_min) / (A_max - A_min + 1e-9)
    print(f"Мінімум A(W): {A_min:.4f}, максимум: {A_max:.4f}")

    # 6) Якщо є мітки – обчислюємо якість по вікнах
    if "Label" in df.columns and df["Label"].nunique() > 1:
        window_labels = compute_window_labels(windows)
        anomaly_df["WindowLabel"] = window_labels.values

        # Вибір порогу як 0.9-квантиль
        thr = float(anomaly_df["A_norm"].quantile(0.9))
        metrics = quality_metrics(window_labels, anomaly_df["A_norm"], threshold=thr)

        print("Оцінка якості (по вікнах):")
        for k, v in metrics.items():
            if isinstance(v, float):
                print(f"  {k}: {v:.4f}")
            else:
                print(f"  {k}: {v}")
        threshold_for_plot = thr
    else:
        print("Мітки аномалій відсутні – метрики якості не обчислюються.")
        threshold_for_plot = float(anomaly_df["A_norm"].quantile(0.9))

    # 7) Побудова і збереження графіка
    anomaly_df_plot = anomaly_df.set_index("WindowStart")
    png_path = os.path.join(base_dir, "BGL_A_norm.png")
    plot_anomaly_score(
        anomaly_df_plot,
        score_col="A_norm",
        threshold=threshold_for_plot,
        title="Нормалізований індекс аномальності A_norm(W) (BGL)",
        save_path=png_path,
    )
    print("Графік збережено у:", png_path)

    # 8) Збереження таблиці результатів
    csv_path = os.path.join(base_dir, "BGL_anomaly_results.csv")
    anomaly_df.to_csv(csv_path, index=False)
    print("Таблиця результатів збережена у:", csv_path)

    return anomaly_df

if __name__ == "__main__":
    main()
