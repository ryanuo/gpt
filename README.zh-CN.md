# GPT模型交互与应用平台

[![中文][zh-src]][zh-href]
[![English][en-src]][en-href]

[zh-src]: https://img.shields.io/badge/中文-black.svg
[zh-href]: ./README.zh-CN.md
[en-src]: https://img.shields.io/badge/English-black.svg
[en-href]: ./README.en.md

## 项目概述

这是一个基于Flask的Web应用程序，提供API接口和简单的前端界面，用于与GPT模型进行交互。用户可以通过微信公众号或Web界面与AI进行聊天、生成图像或获取内容摘要。

## 主要功能
- **与GPT模型的文本对话**：支持多轮对话，模拟类人聊天。
- **基于用户输入的图像生成**：使用AI模型生成高质量图像。
- **微信公众号公众号消息处理**：支持自动回复、图像生成等功能。
- **内容摘要**：从长文本或网页中提取关键信息，生成简洁摘要。
- **自定义AI服务的供应商**: 支持自定义AI服务供应商，如OpenAI兼容的API。

## 一键部署

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ryanuo/gpt)
**注：需要根据实际使用情况填写环境变量**

## 使用说明

### 环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/ryanuo/gpt.git
   cd gpt
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   ```bash
   cp .env.example .env
   ```
4. 启动服务：
   ```bash
   python -m api.index
   ```
### 环境变量配置

| 环境变量名称         | 用途说明                                                                 | 示例值                                  | 是否必填 | 备注                                                                 |
|----------------------|--------------------------------------------------------------------------|-----------------------------------------|----------|----------------------------------------------------------------------|
| `WX_TOKEN`           | 微信公众号的Token，用于消息签名验证                                     | `wechat_token_123456`                   | 是（微信功能） | 仅在使用微信公众号消息处理功能时需要配置                             |
| `OPENAI_API_KEY`     | GPT模型的API密钥                                                       | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`   | 否       | 当使用自定义OpenAI兼容API（`PROVIDER=custom`）时需要配置             |
| `PROVIDER`           | 指定AI服务提供商类型                                                   | `custom`                                | 否       | 默认为空（使用`g4f`客户端默认服务），`custom`表示使用自定义API       |
| `COMPLETION_MODEL`   | 设置默认使用的文本生成模型                                             | `gpt-4o-mini`、`gpt-3.5-turbo`          | 否       | 未设置时使用`api/config.py`中定义的`default_model`（默认为`gpt-4o-mini`） |
| `API_KEY`            | 自定义AI服务的认证密钥                                                 | `custom_api_key_789`                    | 否       | 当`PROVIDER=custom`时需配置，与`OPENAI_API_KEY`功能类似             |
| `API_URL`            | 自定义AI服务的API端点URL（兼容OpenAI格式）                              | `https://api.example.com/v1`            | 否       | 当`PROVIDER=custom`时需配置，默认使用OpenAI官方API地址               |

### 补充说明
- 环境变量需配置在项目根目录的 `.env` 文件中（参考 `.gitignore` 文件，该文件已忽略 `.env`，避免密钥泄露）。
- 不同场景下的配置组合可参考：
  - 使用默认 `g4f` 服务：无需配置 `PROVIDER`、`API_KEY`、`API_URL`，按需设置 `COMPLETION_MODEL`。
  - 使用自定义 API：需同时配置 `PROVIDER=custom`、`API_KEY`、`API_URL`，可选配 `COMPLETION_MODEL`。

## 接口列表
| API类型         | 路径                | 方法   | 参数                                                                                                                                                 | 返回内容                                                                                                                                                |
|----------------|---------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **对话API**     | `/g4f/<model>`      | POST   | - `message`：用户输入文本<br>- `context`（可选）：对话上下文（格式为`[{"role":"user","content":"xxx"},{"role":"assistant","content":"xxx"}]`）<br>_注：模型通过路径中的`<model>`指定，支持的模型可通过`/vmodels`接口获取_ | JSON格式，包含`response`字段（模型生成的响应文本）                                                                                                         |
| **图像生成**    | `/generate-image`   | POST   | - `prompt`：描述图像内容的文本（如“赛博朋克风格的城市夜景”）<br>_注：固定使用`flux`模型_                                                                 | JSON格式，包含`image_url`字段（生成图像的在线访问URL）                                                                                                      |
| **微信公众号**  | `/wechat`           | POST   | 自动解析微信服务器推送的消息格式（含`signature`、`timestamp`、`nonce`等验证参数及`xml`格式消息内容）<br>_注：使用`api/config.py`中定义的`default_model`，默认`gpt-4o-mini`_ | 按微信接口规范返回`xml`格式消息回复（文本或含图像URL的图文消息）                                                                                               |
| **内容摘要**    | `/ai-post`          | POST   | - `url`：需提取摘要的网页URL（如“https://example.com/article”）<br>_注：使用`api/config.py`中定义的`default_model`，默认`gpt-4o-mini`_ | JSON格式，包含`summary`字段（网页核心内容的简洁摘要，约50-200字）                                                                                             |
| **模型列表查询**| `/vmodels`          | GET    | 无（无需请求参数）<br>_注：仅返回支持的模型列表，不涉及模型调用_                                                                                          | JSON格式，按类型分组的模型列表，示例：<br>`{`<br>  `"GPT系列": ["gpt-4o-mini", "gpt-3.5-turbo"],`<br>  `"其他模型": ["claude-3-haiku", "gemini-pro"]`<br>`}` |

## 参考资料

- [wechatpy文档](https://wechatpy.readthedocs.io/)
- [OpenAI GPT模型](https://github.com/xtekky/gpt4free)

## 许可证

本项目采用MIT许可证，详情参见 [LICENSE](./LICENSE.md) 文件。