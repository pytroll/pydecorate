try:
    from .version import version as __version__  # noqa
except ImportError:
    # package is not installed
    pass

from pydecorate.decorator_agg import DecoratorAGG  # noqa
