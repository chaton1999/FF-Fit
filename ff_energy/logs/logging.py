import logging


def hide_logs():
    logging.getLogger("matplotlib.font_manager").disabled = True
    logging.getLogger("matplotlib.texmanager").disabled = True
    logging.getLogger("matplotlib.dviread").disabled = True
    logging.getLogger("matplotlib").disabled = True
    logging.getLogger("matplotlib.axes").disabled = True
    logging.getLogger("matplotlib.pyplot").disabled = True
    logging.getLogger("PngImagePlugin").disabled = True
    # pxla, dispatch, and other jax logs
    logging.getLogger("pxla").disabled = True
    logging.getLogger("dispatch").disabled = True
    logging.getLogger("jax").disabled = True

    pil_logger = logging.getLogger('PIL')
    pil_logger.setLevel(logging.INFO)

    jax_logger = logging.getLogger('jax')
    jax_logger.setLevel(logging.INFO)

    matplotlib_logger = logging.getLogger('matplotlib')
    matplotlib_logger.setLevel(logging.INFO)

    logger.propagate = False


logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(module)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(filename="info.log"),
        # logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

hide_logs()
