"""Persistência dos pontos de coleta em DynamoDB."""

import boto3


class DynamoRepository:
    def __init__(self, nome_tabela):
        self.tabela = boto3.resource("dynamodb").Table(nome_tabela)

    def salvar(self, ponto):
        self.tabela.put_item(Item=ponto)

    def listar(self, material=None):
        # A paginação evita omitir registros quando a tabela supera 1 MB.
        itens = []
        parametros = {}
        while True:
            resposta = self.tabela.scan(**parametros)
            itens.extend(resposta.get("Items", []))
            chave = resposta.get("LastEvaluatedKey")
            if not chave:
                break
            parametros["ExclusiveStartKey"] = chave
        if material:
            itens = [item for item in itens if material in item.get("materiais", [])]
        return sorted(itens, key=lambda item: (item.get("bairro", ""), item.get("nome", "")))
