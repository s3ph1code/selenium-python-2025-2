from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import shutil
import sys
from pathlib import Path

# Ensure project root is on sys.path so that 'pages' package can be imported from steps
_features_dir = Path(__file__).resolve().parent
_project_root = _features_dir.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def _build_chrome_driver():
    """
    Try to create a Chrome WebDriver in a robust way:
    1) Use chromedriver(.exe) from project root if present.
    2) Else, if chromedriver is in PATH, use it.
    3) Else, try webdriver-manager if installed.
    """
    options = ChromeOptions()
    # Headless mode for CI or when HEADLESS=1 is set
    if os.environ.get("CI") or os.environ.get("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")

    # Candidate paths for chromedriver in project root
    local_driver = _project_root / ("chromedriver.exe" if os.name == "nt" else "chromedriver")

    service = None

    if local_driver.exists():
        service = ChromeService(executable_path=str(local_driver))
    else:
        which_path = shutil.which("chromedriver")
        if which_path:
            service = ChromeService(executable_path=which_path)
        else:
            try:
                from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
                service = ChromeService(ChromeDriverManager().install())
            except Exception:
                # Last fallback: let Selenium try default discovery (may fail if no driver in PATH)
                service = ChromeService()

    return webdriver.Chrome(service=service, options=options)


def before_scenario(context, scenario):
    """
    Esta función se ejecuta antes de cada escenario de prueba.
    Inicializa el WebDriver y lo almacena en el contexto.
    """
    context.driver = _build_chrome_driver()
    try:
        context.driver.maximize_window()
    except Exception:
        # In headless or some environments maximize may not be supported
        pass


def after_scenario(context, scenario):
    """
    Esta función se ejecuta después de cada escenario de prueba.
    Cierra el navegador para limpiar después de cada prueba.
    """
    if getattr(context, "driver", None):
        context.driver.quit()
