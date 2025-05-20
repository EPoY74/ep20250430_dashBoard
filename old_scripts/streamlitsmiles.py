import streamlit as st
import pandas as pd

# # Заголовок приложения
# st.title("Таблица смайликов с управлением видимостью")

st.markdown(
    "<h1 style='white-space: nowrap; width: 95%'>1Таблица смайликов с управлением видимостью</h1>",
    unsafe_allow_html=True,
)

# Создаем DataFrame с смайликами
data = {
    "A": ["😊", "😂", "🤔", "😍"],
    "B": ["👍", "👎", "🙏", "✌️"],
    "C": ["🐶", "🐱", "🐭", "🐹"],
    "D": ["🍎", "🍌", "🍒", "🍓"],
}
df = pd.DataFrame(data)

# Создаем чекбоксы для управления видимостью столбцов
st.sidebar.header("Управление видимостью столбцов")
visible_columns = {}
for column in df.columns:
    visible_columns[column] = st.sidebar.checkbox(
        f"Показать {column}", value=True
    )

# Фильтруем столбцы, которые нужно показать
columns_to_show = [col for col in df.columns if visible_columns[col]]
filtered_df = df[columns_to_show]

# Отображаем таблицу
st.dataframe(filtered_df)

# Альтернативный вариант с более гибким управлением (по ячейкам)
st.header("Расширенное управление видимостью ячеек")

# Создаем сетку чекбоксов для каждой ячейки
cell_visibility = {}
for i in range(len(df)):
    for col in df.columns:
        cell_visibility[(i, col)] = st.checkbox(
            f"Показать ячейку {col}{i} ({df[col][i]})",
            value=True,
            key=f"cell_{i}_{col}",
        )

# Создаем стилизованную таблицу с HTML
html = "<table><tr><th></th>"
for col in df.columns:
    html += f"<th>{col}</th>"
html += "</tr>"

for i in range(len(df)):
    html += "<tr>"
    html += f"<td>Строка {i}</td>"
    for col in df.columns:
        if cell_visibility.get((i, col), True):
            html += f"<td style='border: 1px solid; padding: 5px; text-align: center;'>{df[col][i]}</td>"
        else:
            html += "<td style='border: 1px solid; padding: 5px; text-align: center; color: lightgray;'>---</td>"
    html += "</tr>"

html += "</table>"

# Отображаем HTML таблицу
st.markdown(html, unsafe_allow_html=True)
