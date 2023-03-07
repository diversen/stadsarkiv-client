from stadsarkiv_client.hooks import hook_specs
from stadsarkiv_client.utils.logging import log
import pluggy
import inspect
import sys


try:
    import hooks
    log.info("Loaded local hooks: hooks.py")
except ImportError:
    log.info("Local hooks NOT loaded: hooks.py")
    hooks = None


def get_plugin_manager() -> pluggy.PluginManager:
    pm = pluggy.PluginManager("stadsarkiv_client")
    pm.add_hookspecs(hook_specs)

    if hooks:
        pm.register(hooks)

        for _, obj in inspect.getmembers(sys.modules[hooks.__name__]):
            if inspect.isclass(obj):
                pm.register(obj)

    return pm
