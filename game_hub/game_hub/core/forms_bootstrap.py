class BootstrapFormMixin:
    """
    About Bootstrap
    The class append  form-control class on every field in form which inherit it.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_fields()

    def _init_bootstrap_fields(self):
        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'