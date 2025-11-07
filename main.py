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

        with open(current_file, 'r', encoding="UTF-8") as file_html:
            result = file_html.read()
            # print(result)
        return result

    def do_GET(self) -> None:
        """ Метод для обработки входящих GET-запросов """

        # Загружаем стили
        if self.path.startswith("/static/"):
            static_file_path =self.path.lstrip("/")
            try:
                with open(static_file_path, "rb") as static_file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/css")
                    self.end_headers()
                    self.wfile.write(static_file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

            return

        self.send_response(200) # Отправка кода ответа
        self.send_header("Content-type", "text/html") # Отправка типа данных, который будет передаваться
        self.end_headers() # Завершение формирования заголовков ответа

        # читаем файл html, который возвращает разметку html
        r = self.__read_html("contacts.html")
        self.wfile.write(r.encode('utf-8'))

        #self.wfile.write(bytes("{'message': 'OK'}", "utf-8")) # Тело ответа

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    """
    Инициализация веб-сервера, который будет по заданным параметрах в сети
    принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    """

    webServer = HTTPServer((hostname, serverPort), MyServer)
    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
