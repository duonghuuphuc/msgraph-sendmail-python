#!/bin/sh

export SECRET_KEY='h@rd-t0-get-string'
export CLIENT_ID='INSERT_APPLICATION_CLIENT_ID'
export CLIENT_SECRET='INSERT_APPLICATION_CLIENT_SECRET'
export FLASK_DEBUG=1

flask run