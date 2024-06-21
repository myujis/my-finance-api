#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

# to have it watch app dir while developing
os.chdir('../app')

import uvicorn

if __name__ == '__main__':

    # load .env into environment if not run in Docker
    # env_file option of uvicorn also takes care of that
    # relative paths are different here!
    #
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path('./../../') / '.env'
    load_dotenv(dotenv_path=env_path)

    # test
    from app.core.config import settings
    print(f'{settings.PROJECT_NAME} backend starting')
    print(f'starting on port: {settings.BACKEND_PORT}')

    uvicorn.run('app.main:app', host='0.0.0.0', port=settings.BACKEND_PORT, env_file='../.env', reload=True)

