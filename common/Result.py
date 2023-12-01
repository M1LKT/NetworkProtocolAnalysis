class Result:
    CODE_SUCCESS = "200"
    CODE_AUTH_ERROR = "401"
    CODE_SYS_ERROR = "500"

    __msg=''
    __code=''
    __data=''


    def __init__(self, msg, code,data):
        self.__code = code
        self.__data = data
        self.__msg=msg


    def to_dict(self):
        return {
            "msg": self.__msg,
            "code": self.__code,
            "data": self.__data,
        }



    @staticmethod
    def success(data):
        msg='请求成功'
        return Result(msg, Result.CODE_SUCCESS, data).to_dict()

