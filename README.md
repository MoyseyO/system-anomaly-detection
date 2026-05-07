# system-anomaly-detection
The methods are designed for:  system log analysis; anomaly and failure detection; template frequency monitoring; comparative experiments with classical approaches.
Цей репозиторій містить програмну реалізацію методу виявлення відхилень у роботі систем 

## Основні компоненти:
- **Типізація (Template Mining)**: Автоматичне вилучення шаблонів із неструктурованих повідомлень (`template_miner.py`).
- **Аналіз аномалій**: Оцінка відхилень у послідовностях подій (`anomaly_score.py`).
- **Візуалізація**: Побудова розподілів та нормалізація результатів (`visualizer.py`).

## Як використовувати:
1. Клонуйте репозиторій.
2. Встановіть необхідні бібліотеки (pandas, numpy, matplotlib, re).
3. Запустіть `main_bgl.py` для обробки тестового набору
