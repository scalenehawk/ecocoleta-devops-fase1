"""Rotas HTTP da API EcoColeta para AWS Lambda."""

import json
import os
import uuid


MATERIAIS = {"papel", "plástico", "vidro", "metal", "eletrônicos"}


def _resposta(status, dados):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json; charset=utf-8"},
        "body": json.dumps(dados, ensure_ascii=False),
    }


def _validar_ponto(dados):
    if not isinstance(dados, dict):
        return "O corpo da requisição deve ser um objeto JSON."
    if not isinstance(dados.get("nome"), str) or not dados["nome"].strip():
        return "Informe o nome do ponto."
    if not isinstance(dados.get("bairro"), str) or not dados["bairro"].strip():
        return "Informe o bairro."
    materiais = dados.get("materiais")
    if not isinstance(materiais, list) or not materiais:
        return "Informe ao menos um material."
    if any(not isinstance(item, str) or item not in MATERIAIS for item in materiais):
        return "Há um material não reconhecido."
    return None


def tratar(evento, repositorio, gerador_id=None):
    """Processa eventos HTTP API v2 com um repositório injetado para testes."""
    gerador_id = gerador_id or (lambda: str(uuid.uuid4()))
    contexto = evento.get("requestContext", {}).get("http", {})
    metodo = contexto.get("method", "")
    caminho = evento.get("rawPath", "")

    if caminho == "/pontos" and metodo == "GET":
        material = (evento.get("queryStringParameters") or {}).get("material")
        if material is not None and material not in MATERIAIS:
            return _resposta(400, {"erro": "Material não reconhecido."})
        return _resposta(200, {"pontos": repositorio.listar(material)})

    if caminho == "/pontos" and metodo == "POST":
        try:
            dados = json.loads(evento.get("body") or "")
        except (json.JSONDecodeError, TypeError):
            return _resposta(400, {"erro": "JSON inválido."})
        erro = _validar_ponto(dados)
        if erro:
            return _resposta(400, {"erro": erro})
        ponto = {
            "id": gerador_id(),
            "nome": dados["nome"].strip(),
            "bairro": dados["bairro"].strip(),
            "materiais": sorted(set(dados["materiais"])),
        }
        repositorio.salvar(ponto)
        return _resposta(201, ponto)

    return _resposta(404, {"erro": "Rota não encontrada."})


def handler(evento, _contexto):
    from .repository import DynamoRepository

    tabela = os.environ["TABLE_NAME"]
    return tratar(evento, DynamoRepository(tabela))
