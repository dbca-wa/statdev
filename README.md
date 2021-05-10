Statutory Development
=====================

This project is the Department of Parks and Wildlife Statutory Development
corporate application.

# Environment variables

This project uses **django-confy** to set environment variables (in a `.env` file).
The following variables are required for the project to run:

    DATABASE_URL="postgis://USER:PASSWORD@HOST:5432/DATABASE_NAME"
    SECRET_KEY="ThisIsASecretKey"

Variables below may also need to be defined (context-dependent):

    DEBUG=True
    ALLOWED_DOMAIN=".dpaw.wa.gov.au"
    EMAIL_HOST="email.host"
    EMAIL_PORT=25
    SSO_COOKIE_NAME="oim_dpaw_wa_gov_au_sessionid"


This system requries a ledger gw server to be setup in order to udpate identification information and the following environment vairables configured.
    
    LEDGER_API_KEY='ZXMSV7HJ7T6C2BJF0LCSBJFYF0HCFUDCD74QXW49U2TV87MIXRN5SOWOWUHDLO17GSILNL7R9NQVMH1O5KVQ6ZDVTTEPRKQWDK8Y'
    LEDGER_API_URL='http://172.17.0.3:9002'

