'''
Author: liziwei01
Date: 2022-07-10 16:06:30
LastEditors: liziwei01
LastEditTime: 2022-07-11 13:46:22
Description: file content
'''
from pywebio.input import input_group, input, TEXT, PASSWORD
from pywebio.output import put_buttons, put_success, put_warning
from pywebio.session import go_app
import requests
from library.utils.encrypt import EncryptRsa

def UserLogin() -> None:
	while True:
		data = input_group(label="login", inputs=[
			input(label="email", name="email", type=TEXT),
			input(label="password", name="...word", type=PASSWORD),
		])
		
		if data["email"] == "" or data["...word"] == "":
			put_warning("Please input email and ...word")
		else:
			data["...word"] = EncryptRsa(data["...word"])
			r = requests.post(url="http://localhost:8082/gin-file-download/user/login", params=data)
			if r.status_code == 200:
				data = r.json()["data"]
				errmsg = r.json()["errmsg"]
				errno = r.json()["errno"]
				if errmsg == "Success":
					put_success("Login success")
					put_buttons(['Go to tree'], [lambda: go_app('task_A')])
					break