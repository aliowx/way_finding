from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.utils import utils


class CustomResponse(JSONResponse):
    """
    Custom reponse class
    Adds custom header, messages to reponses
    """
    def __init__(self, data, msg_code=0, msg_status=0, **kwargs):
        """
        msg_status -> 0: successful -- 1: external error -- 2: internal error
        """
        response_data = {
            "Header": {
                "Status": msg_status,
                "MessageCode": msg_code,
                "Message": utils.MessageCodes.messages_names[msg_code],
                "PersianMessage": utils.MessageCodes.persian_messages_names[msg_code],
            },
            "ContentData": jsonable_encoder(data),
        }
        super().__init__(response_data, **kwargs)

    def __new__(cls, *args, **kwargs):
        """
        If response data is an instance of the main Response class
        then return the response without manipulating it to correctly
        process file, streaming and other types of responses passed
        """
        if args:
            if isinstance(args[0], Response):
                return args[0]
        return super().__new__(cls)
