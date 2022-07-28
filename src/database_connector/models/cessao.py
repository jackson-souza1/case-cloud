from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class CessaoModel(Model):
    class Meta:
        table_name = "cessao"

    ID_CESSAO = UnicodeAttribute(hash_key=True)
    ORIGINADOR = UnicodeAttribute(null=True)
    DOC_ORIGINADOR = UnicodeAttribute(null=True)
    CEDENTE = UnicodeAttribute(null=True)
    DOC_CEDENTE = UnicodeAttribute(null=True)
    CCB = UnicodeAttribute(null=True)
    ID_EXTERNO = UnicodeAttribute(range_key=True)
    CLIENTE = UnicodeAttribute(null=True)
    CPF_CNPJ = UnicodeAttribute(null=True)
    ENDERECO = UnicodeAttribute(null=True)
    CEP = UnicodeAttribute(null=True)
    CIDADE = UnicodeAttribute(null=True)
    UF = UnicodeAttribute(null=True)
    VALOR_DO_EMPRESTIMO = UnicodeAttribute(null=True)
    VALOR_PARCELA = UnicodeAttribute(null=True)
    TOTAL_PARCELAS = UnicodeAttribute(null=True)
    PARCELA = UnicodeAttribute(null=True)
    DATA_DE_EMISSAO = UnicodeAttribute(null=True)
    DATA_DE_VENCIMENTO = UnicodeAttribute(null=True)
    PRECO_DE_AQUISICAO = UnicodeAttribute(null=True)
