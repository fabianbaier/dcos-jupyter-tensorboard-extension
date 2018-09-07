import os

__version__ = '0.0.1'


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    from json import dumps
    from markupsafe import Markup

    nb_server_app.log.info("DC/OS Jupyter Serverextension: loading...")
    web_app = nb_server_app.web_app
    page_config = web_app.settings.setdefault('page_config_data', dict())
    
    try:
        page_config['dcos'] = os.environ['START_TENSORBOARD']
    except KeyError as k:
        nb_server_app.log.info("DC/OS Jupyter Serverextension: TensorBoard environment variable not set")

    nb_server_app.log.info("DC/OS Jupyter Serverextension: loaded.")
