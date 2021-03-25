# docshare-api

### Introduction

An API service to upload and share documents in a document library.

### Setup

1. Clone the repository

        git clone https://github.com/curioswati/docshare.git
    
2. Build the docker image

        docker build -t demo .

3. Run the container

        docker run --rm -it -p 8000:8000 demo:latest
        
### API

In a development setup, you can access the API docs at http://localhost:8000/docs/
