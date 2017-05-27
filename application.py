# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, request
from flask import render_template
import sys
from datetime import datetime
import pytz
import os
import simplejson
import StringIO
from PIL import Image

import logging
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
import json


# @app.route('/')
# def hello():
#     return render_template("index.html", title="home")


@app.route('/uploader', methods=['POST'])
def multi_picture_uploader():

    args = []
    user = ''
    if(request.method == 'POST'):
        if(request.files):
            if request.form.get('images'):
                imgs = request.form.get('images')
                if len(imgs) > 1:
                    for i in json.loads(imgs):
                        args.append(i)
            if request.form.get('user'):
                user = request.form.get('user')
            ufile = request.files.getlist('ufile', None)
            for nfile in ufile:
                addons_path = '/opt/odoo-produccion/odoo/openerp/addons'
                data = nfile.read()

                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                start = datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
                tz = pytz.timezone('America/Asuncion')
                start = pytz.utc.localize(start).astimezone(tz)
                # tz_date = start.strftime("%Y-%m-%d %H:%M:%S")
                current_dat_time = start.strftime("%d-%m-%Y-%H_%M_%S")
                ##
                file_name = current_dat_time + "_" + nfile.filename
                true_file_name = file_name

                addons_path += '/web/static/src/img/image_multi/'
                if not os.path.isdir(addons_path):
                    os.mkdir(addons_path)

                addons_path += file_name
                buff = StringIO.StringIO()
                buff.write(data)
                buff.seek(0)
                file_name = "/web/static/src/img/image_multi/" + file_name
                file = open(addons_path, 'wb')
                file.write(buff.read())
                file.close()
                thumb_file = make_thumbnails(addons_path, true_file_name)
                args.append({
                    "size": len(data),
                    "name": file_name.encode("utf-8"),
                    "content_type": nfile.content_type,
                    "orignal_name": nfile.filename.encode("utf-8"),
                    "date": start.strftime("%m/%d/%Y %H:%M:%S"),
                    "thumb_file": thumb_file.encode("utf-8"),
                    "user": user.encode("utf-8")
                    })
    args = str(args)
    args = args.replace("\'", "\"")
    args = args.replace("u\"","\"").replace("u\'","\'")
    print("el valor de args" +args)
    return args
    # return render_template("resultado.html", name=args)


def make_thumbnails(addons_path, true_file_name):
    size = 256, 256
    img_original = Image.open(addons_path)
    # thumbs_path = http.addons_manifest['web']['addons_path'] +\
    #    # "/web/static/src/img/image_multi/thumbs/"
    thumbs_path = "/opt/odoo-produccion/odoo/openerp/addons/web/static/src/img/image_multi/thumbs/"
    if not os.path.isdir(thumbs_path):
        os.mkdir(thumbs_path)
    img_original.thumbnail(size)
    img_original.save(os.path.join(thumbs_path+true_file_name), "JPEG")
    return ("/web/static/src/img/image_multi/thumbs/"+true_file_name)


if __name__ == '__main__':
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)
    app.run(debug=True)
