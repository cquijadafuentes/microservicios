from flask import Flask
from datetime import date
import os
import socket

app = Flask(__name__)
@app.route("/")

def hello():
	today = date.today().strftime("%m/%d/%Y, %H:%M:%S")
	x = "Hello work! "
	r = ""
	for i in range(1, 11):
		r = r + x
	html = "<h3>Hello {name}!</h3> <b>Hostname:</b> {hostname}<br/><b>Datetime:</b> " + today + "<br/>" + r + "<br/>"
	print html
	return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=4000)
	
