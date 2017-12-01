from types import ModuleType


def test_import():
    import objectstore

    assert isinstance(objectstore, ModuleType)
