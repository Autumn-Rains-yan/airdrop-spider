import os
import sys

from settings.UserSettings import APP_ID, GROUP_CODE, APP_SECRET

BASE_DIR = os.path.abspath('.')
PORT = '6873'
HTTP_BASE = 'http://127.0.0.1:' + PORT

# CMD命令
CMD_HUB = f"hubstudio_connector.exe --server_mode=http --http_port={PORT} --app_id={APP_ID} --group_code={GROUP_CODE} --app_secret={APP_SECRET}"
DEBUG = not getattr(sys, 'frozen', False)

