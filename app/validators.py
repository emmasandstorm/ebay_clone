class RequiredIf(object):
    def __init__(self, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        if form.data.get(field.name) == "None":
            for name, value in self.conditions:
                if name not in form.data:
                    continue
                condition = form.data.get(name)
                if value == condition:
                    raise Exception(
                        f"{field.name} field is required when {name} field is {condition}"
                    )
