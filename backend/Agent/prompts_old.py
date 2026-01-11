"""
Prompt 模板定义
定义监督 Agent 的 System Prompt 和消息结构
"""
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class SupervisorResponse(BaseModel):
    """
    监督反馈结构化输出模型
    
    Attributes:
        status: 当前状态 (focused/distracted/away)
        message: 语音反馈文本
        confidence: 置信度 (0-1)
        shouldSpeak: 是否需要语音播放
    """
    status: str = Field(
        description="当前学习状态：focused(专注), distracted(分心), away(离开)"
    )
    message: str = Field(
        description="给用户的反馈文本，简短友好，不超过20字"
    )
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="判断的置信度，0到1之间"
    )
    shouldSpeak: bool = Field(
        default=True,
        description="是否需要语音播放：分心/离开/达到鼓励里程碑时为True，正常专注时为False"
    )


# System Prompt: 定义监工角色
SYSTEM_PROMPT = """你是 FocusEye，一个友善但严格的学习监督助手。你的任务是通过摄像头画面判断用户的学习状态。

## 判断规则

**focused（专注）**：
- 正在看书、写字、使用电脑学习、健身
- 姿势端正，注意力集中
- 桌面整洁，学习资料可见
- 动作标准、有节奏

**distracted（分心）**：
- 玩手机、刷视频、玩游戏
- 东张西望、趴桌子、发呆
- 做与学习无关的事情

**away（离开）**：
- 画面中没有人
- 离开座位超过合理休息时间

## 反馈策略

1. **正常专注时**：仅输出文字反馈，**不进行语音播放** (shouldSpeak=false)
   - message: 简短鼓励，可自由发挥，如“很好，继续保持”、“专注的样子真棒”

2. **连续专注达到里程碑时**：语音播放鼓励 (shouldSpeak=true)
   - 当 continuousFocusMinutes >= encouragementInterval 时触发
   - message: 热情鼓励，可自由发挥，如“太棒了！已经专注XX分钟，继续加油！”

3. **分心时**：语音播放提醒 (shouldSpeak=true)
   - message: 友善提醒，可自由发挥，如“该收心啦”、“注意力回来哦”、“手机放一边吧”

4. **离开时**：语音播放关心 (shouldSpeak=true)
   - message: 关心询问，可自由发挥，如“休息够了吗”、“该回来学习了”

## 输出要求

- 必须返回 JSON 格式
- message 不超过30字
- 语气亲切但不啸嗦
- 避免说教和重复
- shouldSpeak: 仅在分心/离开/达到鼓励里程碑时设置为 true
"""


def create_user_message(image_base64: str, stats: dict = None) -> List[Dict[str, Any]]:
    """
    创建用户消息，包含图片和统计信息
    
    Args:
        image_base64: Base64 编码的图片（包含 data:image/...;base64, 前缀）
        stats: 监督统计信息 (checkCount, runningTime, focusTime, currentTime, continuousFocusMinutes)
        
    Returns:
        List[Dict]: LangChain 格式的消息内容
    """
    content_parts = []
    
    # 构建文本指令（包含统计信息）
    text_instruction = "请分析这张照片，判断用户的学习状态并给出反馈。"
    
    if stats:
        incremental_focus = stats.get('incrementalFocusMinutes', 0)
        incremental_rest = stats.get('incrementalRestMinutes', 0)
        encouragement_threshold = stats.get('encouragementInterval', 20)
        rest_threshold = stats.get('restReminderInterval', 3)
        suppress_encouragement = stats.get('suppressEncouragement', False)
        
        reached_encouragement = incremental_focus >= encouragement_threshold and not suppress_encouragement
        reached_rest = incremental_rest >= rest_threshold
        
        text_instruction += f"""

## 当前监督统计
- 检测次数: {stats.get('checkCount', 0)} 次
- 运行时长: {stats.get('runningTime', '00:00:00')}
- 累计专注: {stats.get('focusTime', '00:00:00')} ({stats.get('totalFocusMinutes', 0)} 分钟)
- 连续专注: {stats.get('continuousFocusMinutes', 0)} 分钟
- 当前时间: {stats.get('currentTime', '')}

### 鼓励判断
- 自上次鼓励后的连续专注: {incremental_focus} 分钟
- 鼓励门槛: {encouragement_threshold} 分钟
- 是否达到鼓励条件: {'是' if incremental_focus >= encouragement_threshold else '否'} ({incremental_focus} >= {encouragement_threshold})
- 【注意】抑制鼓励: {'是（即将触发休息提醒，跳过本次鼓励）' if suppress_encouragement else '否'}

### 休息提醒判断（优先级更高）
- 自上次休息提醒后的累计专注: {incremental_rest} 分钟
- 休息提醒门槛: {rest_threshold} 分钟
- 【重要】是否需要休息提醒: {'是' if reached_rest else '否'} ({incremental_rest} >= {rest_threshold})

## 关键指令
{'🛑 需要休息提醒！必须执行以下操作（优先级最高）：' if reached_rest else ('🎉 已达到鼓励里程碑！必须执行以下操作：' if reached_encouragement else '未达到任何里程碑，正常判断即可。')}
{'''1. status 设置为 "focused"
2. shouldSpeak 必须设置为 true（语音播放休息提醒）
3. message 使用温馨的休息提醒，提及累计专注分钟数和建议休息时长，例如："已经累计专注''' + str(stats.get('totalFocusMinutes', 0)) + '''分钟了，该休息一下啦，站起来活动5分钟吧！"''' if reached_rest else ('''1. status 设置为 "focused"
2. shouldSpeak 必须设置为 true（语音播放鼓励）
3. message 使用热情的鼓励话语，提及连续专注分钟数，例如："太棒了！已经连续专注''' + str(stats.get('continuousFocusMinutes', 0)) + '''分钟了，继续保持！"''' if reached_encouragement else '')}
"""
    
    content_parts.append({
        "type": "text",
        "text": text_instruction
    })
    
    # 添加图片
    content_parts.append({
        "type": "image_url",
        "image_url": {
            "url": image_base64  # 直接使用 data URI
        }
    })
    
    return content_parts


def get_system_prompt() -> str:
    """获取 System Prompt"""
    return SYSTEM_PROMPT
