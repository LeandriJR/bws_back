class ValidationError(Exception):

    def __init__(self, mensagem: str = None, status_code: int = 200, retorno=None):
        self.__mensagem = mensagem
        self.__retorno = retorno
        self.__status_code = status_code
        super().__init__(self.__mensagem)

    @property
    def retorno(self):
        return self.__retorno

    @property
    def mensagem(self):
        return self.__mensagem

    @property
    def status_code(self):
        return self.__status_code

