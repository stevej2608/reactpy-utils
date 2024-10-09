## Building

    poetry install --no-root


## Publish 

    rm -rf dist && poetry build
    poetry publish

Or publish to local repo

    poetry publish -r pypicloud
