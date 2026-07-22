from django import forms

from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message

        fields = ["content"]

        widgets = {

            "content": forms.TextInput(

                attrs={

                    "id": "chat-message-input",

                    "class": "form-control",

                    "placeholder": "Type your message...",

                    "autocomplete": "off",

                }

            )

        }