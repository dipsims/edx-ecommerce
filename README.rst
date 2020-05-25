Install Node
sudo apt install mysql-server mysql-client libmysqlclient-dev (Needed by mysqlclient python lib)
Setup Virtual Env
python3 -m venv venv
source venv/bin/activate
pip install -U setuptools pip
git checkout -b feature-modifications
make requirements
Mimick Devstack
cp ecommerce/settings/private.py.example ecommerce/settings/private.py (Uses SQLITE)
python manage.py migrate
make static
python manage.py createsuperuser

Use the information in LMS to create_or_update_site
http://dev.dipsims.xyz/admin/oauth2_provider/application/4/change/
http://dev.dipsims.xyz/admin/oauth2_provider/application/3/change/

python manage.py create_or_update_site --site-id 1 \
    --site-domain 'http://dev.dipsims.xyz' --partner-code edX --partner-name 'Open edX' \
    --lms-url-root 'http://dev.dipsims.xyz' --payment-processors cybersource,paypal,paystack \
    --backend-service-client-id 'ecommerce-backend-service-key' \
    --backend-service-client-secret 'ecommerce-backend-service-secret' \
    --sso-client-id 'ecommerce-sso-key' --sso-client-secret 'ecommerce-sso-secret' \
    --from-email sales@logicaladdress.com --discovery_api_url http://134.209.204.119:18381

http://dev.dipsims.xyz/admin/oauth2_provider/application/3/change/
Redirect uris:
http://localhost:18130/complete/edx-oauth2/ http://ecommerce.dev.dipsims.xyz/complete/edx-oauth2/ http://127.0.0.1:8002/complete/edx-oauth2/ http://localhost:8002/complete/edx-oauth2/


Issues
ERROR:  py35-django22-theme_static: InterpreterNotFound: python3.5

python --version (Ubuntu 18.04)
Python 3.6.9
apt install libsqlite3-dev
See: https://vlearningit.wordpress.com/installation/install-python3-5-from-the-source-in-ubuntu-18-04/




TMP
127.0.0.1:8002/basket/add/?sku=3D1B341