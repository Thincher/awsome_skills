---
name: minimax-use
description: 使用 MiniMax 进行网络搜索和语音合成。触发条件：(1) 用户要求进行网络搜索、在线搜索、查找最新资讯 (2) 用户要求文本转语音、语音合成。其他功能（图像理解、视频生成、图片生成）需要用户明确指定使用 MiniMax 才会触发。
---

# minimax-use

使用 MiniMax 进行网络搜索、图像理解、语音合成和文生视频分析。

## 功能一：网络搜索

### 调用 web_search

使用脚本调用 MCP 服务：

```bash
python3 {curDir}/scripts/web_search.py "<搜索查询>"
```

**示例：**

```bash
# 搜索今日新闻
python3 {curDir}/scripts/web_search.py "今天的热点新闻"
```

### API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| query | 搜索查询字符串 | string (必填) |

## 功能二：图像理解

### 准备图片

将图片放到可访问路径，例如：
- `~/.openclaw/workspace/images/图片名.jpg`
- 或者使用 URL

### 调用 understand_image

使用脚本调用 MCP 服务：

```bash
python3 {curDir}/scripts/understand_image.py <图片路径或URL> "<对图片的提问>"
```

**示例：**

```bash
# 描述图片内容
python3 {curDir}/scripts/understand_image.py ~/image.jpg "详细描述这张图片的内容"

# 使用 URL
python3 {curDir}/scripts/understand_image.py "https://example.com/image.jpg" "这张图片展示了什么？"
```

### API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| image | 图片路径或 URL | string (必填) |
| prompt | 对图片的提问 | string (必填) |

## 功能三：语音合成

### 调用 text_to_speech

使用脚本调用 MiniMax 语音合成 API：

```bash
python3 {curDir}/scripts/text_to_speech.py "<文本>" [选项]
```

**示例：**

```bash
# 基本用法（输出 hex 格式）
python3 {curDir}/scripts/text_to_speech.py "你好世界"

# 保存为 MP3 文件
python3 {curDir}/scripts/text_to_speech.py "你好世界" --output audio.mp3

# 使用 URL 格式输出
python3 {curDir}/scripts/text_to_speech.py "你好世界" --format url

# 指定模型
python3 {curDir}/scripts/text_to_speech.py "你好世界" --model speech-2.8-turbo --output audio.mp3

# 指定音色
python3 {curDir}/scripts/text_to_speech.py "你好世界" --voice male-qn-jingying --output audio.mp3

# 查看可用音色列表
python3 {curDir}/scripts/text_to_speech.py --list-voices

# 音色复刻
python3 {curDir}/scripts/text_to_speech.py --clone-voice my_voice.mp3
```

### 选项说明

| 选项 | 说明 | 默认值 |
|------|------|--------|
| --model | 模型版本 | speech-2.8-hd |
| --output | 保存音频到文件（MP3 格式） | 无 |
| --format | 输出格式：hex 或 url | hex |
| --voice | 音色 ID | female-shaonv |
| --list-voices | 列出所有可用音色 | 无 |
| --clone-voice | 音色复刻（上传音频文件） | 无 |

### 音色复刻说明

使用 `--clone-voice` 参数上传音频文件进行音色复刻：

**文件要求：**
- 格式：mp3、m4a、wav
- 时长：10秒 - 5分钟
- 大小：不超过 20MB

**使用流程：**
1. 上传音频文件进行复刻
2. 获取返回的 voice_id
3. 使用该 voice_id 进行语音合成

### 可用模型

- speech-2.8-hd
- speech-2.8-turbo
- speech-2.6-hd
- speech-2.6-turbo

### API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| text | 需要合成语音的文本 | string (必填) |
| model | 模型版本 | string |
| output_format | 输出格式：hex 或 url | string |
| voice_id | 音色 ID | string |
| voice_setting | 声音设置 | object |
| audio_setting | 音频设置 | object |

## 功能四：视频生成

### 调用 video

使用脚本调用 MiniMax 视频生成 API：

```bash
python3 {curDir}/scripts/video.py "<描述>" [选项]
```

**示例：**

```bash
# 文生视频（T2V）
python3 {curDir}/scripts/video.py "一只可爱的猫咪在阳光下玩耍"

# 指定时长和分辨率
python3 {curDir}/scripts/video.py "一只可爱的猫咪在阳光下玩耍" --duration 10 --resolution 1080P

# 图生视频（I2V）
python3 {curDir}/scripts/video.py --image /path/to/image.jpg "猫咪玩耍"

# 首尾帧生成视频（FL2V）
python3 {curDir}/scripts/video.py --image /path/to/first.jpg --last-frame /path/to/last.jpg "猫咪玩耍"

# 主体参考视频生成（S2V）
python3 {curDir}/scripts/video.py --subject /path/to/subject.jpg "猫咪玩耍"

# 查询任务状态
python3 {curDir}/scripts/video.py --query <task_id>

# 下载视频
python3 {curDir}/scripts/video.py --download <file_id> --output video.mp4
```

### 选项说明

| 选项 | 说明 | 默认值 |
|------|------|--------|
| --model | 模型版本 | MiniMax-Hailuo-2.3 |
| --duration | 视频时长（秒） | 6 |
| --resolution | 视频分辨率：512P, 720P, 768P, 1080P | 768P |
| --query | 查询任务状态 | 无 |
| --download | 下载视频（需 file_id） | 无 |
| --output | 保存视频到文件（mp4 格式） | 无 |
| --image | 首帧图片（图生视频 I2V / 首尾帧 FL2V） | 无 |
| --last-frame | 尾帧图片（首尾帧 FL2V） | 无 |
| --subject | 主体参考图片（主体参考 S2V） | 无 |

### 可用模型

**文生视频（T2V）：**
- MiniMax-Hailuo-2.3
- MiniMax-Hailuo-02
- T2V-01-Director
- T2V-01

**图生视频（I2V）：**
- MiniMax-Hailuo-2.3
- MiniMax-Hailuo-2.3-Fast
- MiniMax-Hailuo-02
- I2V-01-Director
- I2V-01-live
- I2V-01

**首尾帧生成（FL2V）：**
- MiniMax-Hailuo-02

**主体参考视频生成（S2V）：**
- S2V-01

### 分辨率支持

**T2V：** 720P, 768P, 1080P

**I2V：** 512P, 720P, 768P, 1080P

**FL2V：** 768P, 1080P

**S2V：** 默认分辨率

### 运镜指令

对于 MiniMax-Hailuo-2.3、MiniMax-Hailuo-02 和 *-Director 系列模型，支持使用 `[指令]` 语法进行运镜控制：

**支持 15 种运镜指令：**
- 左右移：`[左移]`, `[右移]`
- 左右摇：`[左摇]`, `[右摇]`
- 推拉：`[推进]`, `[拉远]`
- 升降：`[上升]`, `[下降]`
- 上下摇：`[上摇]`, `[下摇]`
- 变焦：`[变焦推近]`, `[变焦拉远]`
- 其他：`[晃动]`, `[跟随]`, `[固定]`

**使用规则：**
- 组合运镜：同一组 `[]` 内的多个指令会同时生效，如 `[左摇,上升]`，建议组合不超过 3 个
- 顺序运镜：prompt 中前后出现的指令会依次生效

### API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| prompt | 视频的文本描述，最大 2000 字符 | string (必填) |
| model | 模型名称 | string (必填) |
| duration | 视频时长（秒） | integer |
| resolution | 视频分辨率 | string |
| prompt_optimizer | 是否自动优化 prompt | boolean |
| fast_pretreatment | 是否缩短优化耗时 | boolean |
| aigc_watermark | 是否添加水印 | boolean |

## 功能五：图片生成

### 调用 image

使用脚本调用 MiniMax 图片生成 API：

```bash
python3 {curDir}/scripts/image.py "<描述>" [选项]
```

**示例：**

```bash
# 文生图（T2I）
python3 {curDir}/scripts/image.py "一只可爱的猫咪在阳光下玩耍"

# 指定宽高比和数量
python3 {curDir}/scripts/image.py "一只可爱的猫咪在阳光下玩耍" --aspect-ratio 16:9 --n 2

# 指定宽高
python3 {curDir}/scripts/image.py "一只可爱的猫咪在阳光下玩耍" --width 1024 --height 768 --output cat.png

# 图生图（I2I）
python3 {curDir}/scripts/image.py --subject /path/to/image.jpg "猫咪玩耍"
```

### 选项说明

| 选项 | 说明 | 默认值 |
|------|------|--------|
| --model | 模型版本 | image-01 |
| --aspect-ratio | 图片宽高比 | 1:1 |
| --width | 图片宽度（512-2048，8的倍数） | 无 |
| --height | 图片高度（512-2048，8的倍数） | 无 |
| --n | 生成图片数量（1-9） | 1 |
| --seed | 随机种子 | 无 |
| --format | 返回格式：url, base64 | url |
| --output | 保存图片到文件（png/jpg 格式） | 无 |
| --subject | 主体参考图片（图生图 I2I） | 无 |

### 可用模型

**文生图（T2I）：**
- image-01
- image-01-live

**图生图（I2I）：**
- image-01
- image-01-live

### 宽高比选项

- 1:1 (1024x1024)
- 16:9 (1280x720)
- 4:3 (1152x864)
- 3:2 (1248x832)
- 2:3 (832x1248)
- 3:4 (864x1152)
- 9:16 (720x1280)
- 21:9 (1344x576) (仅适用于 image-01)

### API 参数说明

| 参数 | 说明 | 类型 |
|------|------|------|
| prompt | 图片的文本描述，最长 1500 字符 | string (必填) |
| model | 模型名称 | string (必填) |
| aspect_ratio | 图片宽高比 | string |
| width | 图片宽度（像素） | integer |
| height | 图片高度（像素） | integer |
| n | 单次请求生成的图片数量 | integer |
| seed | 随机种子 | integer |
| response_format | 返回格式：url, base64 | string |
| prompt_optimizer | 是否自动优化 prompt | boolean |
| aigc_watermark | 是否添加水印 | boolean |
| subject_reference | 主体参考（I2I） | object[] |
