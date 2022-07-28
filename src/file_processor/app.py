import json
import uuid
from http import HTTPStatus
from services.processor import CsvProcessor


def lambda_handler(event, context):
    try:
        request_body = json.loads(event['body'])
        CsvProcessor(
            object_key=request_body['object_key'],
            bucket_name=request_body['bucket_name']
        ).run()
        return {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps({
                "status": "enviado",
                "identificador": str(uuid.uuid4()),  # Ficticio
                "mensagem": "Arquivo enviado com sucesso para o processamento!"
            })
        }
    except Exception as e:
        print(str(e))
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({
                "result": "Houve uma falha no processamento do arquivo!"
            }),
        }
