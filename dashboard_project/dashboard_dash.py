import logging
import os

import dash_bootstrap_components as dbc
import dotenv
from dash import Dash, html
from numpy import info

# --- конфигурация и .env ---
dotenv.load_dotenv()
DVR_USERNAME = os.getenv("USERNAME")
DVR_PASSWORD = os.getenv("PASSWORD")
SERVERS = os.getenv("SERVERS", "").split(",")

DB_DSN = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

servers = [
    {"name": "Сервер 1", "cpu": "45%", "ram": "3.2/8 GB", "status": "online"},
    {"name": "Сервер 2", "cpu": "90%", "ram": "7.5/8 GB", "status": "offline"},
    # ... добавьте остальные серверы
    {"name": "Сервер 3", "cpu": "34%", "ram": "3.2/8 GB", "status": "online"},
    {"name": "Сервер 4", "cpu": "76%", "ram": "7.5/8 GB", "status": "offline"},
    {"name": "Сервер 5", "cpu": "56%", "ram": "3.2/8 GB", "status": "online"},
    {"name": "Сервер 6", "cpu": "45%", "ram": "7.5/8 GB", "status": "offline"},
    {"name": "Сервер 7", "cpu": "25%", "ram": "3.2/8 GB", "status": "online"},
    {"name": "Сервер 8", "cpu": "56%", "ram": "7.5/8 GB", "status": "offline"},
]

# Стиль для контейнера с карточками
grid_style = {
    "display": "flex",
    "flexWrap": "wrap",
    "gap": "20px",
    "padding": "10px",
}

# .online { color: green; }
# .offline { color: red; }

# Стиль для каждой карточки
card_style = {
    "border": "1px solid #ddd",
    "borderRadius": "8px",
    "padding": "15px",
    "width": "300px",
}

app.layout = html.Div(
    [
        html.H1("Мониторинг видеосерверов"),
        html.Div(
            children=[
                html.Div(
                    [
                        html.H3(server["name"]),
                        html.P(f"CPU: {server['cpu']}"),
                        html.P(f"RAM: {server['ram']}"),
                        html.P(f"Статус: {server['status']}"),
                    ],
                    style=card_style,
                )
                for server in servers
            ],
            style=grid_style,
        ),
    ]
)

if __name__ == "__main__":
    logging.info("Запуск вывода информации")
    app.run(debug=True)
    logging.info("Остановка вывода информации")
