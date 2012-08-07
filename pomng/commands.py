
def cmdRegistryReload(pom, args):
	pom.registry.load();
	print("Registry reloaded");

def cmdRegistryDump(pom, args):
	print(pom.registry.getClasses())

def cmdConfigShow(pom, args):
	proxy = pom.registry.getProxy()
	classes = pom.registry.getClasses()
	for cls in classes:
		print(cls, ":")
		
		if len(classes[cls]['instances']) == 0:
			print("\t<none>")
			continue

		for instName in classes[cls]['instances']:
			inst = classes[cls]['instances'][instName]
			print("\t" + instName + " :")

			if len(inst['parameters']) == 0:
				print("\t\t<none>")
				continue

			for paramName in inst['parameters']:
				param = inst['parameters'][paramName]
				print("\t\t" + paramName + " : '" + param['value'] + "' (" + param['type'] + ")")
		

def cmdCoreGetVersion(pom, args):
	proxy = pom.registry.getProxy()
	print("Pom-ng version is " + proxy.core.getVersion())

def cmdInstanceAdd(pom, instClass, args):
	instName = args[1]
	instType = args[0]
	pom.registry.addInstance(instClass, instName, instType)

def completeInstanceAdd(pom, instClass, words):
	if len(words) != 1:
		return []
	cls = pom.registry.getClass(instClass)
	return [ x['name'] for x in cls['available_types'] if x['name'].startswith(words[0]) ]

def cmdInstanceRemove(pom, instClass, args):
	instName = args[0]
	pom.registry.removeInstance(instClass, instName)

def completeInstanceRemove(pom, instClass, words):
	if len(words) != 1:
		return []
	cls = pom.registry.getClass(instClass)
	return [ x for x in cls['instances'] if x.startswith(words[0]) ]

def cmdLogLevelSet(pom, words):

	newLevel = 0
	levels = pom.getLoggingLevels()

	if words[0] in levels:
		newLevel = levels.index(words[0]) + 1
	else:
		try:
			newLevel = int(words[0])
		except:
			print("New level must be an integer or any of", levels)
			return

	if newLevel < 1 or newLevel > 4:
		print("Log level must be 1-4")

	pom.setLoggingLevel(newLevel)
	print("Logging level set to '" + levels[newLevel - 1] + "'")

def completeLogLevelSet(pom, words):
	if len(words) != 1:
		return []

	levels = pom.getLoggingLevels()
	levels.extend([ '1', '2', '3', '4'])
	return [ x for x in levels if x.startswith(words[0]) ]

def cmdLogLevelGet(pom, words):
	levels = pom.getLoggingLevels()
	level = pom.getLoggingLevel()
	print("Logging level set to '" + levels[level - 1] + "' (" + str(level) + ")")

cmds = [

		# Config functions
		{
			'cmd'		: "config show",
			'help'		: "Show the whole configuration",
			'callback'	: cmdConfigShow
		},
		

		# Core functions
		{
			'cmd'		: "core get version",
			'help'		: "Get pom-ng version",
			'callback'	: cmdCoreGetVersion
		},

		# Datastore functions
		{
			'cmd'		: "datastore add",
			'signature'	: "datastore add <type> <name>",
			'help'		: "Add an datastore",
			'callback'	: lambda pom, args : cmdInstanceAdd(pom, "datastore", args),
			'complete'	: lambda pom, words : completeInstanceAdd(pom, "datastore", words),
			'numargs'	: 2
		},

		{
			'cmd'		: "datastore remove",
			'signature'	: "datastore remove <name>",
			'help'		: "Remove an datastore",
			'callback'	: lambda pom, args : cmdInstanceRemove(pom, "datastore", args),
			'complete'	: lambda pom, words : completeInstanceRemove(pom, "datastore", words),
			'numargs'	: 1
		},

		# Input functions
		{
			'cmd'		: "input add",
			'signature'	: "input add <type> <name>",
			'help'		: "Add an input",
			'callback'	: lambda pom, args : cmdInstanceAdd(pom, "input", args),
			'complete'	: lambda pom, words : completeInstanceAdd(pom, "input", words),
			'numargs'	: 2
		},

		{
			'cmd'		: "input remove",
			'signature'	: "input remove <name>",
			'help'		: "Remove an input",
			'callback'	: lambda pom, args : cmdInstanceRemove(pom, "input", args),
			'complete'	: lambda pom, words : completeInstanceRemove(pom, "input", words),
			'numargs'	: 1
		},

		# Output functions
		{
			'cmd'		: "output add",
			'signature'	: "output add <type> <name>",
			'help'		: "Add an output",
			'callback'	: lambda pom, args : cmdInstanceAdd(pom, "output", args),
			'complete'	: lambda pom, words : completeInstanceAdd(pom, "output", words),
			'numargs'	: 2
		},

		{
			'cmd'		: "output remove",
			'signature'	: "output remove <name>",
			'help'		: "Remove an output",
			'callback'	: lambda pom, args : cmdInstanceRemove(pom, "output", args),
			'complete'	: lambda pom, words : completeInstanceRemove(pom, "output", words),
			'numargs'	: 1
		},

		# Registry functions
		{
			'cmd'		: "registry dump",
			'help'		: "Dump the whole registry",
			'callback'	: cmdRegistryDump
		},

		{
			'cmd'		: "registry reload",
			'help'		: "Reload the registry if it gets out of sync",
			'callback'	: cmdRegistryReload
		},

		# Logs functions
		{
			'cmd'		: "log level set",
			'help'		: "Set the logging level to be displayed",
			'callback'	: cmdLogLevelSet,
			'complete'	: completeLogLevelSet,
			'numargs'	: 1
		},

		{
			'cmd'		: "log level get",
			'help'		: "Display the current loging level that will be displayed",
			'callback'	: cmdLogLevelGet
		}
		
	]

def commandsRegister(console):
	console.registerCmds(cmds)
