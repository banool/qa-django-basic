from .models import Question
from django import forms
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
from ratelimit.decorators import ratelimit

import logging

logger = logging.getLogger(__name__)


def index(request):
    questions_all = Question.objects.order_by('-answer_date')
    questions = [q for q in questions_all if q.answer]
    unanswered = len([q for q in questions_all if not q.answer])
    context = {
        'questions': questions,
        'unanswered': unanswered,
    }
    return render(request, 'qa/index.html', context)


class AskForm(forms.Form):
    question = forms.CharField(
        label='',  # The question text is in the template instead.
        widget=forms.Textarea,
        max_length=500,
    )


@ratelimit(key='ip', rate='2/m', method=ratelimit.UNSAFE)
def ask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return HttpResponseRedirect('/limited')
        # create a form instance and populate it with data from the request:
        form = AskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Question.objects.create(
                question=form.cleaned_data['question'],
                answer=None,
                ask_date=now(),
                answer_date=None,
            )
            # TODO What if I gave them an option to be notified when I respond.
            email = EmailMessage(
                'Question received!',
                'A question has been received on the Q & A thingy!',
                to=['danielporteous1@gmail.com']
            )
            email.send()
            return HttpResponseRedirect('/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AskForm()

    return render(request, 'qa/ask.html', {'form': form})


def thanks(request):
    context = {}
    return render(request, 'qa/thanks.html', context)


def limited(request):
    context = {}
    return render(request, 'qa/limited.html', context)
