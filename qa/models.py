from django.db import models


class Question(models.Model):
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    ask_date = models.DateTimeField(null=True)
    answer_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        preview_len = 20
        if len(self.question):
            s = self.question[:preview_len]
            if len(self.question) > preview_len:
                s += '...'
            return s
        return str(self.ask_date)
