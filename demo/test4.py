class Descriptor:

    def __get__(self, instance, owner):
        if instance is None:
            print('__get__(): Accessing x from the class', owner)
            return self

        print('__get__(): Accessing x from the object', instance)
        return 'X from descriptor'

    def __set__(self, instance, value):
        print('__set__(): Setting x on the object', instance)
        instance.__dict__['_x'] = value


class Foo:
    x = Descriptor()


Foo().x = 1
