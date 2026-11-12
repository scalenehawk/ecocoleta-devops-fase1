import json
import unittest

from src.app import tratar


class RepositorioMemoria:
    def __init__(self):
        self.pontos = []

    def salvar(self, ponto):
        self.pontos.append(ponto)

    def listar(self, material=None):
        if material:
            return [p for p in self.pontos if material in p["materiais"]]
        return list(self.pontos)


def evento(metodo, caminho="/pontos", corpo=None, consulta=None):
    return {
        "requestContext": {"http": {"method": metodo}},
        "rawPath": caminho,
        "body": corpo,
        "queryStringParameters": consulta,
    }


class TestarRotas(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioMemoria()

    def test_cadastra_ponto_e_retira_duplicatas(self):
        corpo = json.dumps({"nome": "  Ecoponto Central ", "bairro": " Centro ", "materiais": ["papel", "vidro", "papel"]})
        resposta = tratar(evento("POST", corpo=corpo), self.repo, lambda: "p-001")
        self.assertEqual(resposta["statusCode"], 201)
        self.assertEqual(json.loads(resposta["body"]), {
            "id": "p-001", "nome": "Ecoponto Central", "bairro": "Centro", "materiais": ["papel", "vidro"]
        })

    def test_lista_filtrada_por_material(self):
        self.repo.pontos = [
            {"id": "1", "nome": "A", "bairro": "Centro", "materiais": ["papel"]},
            {"id": "2", "nome": "B", "bairro": "Centro", "materiais": ["vidro"]},
        ]
        resposta = tratar(evento("GET", consulta={"material": "papel"}), self.repo)
        self.assertEqual([p["id"] for p in json.loads(resposta["body"])["pontos"]], ["1"])

    def test_rejeita_json_invalido(self):
        resposta = tratar(evento("POST", corpo="{"), self.repo)
        self.assertEqual(resposta["statusCode"], 400)
        self.assertEqual(self.repo.pontos, [])

    def test_rejeita_material_desconhecido(self):
        corpo = json.dumps({"nome": "Ponto", "bairro": "Centro", "materiais": ["óleo"]})
        resposta = tratar(evento("POST", corpo=corpo), self.repo)
        self.assertEqual(resposta["statusCode"], 400)

    def test_rejeita_nome_vazio(self):
        corpo = json.dumps({"nome": " ", "bairro": "Centro", "materiais": ["papel"]})
        self.assertEqual(tratar(evento("POST", corpo=corpo), self.repo)["statusCode"], 400)

    def test_rota_inexistente(self):
        self.assertEqual(tratar(evento("GET", "/outra"), self.repo)["statusCode"], 404)

    def test_rejeita_filtro_invalido(self):
        self.assertEqual(tratar(evento("GET", consulta={"material": "óleo"}), self.repo)["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
