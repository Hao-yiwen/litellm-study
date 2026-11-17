# litellm-study

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-1.80.16-5B4BFF)](https://docs.litellm.ai/)
[![uv](https://img.shields.io/badge/uv-lockfile-DE5FE9)](https://docs.astral.sh/uv/)

用 [LiteLLM](https://github.com/BerriAI/litellm) 练习统一调用大模型的学习记录：同步补全、流式输出、异步并发、工具调用，以及 DeepSeek Chat / Reasoner 和火山引擎豆包。脚本会向真实服务发请求，仓库里没有密钥，也没有封装成应用。

## 内容

| 文件 | 实际在做什么 |
| --- | --- |
| `01_basic_completion.py` | `litellm.completion` 调用 `deepseek/deepseek-chat`。示例 1 打印回复和 `usage`，并捕获异常；示例 2 加上 `temperature`、`max_tokens`、`top_p`、`frequency_penalty`、`presence_penalty`。 |
| `02_streaming.py` | 同一模型、`stream=True`。示例 1 拼出完整文本；示例 2 统计 chunk 数并打印 `finish_reason`。 |
| `03_async_completion.py` | `acompletion`：单次异步、异步流式，以及 `asyncio.gather` 并发 3 个短问题。 |
| `04_tool_calling.py` | 向模型声明 `get_weather` 与 `calculate`，`tool_choice="auto"`。模型发起工具调用后，本地执行并把结果再送回去生成最终回复。天气数据是写死的（北京 / 上海 / 广州及默认值），计算使用 `eval`；源码里已注明不要拿到生产环境使用。 |
| `05_multi_provider.py` | 对比 `deepseek/deepseek-chat` 与 `deepseek/deepseek-reasoner`。若响应里有 `reasoning_content`，会先打印思考过程。文件名里的 multi-provider 指的是这两个模型条目，脚本没有再接入其他厂商。 |
| `06_doubao.py` | 以 OpenAI 兼容方式调用火山引擎方舟上的 `openai/doubao-seed-1-8-251228`（`api_base` 为 `https://ark.cn-beijing.volces.com/api/v3`，密钥读 `ARK_API_KEY`）。直接运行时只执行基础对话。同文件里还有推理、图片理解（请求一张方舟示例图）和流式输出，入口处被注释掉了。 |
| `proxy/config.yaml` | LiteLLM Proxy 配置。模型别名：`doubao`、`deepseek-chat`、`deepseek-reasoner`。路由为 `simple-shuffle`，重试 2 次，超时 30 秒，并打开 `drop_params`。 |

`01`–`05` 不传 `api_key`，LiteLLM 的 DeepSeek 提供方会读环境变量 `DEEPSEEK_API_KEY`，请求发往 `https://api.deepseek.com`。这些示例不经过本地 Proxy；Proxy 是另一条独立入口。

## 技术栈

由 `pyproject.toml` 与 `uv.lock` 锁定：

| 依赖 | 声明 | 锁定版本 |
| --- | --- | --- |
| Python | `>=3.13`（`.python-version` 为 `3.13`） | 验证时由 uv 安装的是 3.13.18 |
| `litellm[proxy]` | `>=1.0.0` | `1.80.16`（附带 Proxy 相关依赖，如 FastAPI、Uvicorn） |
| `python-dotenv` | `>=1.0.0` | `1.2.1` |

各脚本开头都会 `load_dotenv()`，从当前工作目录的 `.env` 读变量。`.gitignore` 忽略 `.env*`。

## 目录

```text
.
├── 01_basic_completion.py   # 同步补全
├── 02_streaming.py          # 流式输出
├── 03_async_completion.py   # 异步与并发
├── 04_tool_calling.py       # 工具调用
├── 05_multi_provider.py     # DeepSeek Chat / Reasoner 对比
├── 06_doubao.py             # 豆包（方舟 OpenAI 兼容接口）
├── proxy/
│   └── config.yaml          # LiteLLM Proxy 配置
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

没有测试、截图或许可证文件。

## 环境

- Python 3.13 或更高。系统自带的 3.12 不满足 `requires-python`。
- [uv](https://docs.astral.sh/uv/)。仓库用 `uv.lock` 锁依赖；下面的命令都按 uv 来写。
- 要看到模型回复，需要对应密钥：
  - `DEEPSEEK_API_KEY`：`01`–`05`，以及 Proxy 里的两个 DeepSeek 模型
  - `ARK_API_KEY`：`06_doubao.py`，以及 Proxy 里的 `doubao`

在仓库根目录创建 `.env`（不要提交）：

```bash
cat > .env << 'EOF'
DEEPSEEK_API_KEY=你的_DeepSeek_密钥
ARK_API_KEY=你的_方舟_密钥
EOF
```

只跑某一侧时，可以只填用到的那一项。

## 安装与运行

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/) 后，在仓库根目录：

```bash
uv sync
```

`uv sync` 会按 `.python-version` 准备 Python 3.13，并装入 `.venv`。

### 直接跑示例

```bash
uv run python 01_basic_completion.py
uv run python 02_streaming.py
uv run python 03_async_completion.py
uv run python 04_tool_calling.py
uv run python 05_multi_provider.py
uv run python 06_doubao.py
```

要看豆包的推理、看图或流式示例，去掉 `06_doubao.py` 底部对应函数调用前的注释后再运行。

### 启动本地 Proxy

配置文件头部写的就是这条命令：

```bash
uv run litellm --config proxy/config.yaml --port 4000
```

`general_settings.master_key` 写在仓库里，值是 `sk-litellm-proxy-key`，只适合本机练习。请求需要带上它：

```bash
curl -sS http://127.0.0.1:4000/health/liveliness

curl -sS http://127.0.0.1:4000/v1/models \
  -H "Authorization: Bearer sk-litellm-proxy-key"
```

把对话转到 Proxy 上的别名（仍需要 `.env` 里有对应厂商密钥，Proxy 用 `os.environ/...` 读取）：

```bash
curl -sS http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-litellm-proxy-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"用一句话介绍 Python"}]}'
```

`model` 可换成 `deepseek-reasoner` 或 `doubao`。

## 验证情况

在 Linux 上用 uv 0.13.8 核对过这些步骤：

- `uv sync` 成功，解释器为 CPython 3.13.18，安装的 `litellm` 为 1.80.16、`python-dotenv` 为 1.2.1。
- 六个脚本通过 `python -m py_compile`。
- 未配置有效密钥时，`01_basic_completion.py` 会请求 DeepSeek 并因鉴权失败结束（示例 1 打印错误后继续，示例 2 抛出异常）；`06_doubao.py` 在没有 `ARK_API_KEY` 时抛出 `AuthenticationError`。
- `litellm --config proxy/config.yaml --port 4000` 能启动。`/health/liveliness` 返回 `I'm alive!`；携带 master key 访问 `/v1/models` 能列出 `doubao`、`deepseek-chat`、`deepseek-reasoner`。

没有可用的厂商密钥，因此模型生成的正文没有跑通。上面的 chat completions 示例是按已启动的 Proxy 与配置写出的调用方式。

## 参考

- [LiteLLM 文档](https://docs.litellm.ai/docs/)
- [LiteLLM DeepSeek](https://docs.litellm.ai/docs/providers/deepseek)
- [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start)
- [DeepSeek API](https://api-docs.deepseek.com/)
- [火山引擎方舟](https://www.volcengine.com/docs/82379)
