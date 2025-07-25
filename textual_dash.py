from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header


class CCTVMonitor(App):
    def compose(self) -> ComposeResult:
        """Создаём структуру приложения."""
        yield Header()  # Верхняя панель
        yield DataTable()  # Основная таблица
        yield Footer()  # Нижняя панель

    def on_mount(self) -> None:
        """Инициализация таблицы после запуска."""
        table = self.query_one(DataTable)
        table.add_columns("Сервер", "Статус", "CPU %", "RAM %")
        table.add_rows(
            [
                ["Камера 1", "ONLINE", "45", "32"],
                ["Камера 2", "OFFLINE", "0", "0"],
                ["NVR", "LAGGING", "89", "78"],
            ]
        )


if __name__ == "__main__":
    app = CCTVMonitor()
    app.run()
