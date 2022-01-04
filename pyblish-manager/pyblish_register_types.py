import pyblish.api


class PyblishRegisteredData:
    def __init__(self, name, add_command, remove_command, remove_all_command, list_command, ui_add_mode=None):
        self.name = name
        self.add_command = add_command
        self.remove_command = remove_command
        self.remove_all_command = remove_all_command
        self.list_command = list_command
        self.ui_add_mode = ui_add_mode  # None, 'browse', 'text'


plugin_paths = PyblishRegisteredData(
    name='plugin paths',
    add_command=pyblish.api.register_plugin_path,
    remove_command=pyblish.api.deregister_plugin_path,
    remove_all_command=pyblish.api.deregister_all_paths,
    list_command=pyblish.api.registered_paths,
    ui_add_mode='browse')

hosts = PyblishRegisteredData(
    name='hosts',
    add_command=pyblish.api.register_host,
    remove_command=pyblish.api.deregister_host,
    remove_all_command=pyblish.api.deregister_all_hosts,
    list_command=pyblish.api.registered_hosts,
    ui_add_mode='text')

targets = PyblishRegisteredData(
    name='targets',
    add_command=pyblish.api.register_target,
    remove_command=pyblish.api.deregister_target,
    remove_all_command=pyblish.api.deregister_all_targets,
    list_command=pyblish.api.registered_targets,
    ui_add_mode='text')

discovery_filters = PyblishRegisteredData(
    name='discovery filters',
    add_command=pyblish.api.register_discovery_filter,
    remove_command=pyblish.api.deregister_discovery_filter,
    remove_all_command=pyblish.api.deregister_all_discovery_filters,
    list_command=pyblish.api.registered_discovery_filters, )

callbacks = PyblishRegisteredData(
    name='callbacks',
    add_command=pyblish.api.register_callback,
    remove_command=pyblish.api.deregister_callback,
    remove_all_command=pyblish.api.deregister_all_callbacks,
    list_command=pyblish.api.registered_callbacks, )  # warning callbacks is a dict, not a list

plugins = PyblishRegisteredData(
    name='plugins',
    add_command=pyblish.api.register_plugin,
    remove_command=pyblish.api.deregister_plugin,
    remove_all_command=pyblish.api.deregister_all_plugins,
    list_command=pyblish.api.registered_plugins, )

guis = PyblishRegisteredData(
    name='guis',
    add_command=pyblish.api.register_gui,
    remove_command=pyblish.api.deregister_gui,
    remove_all_command=None,
    list_command=pyblish.api.registered_guis,
    ui_add_mode='text')

# a bit unclear how tests work atm. seems we can only have 1 registered test
tests = PyblishRegisteredData(
    name='tests',
    add_command=pyblish.api.register_test,
    remove_command=pyblish.api.deregister_test,
    remove_all_command=None,
    list_command=pyblish.api.registered_test,  # warning test is a single callback function, not a list
    ui_add_mode=None)

# this is technically not a registered data, but it's a convenient way to see all plugins after Pyblish ran discover
discovered_plugins = PyblishRegisteredData(
    name='discovered plugins',
    add_command=None,
    remove_command=None,  # can be done with filters after discovery
    remove_all_command=None,
    list_command=pyblish.api.discover,  # warning test is a single callback function, not a list
    ui_add_mode=None)


registered_data_types = [plugin_paths, hosts, targets, discovery_filters, callbacks, plugins, guis, tests, discovered_plugins]
