"""
20250430 Пишу дашбоард для серверов видеонаблюдения
трассир.
Автор: Евгений Петров
e-mail: p174@mail.ru
"""

import streamlit as st

if __name__ == "__main__":
    # Заголовок приложения
    st.header("st.button")
    # Формирую кнопку  с надписью Say Hello
    if st.button("Say Hello"):
        # Выводит надпись, если кнопка нажата
        st.write("Why hello there")
    else:
        st.write("Goodbye!!!")
