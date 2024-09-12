class MultiSerializerClassViewMixin:
    """
    Multiple Serializers can be defined for a View using this Mixin.
    serializer_classes:
        Takes a dict as input with actions defined as keys and the respective serializer to use as their values
    """
    serializer_classes = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)
