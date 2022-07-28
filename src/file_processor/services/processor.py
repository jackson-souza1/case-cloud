import json
import re
import boto3
import pandas as pd
from http import HTTPStatus
from io import BytesIO
from exceptions.exceptions import FileNotAvailableError


class CsvProcessor(object):
    def __init__(self, object_key: str, bucket_name: str):
        self.__object_key = object_key
        self.__bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
        self.sqs_client = boto3.client('sqs', region_name='us-east-1')
        self.columns_to_mapper = ['Originador', 'Doc Originador', 'Cedente',
                                  'Doc Cedente', 'CCB', 'Id',
                                  'Cliente', 'CPF/CNPJ', 'Endereço',
                                  'CEP', 'Cidade', 'UF', 'Valor do Empréstimo',
                                  'Parcela R$', 'Total Parcelas', 'Parcela #',
                                  'Data de Emissão', 'Data de Vencimento', 'Preço de Aquisição'
                                  ]

    def run(self):
        file = self.__read_file_from_s3(key=self.__object_key, bucketname=self.__bucket_name)
        response = self.__convert_csv_to_json(csv_file=file)
        self.__send_message_to_sqs(
            queue='cessao-queue',  # obter do template
            message=response
        )
        return response

    def __read_file_from_s3(self, key: str, bucketname: str):
        """
            lê arquivo CSV de um bucket especificado e retorna um JSON
            :param key:
            :param bucketname:
            :return: DataFrame
        """
        s3_response = self.s3_client.get_object(Bucket=bucketname, Key=key)
        status = s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == HTTPStatus.OK:
            print(f"Successful S3 get_object response. Status - {status}")
            file = BytesIO(s3_response.get("Body").read())
        else:
            raise FileNotAvailableError(key)
        return file

    def __convert_csv_to_json(self, csv_file: BytesIO, delimiter: str = ';'):
        """
            Recebe um arquivo csv em bytes e o converte para JSON
            :param csv_file:
            :param delimiter:
            :return:
        """
        df = pd.read_csv(csv_file, encoding='latin1', delimiter=delimiter, usecols=self.columns_to_mapper).rename(
            columns={
                'Originador': 'originador',
                'Doc Originador': 'doc_originador',
                'Cedente': 'cedente',
                'Doc Cedente': 'doc_cedente',
                'CCB': 'ccb', 'Id': 'id_externo',
                'Cliente': 'cliente',
                'CPF/CNPJ': 'cpf_cnpj',
                'Endereço': 'endereco',
                'CEP': 'cep',
                'Cidade': 'cidade',
                'UF': 'uf',
                'Valor do Empréstimo': 'valor_do_emprestimo',
                'Parcela R$': 'valor_parcela',
                'Total Parcelas': 'total_parcelas',
                'Parcela #': 'parcela',
                'Data de Emissão': 'data_de_emissao',
                'Data de Vencimento': 'data_de_vencimento',
                'Preço de Aquisição': 'preco_de_aquisicao'
            }
        )
        df = self.__format_columns_to_datetime(dataframe=df, columns=[
            'data_de_vencimento', 'data_de_emissao'
        ])
        df = self.__clean_document_format(dataframe=df, column='cpf_cnpj')
        converted_file = df.to_json(orient='records', date_format='iso')
        return converted_file

    def __send_message_to_sqs(self, message: str, queue: str) -> None:
        """
            Envia mensagem para uma fila do sqs.
            :param message:
            :param queue:
        """
        response = self.sqs_client.send_message(
            QueueUrl=queue,
            MessageBody=message,
        )
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == HTTPStatus.OK:
            print(f"Successful SQS send message. Status - {status}")

    def __retrieve_queue_url(self, queue_name):
        """
            Recupera url da fila especificada
            :param queue_name:
            :return:
        """
        response = self.sqs_client.get_queue_url(
            QueueName=queue_name,
        )
        return response["QueueUrl"]

    @staticmethod
    def __format_columns_to_datetime(dataframe: pd.DataFrame, columns: list,
                                     date_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
            Converte colunas do dataframe para o formato de data especificado.
            :param dataframe:
            :param columns:
            :param date_format:
            :return: Dataframe
        """
        for column in columns:
            dataframe[column] = pd.to_datetime(dataframe[column])
            dataframe[column] = dataframe[column].dt.strftime(date_format)
        return dataframe

    @staticmethod
    def __clean_document_format(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
        """
            Limpa formatação do documento na coluna especificada.
            :param dataframe:
            :param column:
            :return: Dataframe
        """
        dataframe[column] = dataframe[column].replace(r"[^0-9]+", "", regex=True)
        return dataframe
