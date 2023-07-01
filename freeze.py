from py2exe import freeze

freeze(
    console=[],
    windows=['PvZHCCC.py'],
    data_files=None,
    zipfile=None,
    options={"bundle_files":1, "compressed":True},
    version_info={}
)