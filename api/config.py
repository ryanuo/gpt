from g4f.models import ModelUtils

models = ModelUtils()

new_list = {"data": []}
for model in models.convert:
    new_list["data"].append({"id": model})

# 取出模型列表
g4f_model_list = new_list

default_model = "gpt-4o-mini"