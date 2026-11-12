"""Empacota a aplicação e o boto3 para a função Lambda."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "dist" / "lambda.zip"


def main():
    DESTINO.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporario:
        pasta = Path(temporario)
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--quiet", "--target", str(pasta),
            "boto3>=1.35,<2"
        ], check=True)
        shutil.copytree(RAIZ / "src", pasta / "src")
        with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED) as arquivo:
            for caminho in sorted(pasta.rglob("*")):
                if caminho.is_file():
                    arquivo.write(caminho, caminho.relative_to(pasta).as_posix())
    print(DESTINO)


if __name__ == "__main__":
    main()
