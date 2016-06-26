class QuerysetCache(object):
    """
    This class caches a queryset and provides additional functionality to work with the cached queryset
    """
    def __init__(self, queryset):
        """
        Initialized with the queryset which should be cached

        :param queryset: queryset to be cached
        """
        self.queryset = list(queryset)

    def map_by_attribute(self, attribute, unique=False):
        """
        Creates a dict which maps the elements in the queryset by the given attribute. The resulting map is added as an
        attribute to the QuerysetCache object and is returned by this method.

        :param attribute: the name of the attribute which should be the key for resulting map
        :type attribute: str
        :param unique:  set if the given attribute is unique. If it isn't, the values are stored in a list, to allow for
                        multiple values
        :type unique: bool
        :return: resulting map
        :rtype: dict<type(attribute), object> | dict<type(attribute), list<object>>
        """
        map = {}

        for element in self.queryset:
            key = getattr(element, attribute)

            if unique:
                map[key] = element
            else:
                if key in map:
                    map.get(key).append(element)
                else:
                    map[key] = [element,]

        setattr(self, '{attribute_name}_map'.format(attribute_name=attribute), map)

        return map
