from functools import wraps, lru_cache


def lru_cache_factory(hash_func):
    """Return a function decorator that lets functools.lru_cache work with
    unhashable objects without actually adding a __hash__ function to them.

    This may be useful if you:
        - wish to override an existing __hash__ function only when cacheing
        the object
        - do not wish to add a __hash__ function to the object being cached

    `hash_func` - defines how to hash the object(s) you care about.
    """
    @wraps(lru_cache)
    def mlru_cache(*args, **kwargs):
        """
        An lru cache for mutable objects
        """

        def _mlru_cache(func):
            """the actual decorator"""

            @lru_cache(*args, **kwargs)
            def cached_func(*args3, **kwargs3):
                """calls cached_func.f(), where f() is
                assumed to be defined in another scope"""
                return cached_func.f()

            @wraps(func)
            def _func(*args2, **kwargs2):
                # convert args to immutable args we can use in the lru_cache
                args3 = tuple(hash_func(a) for a in args2)
                kwargs3 = {k: hash_func(v) for k, v in kwargs2.items()}

                def f(): return func(*args2, **kwargs2)
                cached_func.f = f
                return cached_func(*args3, **kwargs3)

            # add lru_cache methods
            for k, v in vars(cached_func).items():
                if k.startswith('cache_'):
                    setattr(_func, k, v)
            return _func
        return _mlru_cache
    return mlru_cache
