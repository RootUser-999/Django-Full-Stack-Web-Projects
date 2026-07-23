import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
   

    

    async def connect(self):
        print("=" * 60)
        print("CHAT CONSUMER CONNECT CALLED")
        print("=" * 60)

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]

        self.room_group_name = f"chat_{self.conversation_id}"

        self.user = self.scope["user"]

        # User must be authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Verify user belongs to this conversation
        allowed = await self.user_can_join()

        if not allowed:
            await self.close()
            return
        print("BEFORE GROUP_ADD")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print("AFTER GROUP_ADD")
        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data.get("message", "").strip()

        if not message:
            return

        # Save message
        saved_message = await self.save_message(message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender": saved_message.sender.username,
                "sender_id": saved_message.sender.id,
                "created_at": saved_message.created_at.strftime("%b %d, %Y %H:%M"),
            }
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
                "sender_id": event["sender_id"],
                "created_at": event["created_at"],
            })
        )

    @database_sync_to_async
    def user_can_join(self):

        try:

            conversation = Conversation.objects.select_related(
                "buyer",
                "seller",
                "listing",
            ).get(
                id=self.conversation_id
            )

            return (
                conversation.buyer == self.user
                or conversation.seller == self.user
            )

        except Conversation.DoesNotExist:

            return False

    @database_sync_to_async
    def save_message(self, message):

        conversation = Conversation.objects.get(
            id=self.conversation_id
        )

        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=message,
        )