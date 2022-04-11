from datetime import datetime


class RespCode:
    SUCCESS = 200
    FAIL = 400
    AUTH_FAIL = 401
    NOT_FOUND = 404
    ERROR = 500


dict_code_mapping = {
    200: 'success',
    400: 'fail',
    401: 'auth_fail',
    404: 'not_found',
    500: 'error'
}

class Resp():
    def __init__(self, code=RespCode.SUCCESS, msg='', result={}):
        self.dict_response = {
            'code': code,
            'status': dict_code_mapping[code],
            'time': str(datetime.now()),
            'msg': msg,
            'result': result,
        }

    def dict(self):
        return self.dict_response