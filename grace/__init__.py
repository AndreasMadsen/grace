
# Configureation file for the module allows `import grace`. Grace will then
# contain the dataset as (grace.grids, grace.dates, grace.positions)

# Automaticly build datafiles if they don't exists
import build
build.autobuild()

# Load datafiles
from load import grids, dates, positions

__all__ = ["grids", "dates", "positions"]

