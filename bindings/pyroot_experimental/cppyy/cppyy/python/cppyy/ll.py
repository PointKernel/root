""" Low-level utilities, to be used for "emergencies only".
"""

import cppyy


__all__ = [
    'cast',
    'static_cast',
    'reinterpret_cast',
    'dynamic_cast',
    'malloc',
    'free',
    'array_new',
    'array_detele',
    ]


# import low-level python converters
for _name in ['addressof', 'as_cobject', 'as_capsule', 'as_ctypes']:
    try:
        exec('%s = cppyy._backend.%s' % (_name, _name))
        __all__.append(_name)
    except AttributeError:
        pass
del _name


# create low-level helpers
cppyy.cppdef("""namespace __cppyy_internal {
// type casting
    template<typename T, typename U>
    T cppyy_cast(U val) { return (T)val; }

    template<typename T, typename U>
    T cppyy_static_cast(U val) { return static_cast<T>(val); }

    template<typename T, typename U>
    T cppyy_reinterpret_cast(U val) { return reinterpret_cast<T>(val); }

    template<typename T, typename S>
    T* cppyy_dynamic_cast(S* obj) { return dynamic_cast<T*>(obj); }

// memory allocation/free-ing
    template<typename T>
    T* cppyy_malloc(size_t count=1) { return (T*)malloc(sizeof(T*)*count); }

    template<typename T>
    T* cppyy_array_new(size_t count) { return new T[count]; }

    template<typename T>
    void cppyy_array_delete(T* ptr) { delete[] ptr; }
}""")


# helper for sizing arrays
class ArraySizer(object):
    def __init__(self, func):
        self.func = func
    def __getitem__(self, t):
        self.array_type = t
        return self
    def __call__(self, size):
        res = self.func[self.array_type](size)
        res.reshape((size,))
        return res

# import casting helpers
cast             = cppyy.gbl.__cppyy_internal.cppyy_cast
static_cast      = cppyy.gbl.__cppyy_internal.cppyy_static_cast
reinterpret_cast = cppyy.gbl.__cppyy_internal.cppyy_reinterpret_cast
dynamic_cast     = cppyy.gbl.__cppyy_internal.cppyy_dynamic_cast

# import memory allocation/free-ing helpers
malloc           = ArraySizer(cppyy.gbl.__cppyy_internal.cppyy_malloc)
free             = cppyy.gbl.free      # for symmetry
array_new        = ArraySizer(cppyy.gbl.__cppyy_internal.cppyy_array_new)
array_delete     = cppyy.gbl.__cppyy_internal.cppyy_array_delete
