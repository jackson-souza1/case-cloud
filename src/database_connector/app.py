from repositories.cessao_repository import CessaoRepository
from concurrent.futures import as_completed, ThreadPoolExecutor
from http import HTTPStatus
import json


def handler(event, context):
    print("##Evento")
    print(event)
    records = json.loads(event['Records'][0]['body'])
    repository = CessaoRepository()
    futures = []
    with ThreadPoolExecutor() as executor:
        for record in records:
            futures.append(executor.submit(repository.create, record))
        for future in as_completed(futures):
            print(future.result())
    return {
        "statusCode": HTTPStatus.OK,
        "body": {
            "result": "Registros inseridos com sucesso"
        }
    }
