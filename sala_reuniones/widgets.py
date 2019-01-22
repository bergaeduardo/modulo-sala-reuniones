from django import forms
from django.conf import settings


class DatePicker(forms.DateInput):
    class Media:
        css = {
            'all': ('%scss/datepicker.min.css' % settings.STATIC_URL,)
        }
        js = ('%sjs/bootstrap-datepicker.min.js' % settings.STATIC_URL,
              '%sjs/bootstrap-datepicker.es.js' % settings.STATIC_URL
              )


class TimePicker(forms.TimeInput):
    class Media:
        css = {
            'all': ('%scss/jquery-clockpicker.min.css' % settings.STATIC_URL,)
        }
        js = ('%sjs/jquery-clockpicker.min.js' % settings.STATIC_URL,)
