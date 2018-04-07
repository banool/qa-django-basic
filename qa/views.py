from .models import Question
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import localtime, now

import logging

logger = logging.getLogger(__name__)


def index(request):
    questions = Question.objects.order_by('-answer_date')
    questions = [q for q in questions if q.answer]
    context = {
        'questions': questions,
    }
    return render(request, 'qa/index.html', context)


class AskForm(forms.Form):
    question = forms.CharField(
        label='',  # The question text is in the template instead.
        widget=forms.Textarea,
        max_length=500,
    )


def ask(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Question.objects.create(
                question=form.cleaned_data['question'],
                answer=None,
                ask_date=localtime(now()).date(),
                answer_date=None,
            )
            # TODO What if I gave them an option to be notified when I respond.
            return HttpResponseRedirect('/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AskForm()

    return render(request, 'qa/ask.html', {'form': form})


def thanks(request):
    context = {}
    return render(request, 'qa/thanks.html', context)
