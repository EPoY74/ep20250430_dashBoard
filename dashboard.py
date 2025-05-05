"""
Дашбоард от AI болванка
"""

from typing import Any
import streamlit as st
import pandas as pd
import time


DASHBOARD_COLUNNS = 3


def main() -> None:
    """
    Точка входа в программу
    """

    # st.title("Мониторинг видеонаблюдения")

    def fetch_serevers_data() -> list[dict[str, Any | None]]:
        """
        Заглушка для данных.
        """
        servers = [
            {"name": "Server1", "cpu": 45, "status": "online"},
            {"name": "Server2", "cpu": 64, "status": "online"},
            {"name": "Server3", "cpu": 80, "status": "online"},
            {"name": "Server4", "cpu": 38, "status": "offline"},
            {"name": "Server1-1", "cpu": 45, "status": "online"},
            {"name": "Server2-3", "cpu": 64, "status": "online"},
            {"name": "Server3-2", "cpu": 80, "status": "online"},
            {"name": "Server4-1", "cpu": 38, "status": "offline"}
        ]
        return servers

    # Стиль для карточек серверов
    st.markdown(
        """
        <style>
        .server-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px;
            width: 300px;
            display: inline-block;
            vertical-align: top;
            box-sizing: border-box; 
        }
        .online { color: green; }
        .offline { color: red; }
        .servers-container {
            width: 1800px
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 10px; /* Унифицированный отступ */
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
    servers_health = fetch_serevers_data()

    view_columns_per_row = st.columns(
        DASHBOARD_COLUNNS,
        gap="medium",
        vertical_alignment="center"
        )
    
    st.markdown('<div class="servers-container">', unsafe_allow_html=True)
    for i, server in enumerate(servers_health):
        with view_columns_per_row[(i % DASHBOARD_COLUNNS)]:
            st.markdown(
                f"""
                    <div class="server-card">
                    <h3>{server["name"]}</h3>
                    <p>CPU: {server["cpu"]}</p>
                    <p>Статус: <span class="{server["status"]}">{server["status"]}</span></p>
                    </div>
                """,
                unsafe_allow_html=True,
            )

    # while True:
    #     df = pd.DataFrame(servers)
    #     # st.table(df)
    #     st.dataframe(df)
    #     time.sleep(10)
    #     st.rerun()


if __name__ == "__main__":
    main()
