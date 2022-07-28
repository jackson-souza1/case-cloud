import json


class FileNotAvailableError(Exception):

    def __init__(self, file: str) -> None:
        self.message = f'Não foi possível obter informações do arquivo: {file}'
        super().__init__(file)

    def __str__(self) -> str:
        return self.message