# app.py (Dash)
from typing import Any, Dict  # noqa: UP035

import dash
import pandas as pd
from dash import Dash, Input, Output, dash_table, html
from dash.dash_table.DataTable import NumberType

# from dash.dash_table 

# from numbers import Number as NumberType

app = Dash(__name__)


servers: list[Dict[str | float | int, NumberType | str | bool]] | None= [] # noqa: UP006



servers = [
    {"name": "Сервер 1", "cpu": "45", "status": "online"},
    {"name": "Сервер 2", "cpu": "90", "status": "offline"},
]   


app.layout = html.Div(
    [
        html.H1("Мониторинг видеосерверов (Dash)"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": col, "id": col} for col in servers[0].keys()],
            data=servers,
        ),
        dash.dcc.Interval(id="interval", interval=10000),  # 10 сек
    ]
)


@app.callback(Output("table", "data"), Input("interval", "n_intervals"))
def update_table(n):
    # Здесь запрос к API / БД
    return updated_servers_data


if __name__ == "__main__":
    app.run(debug=True)
