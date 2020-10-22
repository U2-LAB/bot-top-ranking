from django.db import models


class Chat(models.Model):
    telegram_chat_id = models.IntegerField()

    def __str__(self):
        return 'Chat #%d' % (self.telegram_chat_id)


class Poll(models.Model):
    poll_telegram_id = models.IntegerField()
    chat_id = models.ForeignKey('Chat', related_name='polls', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%d : %s' % (self.poll_telegram_id, self.chat_id)


class Song(models.Model):
    poll_id = models.ForeignKey('Poll', related_name='songs', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    mark = models.IntegerField()

    def __str__(self):
        return '%s : %s : %d' % (self.poll_id, self.title, self.mark)
