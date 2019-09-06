from flask import Flask, request, redirect, url_for, send_from_directory, make_response
import numpy as np
import random, threading, webbrowser
import cv2
import requests
import os
from io import BytesIO

app = Flask(__name__)

# Define icon for URL. Will be used on every page of the website
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='favicon.ico')

# Define the Root page.
# Giving one button to go to the prediction
@app.route('/', methods=['GET', 'POST'])
def hello_world():
  if request.method == 'POST':
      #this block is only entered when the form is submitted
    return redirect(url_for('input'))
  return """Hello World!
          <form method="POST">
              <input type="submit" value="Inputs"><br>
          </form>"""

# Input page: given one image url, it will predict mrcnn
@app.route('/input', methods=['GET', 'POST'])
def input():
  if request.method == 'POST':  #this block is only entered when the form is submitted
    import mrcc
    url = request.form.get('url')
    canvas = mrcc.predict(url)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

  return """<form method="POST">
              URL: <input type="text" name="url"> <input type="submit" value="Submit">
          </form>"""
  

if __name__=="__main__":

  port = 5000 + random.randint(0, 999)
  url = "http://127.0.0.1:{0}".format(port)

  threading.Timer(1., lambda: webbrowser.open(url) ).start()

  app.run(port=port, debug=False)
  # app.run()