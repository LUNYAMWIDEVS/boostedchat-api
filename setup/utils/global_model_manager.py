from django.db import models

class DefaultSelectOrPrefetchManager(models.Manager):
    """
    This is for forcing foreign key fields on each model and helps if there are lots
    of relationships and you have the `depth` variable set on your Serializer classes.
    See the README for more info on usage.
    See the StackOverflow question: https://stackoverflow.com/questions/59358079/is-it-possible-to-automatically-create-viewsets-and-serializers-for-each-model
    """
    def __init__(self, *args, **kwargs):
        self._select_related = kwargs.pop('select_related', None)
        self._prefetch_related = kwargs.pop('prefetch_related', None)

        super(DefaultSelectOrPrefetchManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(DefaultSelectOrPrefetchManager, self).get_queryset(*args, **kwargs)
        
        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)

        return qs