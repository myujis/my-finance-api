#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))


if __name__ == '__main__':

    # load .env into environment if not run in Docker
    # env_file option of uvicorn takes care of that
    #
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path('./../../') / '.env'
    load_dotenv(dotenv_path=env_path)

    from app.core.config import settings
    if settings.USE_ALEMBIC == True:
        import subprocess
        subprocess.call("alembic upgrade head", shell=True)

    from app import initial_data
    initial_data.main()
