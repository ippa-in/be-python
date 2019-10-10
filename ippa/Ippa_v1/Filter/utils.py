from django.db.models.fields.related import ForeignKey

def get_foreign_keys(model):
    select_related = list()
    model_attrs = model._meta.get_fields()
    for attr in model_attrs:
        if isinstance(attr, ForeignKey):
            select_related.append(attr.name)
    return select_related