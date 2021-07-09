# -*- coding: utf-8 -*-
from django.forms.utils import flatatt
from django.forms.widgets import DateTimeInput
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

try:
    import json
except ImportError:
    from django.utils import simplejson as json
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:  # python3
    from django.utils.encoding import force_text


class DateTimePicker(DateTimeInput):
    class Media:
        class JsFiles(object):
            def __iter__(self):
                yield 'js/plugins/moment.min.js'
                yield 'js/plugins/bootstrap-datetimepicker.js'
                lang = translation.get_language()
                if lang:
                    lang = lang.lower()
                    #There is language name that length>2 *or* contains uppercase.
                    lang_map = {
                        'ar-ma': 'ar-ma',
                        'en-au': 'en-au',
                        'en-ca': 'en-ca',
                        'en-gb': 'en-gb',
                        'en-us': 'en-us',
                        'fa-ir': 'fa-ir',
                        'fr-ca': 'fr-ca',
                        'ms-my': 'ms-my',
                        'pt-br': 'bt-BR',
                        'rs-latin': 'rs-latin',
                        'tzm-la': 'tzm-la',
                        'tzm': 'tzm',
                        'zh-cn': 'zh-CN',
                        'zh-tw': 'zh-TW',
                        'zh-hk': 'zh-TW',
                    }
                    if len(lang) > 2:
                        lang = lang_map.get(lang, 'en-us')
                    if lang not in ('en', 'en-us'):
                        yield 'bootstrap4_datetime/js/locales/bootstrap-datetimepicker.%s.js' % (lang)

        js = JsFiles()
        css = {}

    # http://momentjs.com/docs/#/parsing/string-format/
    # http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    format_map = (('DDD', r'%j'),
                  ('DD', r'%d'),
                  ('MMMM', r'%B'),
                  ('MMM', r'%b'),
                  ('MM', r'%m'),
                  ('YYYY', r'%Y'),
                  ('YY', r'%y'),
                  ('HH', r'%H'),
                  ('hh', r'%I'),
                  ('mm', r'%M'),
                  ('ss', r'%S'),
                  ('a', r'%p'),
                  ('ZZ', r'%z'),
    )

    @classmethod
    def conv_datetime_format_py2js(cls, format):
        for js, py in cls.format_map:
            format = format.replace(py, js)
        return format

    @classmethod
    def conv_datetime_format_js2py(cls, format):
        for js, py in cls.format_map:
            format = format.replace(js, py)
        return format

    html_template = '''
        <div%(div_attrs)s>
            <input%(input_attrs)s class="form-control datetimepicker" />
            
        </div>'''


    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, icon_attrs=None):
        if not div_attrs:
            div_attrs = {'class': 'form-group'}
        if format is None and options and options.get('format'):
            format = self.conv_datetime_format_js2py(options.get('format'))
        super(DateTimePicker, self).__init__(attrs, format)
        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'
        self.div_attrs = div_attrs and div_attrs.copy() or {}
        self.icon_attrs = icon_attrs and icon_attrs.copy() or {}
        if options == False:  # datetimepicker will not be initalized only when options is False
            self.options = False
        else:
            self.options = options and options.copy() or {}
            if format and not self.options.get('format') and not self.attrs.get('date-format'):
                self.options['format'] = self.conv_datetime_format_py2js(format)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        input_attrs = dict([(key, conditional_escape(val)) for key, val in input_attrs.items()])  # python2.6 compatible
        div_attrs = dict(
            [(key, conditional_escape(val)) for key, val in self.div_attrs.items()])  # python2.6 compatible

        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         input_attrs=flatatt(input_attrs))

        return mark_safe(force_text(html))
