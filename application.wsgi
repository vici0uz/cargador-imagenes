import sys, os
sys.path.insert(0,'/var/www/cargador_imagenes')
os.chdir('/var/www/cargador_imagenes')

from application import app as application
