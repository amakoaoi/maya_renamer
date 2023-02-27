from maya_helper import unload_packages
unload_packages(["maya_renamer"])
# Copy only the following lines to add to a shelf (Windows -> Settings/Preferences -> Shelf Editor):
from maya_renamer import MayaRenamer
window = MayaRenamer()