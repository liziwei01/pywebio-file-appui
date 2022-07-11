'''
Author: liziwei01
Date: 2022-07-10 16:09:35
LastEditors: liziwei01
LastEditTime: 2022-07-10 16:09:36
Description: file content
'''
def ShowFileTree() -> None:
	while True:
		data = input_group(label="login", inputs=[
			input(label="email", name="email", type=TEXT),
			input(label="...word", name="...word", type=TEXT),
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
					break