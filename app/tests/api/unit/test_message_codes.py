import pytest

from app.core.middleware.get_accept_language_middleware import (
    _request_accept_language_var,
)
from app.utils.message_codes import MessageCodes


@pytest.mark.asyncio
class TestMessageCodes:
    async def test_accept_language_en(self) -> None:
        test_case = "da, en-gb;q=0.8, fa;q=0.7"
        _request_accept_language_var.set(test_case)

        response_message = MessageCodes.get_message(MessageCodes.successful_operation)
        assert response_message == MessageCodes.english_messages_names[MessageCodes.successful_operation]

    async def test_accept_language_fa(self) -> None:
        test_case = "da, es;q=0.8, fa;q=0.7"
        _request_accept_language_var.set(test_case)

        response_message = MessageCodes.get_message(MessageCodes.input_error)
        assert response_message == MessageCodes.persian_message_names[MessageCodes.input_error]

    async def test_accept_language_default(self) -> None:
        test_case = "de; q=1.0, es; q=0.5"
        _request_accept_language_var.set(test_case)

        response_message = MessageCodes.get_message(MessageCodes.not_found)
        assert response_message == MessageCodes.persian_message_names[MessageCodes.not_found]
