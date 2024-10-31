# pylint: disable=line-too-long
# flake8: noqa: E501

from typing import Any

from flask import jsonify


class Response:
    """
        A classe Response é utilizada para padronizar as respostas de uma aplicação web.
        Ela encapsula informações sobre o status da resposta, código de erro, mensagem e dados retornados.
        A classe também fornece métodos para verificar se a resposta foi bem-sucedida ou se ocorreu um erro,
        além de métodos estáticos para criar instâncias de respostas de sucesso ou erro.
    """

    def __init__(
        self,
        status: int = None,
        code: str = None,
        message: str = None,
        data: Any = None
    ):
        """
        Inicializa uma nova instância da classe Response.

        Args:
            status (int, opcional): O status da resposta. Padrão é None.
            code (str, opcional): O código da resposta. Padrão é None.
            message (str, opcional): A mensagem da resposta. Padrão é None.
            data (Any, opcional): Dados adicionais da resposta. Padrão é None.
        """
        self.status = status
        self.code = code
        self.message = message
        self.data = data

    def result(self):
        """
        Retorna uma resposta JSON baseada no estado do objeto.
        tuple: Uma tupla contendo a resposta JSON e o status HTTP.
        """
        if (self.errored()):
            return jsonify({
                "code":  self.code,
                "message":  self.message,
            }), self.status
        return jsonify({"data": self.data}), self.status

    def successed(self) -> bool:
        """
        Verifica se a resposta foi bem-sucedida.

        Retorna:
            bool: True se o código e a mensagem forem None e o status estiver entre 200 e 299, False caso contrário.
        """
        return (
            self.code is None and
            self.message is None and
            self.status < 300 and
            self.status >= 200
        )

    def errored(self) -> bool:
        """
        Verifica se a resposta contém um erro.

        Retorna:
            bool: True se o código e a mensagem estiverem definidos e o status for maior ou igual a 400, indicando um erro. Caso contrário, False.
        """
        return (
            self.code is not None and
            self.message is not None and
            self.status >= 400
        )

    def is_ok(self) -> bool:
        """
        Verifica se a operação foi bem-sucedida.

        Retorna:
            bool: True se a operação foi bem-sucedida, False caso contrário.
        """
        return self.successed()

    @staticmethod
    def error(status: int, code: str, message: str):
        """
        Método estático para gerar uma resposta de erro.

        Args:
            status (int): Código de status HTTP.
            code (str): Código de erro específico.
            message (str): Mensagem descritiva do erro.

        Returns:
            Response: Objeto de resposta contendo o status, código e mensagem de erro.
        """
        return Response(status, code, message, None)

    @staticmethod
    def success(status: int, data: Any):
        """
        Método estático que cria uma resposta de sucesso.

        Args:
            status (int): Código de status HTTP da resposta.
            data (Any): Dados a serem incluídos na resposta.

        Returns:
            Response: Objeto de resposta contendo o status e os dados fornecidos.
        """
        return Response(status, None, None, data)
