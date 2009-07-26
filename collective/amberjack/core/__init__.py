from Products.CMFCore.DirectoryView import registerDirectory

GLOBALS = globals()
SKIN_DIR = 'skins'

registerDirectory(SKIN_DIR, GLOBALS)

def initialize(context):
    pass