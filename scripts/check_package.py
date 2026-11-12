"""Confere se o pacote Lambda contém os arquivos necessários para execução."""

from pathlib import Path
from zipfile import ZipFile


PACOTE = Path(__file__).resolve().parents[1] / "dist" / "lambda.zip"
ARQUIVOS_OBRIGATORIOS = {
    "src/__init__.py",
    "src/app.py",
    "src/repository.py",
    "boto3/__init__.py",
}


def main():
    if not PACOTE.is_file():
        raise SystemExit(f"Pacote ausente: {PACOTE}")
    with ZipFile(PACOTE) as arquivo:
        corrompido = arquivo.testzip()
        if corrompido:
            raise SystemExit(f"Arquivo inválido no pacote: {corrompido}")
        ausentes = ARQUIVOS_OBRIGATORIOS - set(arquivo.namelist())
        if ausentes:
            raise SystemExit(f"Arquivos ausentes: {', '.join(sorted(ausentes))}")
    print("Pacote Lambda íntegro e com os arquivos obrigatórios.")


if __name__ == "__main__":
    main()
