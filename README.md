# EcoColeta - API de pontos de coleta

Projeto da Fase 1 de DevOps na Prática. A API recebe e consulta pontos de coleta seletiva. O código da aplicação, os testes, o fluxo de integração contínua e a infraestrutura estão separados para permitir revisão e evolução.

Repositório: https://github.com/scalenehawk/ecocoleta-devops-fase1

## Escopo

- `GET /pontos?material=papel`: lista os pontos, com filtro opcional por material.
- `POST /pontos`: cadastra um ponto com nome, bairro e materiais aceitos.
- Persistência planejada em Amazon DynamoDB.
- Execução planejada em AWS Lambda, exposta por API Gateway HTTP API.

O ambiente AWS não foi criado. O template CloudFormation e o script de empacotamento estão prontos para revisão; executar o provisionamento exige uma conta AWS e a decisão do responsável sobre custos e região.

## Executar testes

Requer Python 3.13 ou superior. Não há dependências externas para executar os testes.

```bash
python -m unittest discover -s tests -v
```

## Estrutura

- `src/app.py`: validação, rotas e respostas HTTP.
- `src/repository.py`: acesso à tabela DynamoDB.
- `tests/`: casos de sucesso e erro com repositório em memória.
- `.github/workflows/ci.yml`: testes, verificação sintática e validação do CloudFormation a cada push e pull request.
- `infra/template.yaml`: recursos de API Gateway, Lambda, DynamoDB e permissões.
- `scripts/package.py`: gera o ZIP da função Lambda para publicação em S3.
- `scripts/check_package.py`: verifica a integridade e o conteúdo do pacote gerado.

## Publicação

1. Executar os testes locais e revisar o template.
2. Criar um bucket S3 para armazenar `lambda.zip`.
3. Executar `python scripts/package.py` e enviar o artefato ao bucket.
4. Implantar `infra/template.yaml` com os parâmetros `ArtifactBucket` e `ArtifactKey`.
5. Confirmar o endpoint gerado pela pilha e testar as rotas.

Os passos 2 a 5 são planos de implantação; não foram executados neste projeto.
