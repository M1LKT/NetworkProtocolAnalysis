class Result:
    """
    Represents the result of an operation.

    Attributes:
        CODE_SUCCESS (str): The success code.
        CODE_AUTH_ERROR (str): The authentication error code.
        CODE_SYS_ERROR (str): The system error code.
    """

    CODE_SUCCESS = "200"
    CODE_AUTH_ERROR = "401"
    CODE_SYS_ERROR = "500"

    __msg=''
    __code=''
    __data=''


    def __init__(self, msg, code, data):
        self.__code = code
        self.__data = data
        self.__msg = msg


    def to_dict(self):
        """
        Converts the result to a dictionary.

        Returns:
            dict: The result as a dictionary.
        """
        return {
            "msg": self.__msg,
            "code": self.__code,
            "data": self.__data,
        }



    @staticmethod
    def success(msg='请求成功',data='null'):
        """
        创建一个success类型的Result对象。

        Args:
            data (str，可选):与结果相关联的数据。默认为'null'。

        Returns:
            返回一个字典对象，包含success类型的Result对象。
        """
        return Result(msg, Result.CODE_SUCCESS, data).to_dict()
      
    @staticmethod
    def error(msg, code=CODE_SYS_ERROR, data='null'):
        """
        创建一个error类型的Result对象。

        Args:
            msg (str):错误消息。
            code (str，可选):错误码。默认为CODE_SYS_ERROR。
            data (str，可选):与结果相关联的数据。默认为'null'。


        Returns:
            返回一个字典对象，包含error类型的Result对象。
        """
        return Result(msg, code, data).to_dict()
    
