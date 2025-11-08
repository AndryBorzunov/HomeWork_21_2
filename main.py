from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def __read_html(self, current_file: str) -> str:
        """Функция чтения шаблона html"""

        try:
            with open(current_file, "r", encoding="UTF-8") as file_html:
                result = file_html.read()
            return result
        except FileNotFoundError:
            print(f"Ошибка: файл {current_file} не найден")
            return "<html><body><h1>File not found</h1></body></html>"

    def do_GET(self) -> None:
        """Метод для обработки входящих GET-запросов"""

        print(f"Получен GET-запрос: {self.path}")

        # Загружаем статические файлы (CSS, JS, изображения)
        if self.path.startswith("/static/"):
            static_file_path = self.path.lstrip("/")
            try:
                # Определяем Content-type по расширению файла
                if static_file_path.endswith(".css"):
                    content_type = "text/css"
                elif static_file_path.endswith(".js"):
                    content_type = "application/javascript"
                elif static_file_path.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    content_type = "image/" + static_file_path.split(".")[-1]
                else:
                    content_type = "application/octet-stream"

                with open(static_file_path, "rb") as static_file:
                    self.send_response(200)
                    self.send_header("Content-type", content_type)
                    self.end_headers()
                    self.wfile.write(static_file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
            return

        # Обработка HTML страниц
        self.send_response(200)  # Отправка кода ответа
        self.send_header(
            "Content-type", "text/html; charset=utf-8"
        )  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа

        # Определяем, какую страницу показать в зависимости от пути
        if self.path == "/" or self.path == "/index.html":
            html_content = self.__read_html("index.html")
        elif self.path == "/catalog.html":
            html_content = self.__read_html("catalog.html")
        elif self.path == "/category.html":
            html_content = self.__read_html("category.html")
        elif self.path == "/contacts.html":
            html_content = self.__read_html("contacts.html")
        else:
            # Если путь не распознан, показываем контакты (как в задании)
            html_content = self.__read_html("contacts.html")

        self.wfile.write(html_content.encode("utf-8"))

        # self.wfile.write(bytes("{'message': 'OK'}", "utf-8")) # Тело ответа

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""

        print(f"Получен POST-запрос: {self.path}")

        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        print(f"Тело запроса: {body.decode('utf-8')}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Возвращаем ту же страницу контактов после отправки формы
        html_content = self.__read_html("contacts.html")
        self.wfile.write(html_content.encode("utf-8"))


if __name__ == "__main__":
    """
    Инициализация веб-сервера, который будет по заданным параметрах в сети
    принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    """

    webServer = HTTPServer((hostname, serverPort), MyServer)
    print(f"Сервер запущен http://{hostname}:{serverPort}")
    print("Для остановки сервера нажмите Ctrl+C")

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        print("\nОстановка сервера...")

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Сервер остановлен.")
