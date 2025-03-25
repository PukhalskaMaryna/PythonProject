class ErrorForMaxCount(Exception):
    """Виключення, коли група перевищує ліміт студентів"""
    def __init__(self, msg = "У групі може бути не більше 10 студентів"):
        self.msg = msg
        super().__init__(self.msg)