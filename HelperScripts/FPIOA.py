#!INFO
#Here we map pin 28 to the function of GPIO0. After executing this command, pins 28
# and GPIO0 are mapped (bound). If you want to unmap (unbind), then Need to call the
#  fm.unregister function, see the API documentation for details, not introduced here


from fpioa_manager import fm # import library
fm.register(28, fm.fpioa.GPIO0)
