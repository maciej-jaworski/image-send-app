from chat import models
from chat.views import SendBannerMessageView
from django.contrib import admin
from django.utils.safestring import mark_safe

admin.site.register_view(
    "send-banner-message/",
    urlname="send-banner-message",
    name="Send message to all users",
    view=SendBannerMessageView.as_view(),
)


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_file",
    )


admin.site.register(models.Image, ImageAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "text",
    )


admin.site.register(models.Message, MessageAdmin)


class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ("rendered_messages",)
    list_display = (
        "created_at",
        "user",
    )
    fields = (
        "user",
        "rendered_messages",
    )

    def rendered_messages(self, instance: models.Chat):
        output = ""
        for msg in instance.messages.select_related("image"):
            image = (
                f'<img width="300" src="{msg.image.image_file.url}"/>'
                if msg.image
                else "No Image"
            )
            output += f"""<tr>
            <td>{msg.created_at.strftime('%c')}</td>
            <td>{msg.text}</td>
            <td>{image}</td>
            </tr>"""

        if output:
            # This is just for easy debugging, normally shouldn't use mark safe on things that users input
            return mark_safe(
                f"""<table>
            <tr>
            <th>Timestamp</th>
            <th>Text</th>
            <th>Image</th>
            </tr>
            {output}
            </table>"""
            )

        return "No messages"


admin.site.register(models.Chat, ChatAdmin)
