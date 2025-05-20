from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

# Загрузка данных
data = []
with open("cameras_errirs_trassir.log", "r") as file:
    for line_number, line in enumerate(file, start = 1):
       
        parts = line.strip().split(",")
        lenparts = len(parts)
        if  lenparts < 3: continue
        print(f"Обрабатывается строка {line_number}:")
        print(line)
        time_str = parts[0].strip()
        name = parts[1].split(":")[1].strip()
        event = parts[2].split(":")[1].strip()
        server = parts[3].split(":")[1].strip()
        time = datetime.strptime(time_str, "%d.%m.%Y %H:%M:%S")
        data.append([time, name, event, server])

df = pd.DataFrame(data, columns=["Time", "Name", "Event", "Server"])
df = df.sort_values(["Name", "Time"]).reset_index(drop=True)

# Словари для хранения результатов
paired_events = {name: [] for name in df["Name"].unique()}
unpaired_lost = {name: [] for name in df["Name"].unique()}

# Обработка для каждого устройства
for name, group in df.groupby("Name"):
    events = group.to_dict("records")
    i = 0
    while i < len(events):
        if events[i]["Event"] == "Signal Lost":
            lost_event = events[i]
            found_restored = False

            j = i + 1
            while j < len(events):
                if events[j]["Event"] == "Signal Restored":
                    paired_events[name].append((lost_event, events[j]))
                    found_restored = True
                    i = j  # Переходим к событию после Restored
                    break
                j += 1

            if not found_restored:
                unpaired_lost[name].append(lost_event)
        i += 1

# Вывод всех найденных пар событий
print("=== Все найденные пары событий ===")
for name, pairs in paired_events.items():
    if pairs:
        print(f"\nУстройство: {name}")
        for idx, (lost, restored) in enumerate(pairs, 1):
            print(
                f"{idx}. Lost: {lost['Time']} -> Restored: {restored['Time']}"
            )

# Создаем DataFrame с длительностями перерывов
downtime_data = []
for name, pairs in paired_events.items():
    for lost, restored in pairs:
        downtime = restored["Time"] - lost["Time"]
        downtime_data.append(
            {"Name": name, "Time": lost["Time"], "Downtime": downtime}
        )

if downtime_data:
    lost_times = pd.DataFrame(downtime_data)

    # Расчет статистики
    print("\n=== Статистика по перерывам ===")
    print("Общее количество сбоев:", len(lost_times))
    print("Средняя длительность перерыва:", lost_times["Downtime"].mean())
    print("Максимальный перерыв:", lost_times["Downtime"].max())
    print("Минимальный перерыв:", lost_times["Downtime"].min())

    # Визуализация
    lost_times["DowntimeSeconds"] = lost_times["Downtime"].dt.total_seconds()
    plt.figure(figsize=(12, 6))
    plt.plot(lost_times["Time"], lost_times["DowntimeSeconds"], "o-")
    plt.xlabel("Время")
    plt.ylabel("Длительность перерыва (секунды)")
    plt.title("Длительность перерывов по времени")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("\nНет данных для построения статистики.")

# Вывод незавершенных событий
print("\n=== Незавершенные события ===")
for name, unpaired in unpaired_lost.items():
    if unpaired:
        print(f"\nУстройство: {name}")
        for idx, event in enumerate(unpaired, 1):
            print(f"{idx}. {event['Time']} - {event['Event']}")
