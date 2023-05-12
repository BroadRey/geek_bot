from typing import Union

from aiogram import filters, types


class IsGroupChat(filters.BoundFilter):
    async def check(self, event: Union[types.Message, types.CallbackQuery]):
        if isinstance(event, types.Message):
            return event.chat.type !=  types.ChatType.PRIVATE

        return event.message.chat.type !=  types.ChatType.PRIVATE
