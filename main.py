import logging
from gui.gui import RunApp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('-----------------------------------------------------------------------------------')
logger.info(f'Initializing {__name__}.')

app = RunApp()
app.after(10, lambda: app.set_appwindow())
app.mainloop()
