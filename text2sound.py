import requests
import json

url = "https://ai.baidu.com/aidemo"

data = {
	"type": "tns",
	"per": "4106",
	"spd": "5",
	"pit": "5",
	"vol": "5",
	"aue": "6",
	"tex": "然后我们在每一帧的图像上罩上网格。",
}

res = requests.post(url, data=data)

print(json.loads(res.text)['data'])