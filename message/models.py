from django.db import models


class Messagefromsky(models.Model):
    date = models.DateField("Дата", auto_now_add=True)
    text = models.TextField("Текст")
    seen = models.BooleanField("Прочитано")

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "СообщенииИзКосмоса"
        verbose_name = "СообщенияИзКосмоса"
