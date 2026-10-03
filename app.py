import sys

import uvicorn

# Impede a criação de __pycache__ e arquivos .pyc (deve vir antes de qualquer import do projeto)
sys.dont_write_bytecode = True

from app.main import create_app  # noqa: E402

HOST_DEFAULT = "0.0.0.0"
PORT_DEFAULT = 7000

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:create_app", factory=True, host=HOST_DEFAULT, port=PORT_DEFAULT, reload=False)
