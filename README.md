pysettings
==========

Package-wide namespace hierarchy for loading user settings.  "Abuses" python
dicts to expose keys as attributes via ``setattr`` and ``getattr``.
  
Can load namespace hiearchies from JSON and YAML files.
  

## Loading Namespaces
Let's assume we have a YAML file. ::
    
    config:
        require_user: true
        connection:
            address: localhost
            port:    18832

The first step would be to set a top-level namespace.  This would take place at the top-level of your project/package. ::
    
    import pysettings

    pysettings.loadfrom_yaml("topLevelKey", "path/to/settings.yaml")

## Using namespaces
The second step is using the imported Namespace in a sub-module or sub-package. ::

	import pysettings

	settings = pysettings.get_namespace("topLevelKey")
	
	# we can access settings loaded in step one like this:
	print settings.config.connection.address

	# we can temporarily change settings like this:
	settings.config.connection.address = "127.0.0.1"
