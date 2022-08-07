from functools import wraps


__all__ = (
    "NameAlreadyRegistered",
    "Registry",
)


class NameAlreadyRegistered(Exception):
    pass


class Registry:
    def __init__(self, name):
        super().__setattr__("_name", name)
        super().__setattr__("_elements", set())

    def __repr__(self):
        return f"<{self._name.capitalize()} Registry>"

    def register(self, cls=None, name=None, replace=False):
        if cls is None:

            @wraps(self.register)
            def _cls_decorator(cls):
                # Allow user to set register as class decorator with arguments
                # e.g:
                # >>> @registry.register(name="TaskName", replace=True)
                # >>> class ReplaceTaskNameTask:
                # >>>     pass
                self.register(cls, name=name, replace=replace)
                return cls

            return _cls_decorator

        if name is None:
            name = cls.__name__

        if name in self._elements and not replace:
            raise NameAlreadyRegistered(f"{name} is already present in registry")

        super().__setattr__(name, cls)
        self._elements.add(name)

        return cls

    def get(self, name):
        return getattr(self, name)

    def builder(self, cls, name, bases, dct):
        result = type.__new__(cls, name, bases, dct)
        self.register(
            result,
            name=dct.get("_registry_name", None),
            replace=dct.get("_registry_replace_existing", False),
        )
        return result

    def __setattr__(self, name, value):
        raise NotImplementedError()

    def __instancecheck__(self, instance):
        for name in self._elements:
            if isinstance(instance, getattr(self, name)):
                return True
        return False

    def __iter__(self):
        for name in self._elements:
            yield getattr(self, name)


class RegisteringMeta(type):
    def __new__(cls, name, registry=None):
        return type(f"{name}Meta", (type,), cls._get_attributes(registry))

    @staticmethod
    def _get_attributes(registry: Registry) -> dict:
        if registry is None:
            registry = Registry()

        return {
            "__new__": registry.builder,
            "get": registry.get,
            "register": registry.register,
        }
