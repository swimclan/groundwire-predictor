from __setmodules__ import modulize
modulize('./models', './lib', './collections')

from Screener import Screener

screener = Screener()

print screener
