from django.forms.widgets import CheckboxSelectMultiple


class PillBoxSelectMultiple(CheckboxSelectMultiple):
    option_template_name = 'widgets/pill_box_option.html'
