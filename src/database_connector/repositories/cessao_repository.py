from .base import BaseRepository
from models.cessao import CessaoModel
import uuid


class CessaoRepository(BaseRepository):
    def __init__(self) -> None:
        pass

    def create(self, data):
        id_cessao = str(uuid.uuid4())
        CessaoModel(
            ID_CESSAO=id_cessao,
            ORIGINADOR=data['originador'],
            DOC_ORIGINADOR=data['doc_originador'],
            CEDENTE=data['cedente'],
            DOC_CEDENTE=str(data['doc_cedente']),
            CCB=str(data['ccb']),
            ID_EXTERNO=data['id_externo'],
            CLIENTE=data['cliente'],
            CPF_CNPJ=data['cpf_cnpj'],
            ENDERECO=data['endereco'],
            CEP=str(data['cep']),
            CIDADE=data['cidade'],
            UF=data['uf'],
            VALOR_DO_EMPRESTIMO=data['valor_do_emprestimo'],
            VALOR_PARCELA=data['valor_parcela'],
            TOTAL_PARCELAS=str(data['total_parcelas']),
            PARCELA=str(data['parcela']),
            DATA_DE_EMISSAO=data['data_de_emissao'],
            DATA_DE_VENCIMENTO=data['data_de_vencimento'],
            PRECO_DE_AQUISICAO=str(data['preco_de_aquisicao'])

        ).save()
        return f"Registro inserido com sucesso: ID {id_cessao}"

    def update(self):
        pass

    def delete(self):
        pass

