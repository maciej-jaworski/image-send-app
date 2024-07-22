from chat.forms import MessageForm
from chat.image_api import GetImageException, get_new_image
from chat.models import Chat
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView


class SendBannerMessageView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "chat/send_banner_message.html"
    form_class = MessageForm

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form: MessageForm):
        try:
            image = get_new_image()
        except GetImageException as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)

        form.save(commit=False)
        form.instance.image = image
        form.save(commit=True)

        form.instance.chats.add(*Chat.objects.values_list("id", flat=True))

        messages.success(self.request, "Message sent")

        return redirect(reverse("admin:index"))
