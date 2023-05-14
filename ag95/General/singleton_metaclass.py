from multiprocessing import Manager

class Singleton_with_cache(type):
    '''
    Class which acts as a Singleton if used as a metaclass;
    It is thread safe, NOT process safe.
    This flavor contains a shared cache among all the instances.
    The shared cache can trigger some strange errors, so if you have those errors you should use Singleton_without_cache.
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if 'shared_cache' not in cls._instances.keys():
            cls._instances['shared_cache'] = Manager().dict()

        if cls not in cls._instances:
            cls.shared_cache = cls._instances['shared_cache']
            cls._instances[cls] = super(Singleton_with_cache, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

class Singleton_without_cache(type):
    '''
    Class which acts as a Singleton if used as a metaclass;
    It is thread safe, NOT process safe.
    This flavor does NOT contain a shared cache among all the instances.
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_without_cache, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

if __name__ == '__main__':
    # check the basic functionality
    for metaclass in [Singleton_without_cache, Singleton_with_cache]:
        class MyClass1(metaclass=metaclass):
            def __init__(self,
                         number):
                self.number = number

            def print_next_value(self):
                self.number += 1
                return self.number

        my_obj_1 = MyClass1(2)
        result = my_obj_1.print_next_value()
        assert result == 3, f'wrong value returned ! expected  {3}, got {result}'
        result = my_obj_1.print_next_value()
        assert result == 4, f'wrong value returned ! expected  {4}, got {result}'

        my_obj_1 = MyClass1(20) # this is ignored as MyClass1 was already initialised with a singleton metaclass
        result = my_obj_1.print_next_value()
        assert result == 5, f'wrong value returned ! expected  {5}, got {result}'
        result = my_obj_1.print_next_value()
        assert result == 6, f'wrong value returned ! expected  {6}, got {result}'

    # check the shared cache functionality
    class MyClass1(metaclass=Singleton_with_cache):
        def __init__(self,
                     number):
            self.shared_cache['class1_number'] = number

    class MyClass2(metaclass=Singleton_with_cache):
        def __init__(self,
                     number):
            self.shared_cache['class2_number'] = number

    my_obj_1 = MyClass1(2)
    result = str(my_obj_1.shared_cache)
    expected = str({'class1_number': 2})
    assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    my_obj_2 = MyClass2(20) # this is ignored as MyClass1 was already initialised with a singleton metaclass
    result = str(my_obj_2.shared_cache)
    expected = str({'class1_number': 2, 'class2_number': 20})
    assert result == expected, f'wrong value returned ! expected  {expected}, got {result}'

    print('All tests are PASSED !')