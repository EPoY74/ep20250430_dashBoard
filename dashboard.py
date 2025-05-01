"""
Дашбоард от AI болванка
"""

import streamlit as st
import pandas as pd
import time

def main() -> None:
    """
    Точка входа в программу
    """

    st.title("Мониторинг видеонаблюдения")
    
    #  Заглушка данных
    servers = [
        {"name": "Server1", "cpu": 45, "status": "online"},
        {"name": "Server2", "cpu": 64, "status": "online"},
        {"name": "Server3", "cpu": 80, "status": "online"},
        {"name": "Server4", "cpu": 38, "status": "Offline"},
    ]

    while True:
        df = pd.DataFrame(servers)
        # st.table(df)
        st.dataframe(
            df
            )
        time.sleep(10)
        st.rerun()


if __name__ == "__main__":
    main()