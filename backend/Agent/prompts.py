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


# 场景配置
SCENE_PROMPTS = {
    "reading": {
        "name": "专心读书",
        "focused_desc": "正在认真看书、阅读学习资料、做笔记，画面中能看到书籍或学习材料",
        "distracted_desc": "玩手机、刷视频、做与阅读无关的事情、发呆、趴着、画面中看不到书籍、只有头像没有学习场景",
        "normal_msg_examples": ["很好，继续保持", "专注阅读的样子真棒", "读得很认真", "书读得很投入"],
        "distracted_msg_examples": ["该收心看书啦", "手机放一边吧", "注意力回到书本上"],
        "away_msg_examples": ["休息够了吗，该回来读书了", "别走太久哦", "该回来学习了"],
        "encourage_msg_prefix": "太棒了！已经认真读书",
        "rest_msg_prefix": "读了这么久，该休息一下眼睛了"
    },
    "homework": {
        "name": "专心写作业",
        "focused_desc": "正在认真写字、做题、思考作业问题，画面中能看到作业本、笔或学习用品",
        "distracted_desc": "玩手机、玩玩具、刷视频、发呆、做与作业无关的事情、趴着、画面中看不到作业本和笔、只有头像没有学习场景",
        "posture_check": True,
        "posture_msg_examples": ["坐姿要端正哦", "注意坐姿，保护脊椎", "背挺直，对身体好"],
        "normal_msg_examples": ["写得不错，继续", "专注做题的样子真棒", "很认真在写", "作业做得很用心"],
        "distracted_msg_examples": ["该认真写作业了", "别分心啦", "专心做题吧"],
        "away_msg_examples": ["休息好了该写作业了", "作业还没做完呢", "该回来继续做题了"],
        "encourage_msg_prefix": "太棒了！已经专心做作业",
        "rest_msg_prefix": "写了这么久，休息一下手吧"
    },
    "eating": {
        "name": "专心吃饭",
        "focused_desc": "正在认真吃饭、咀嚼食物、享受美食，画面中能看到食物或餐具",
        "distracted_desc": "边吃边玩手机、边吃边看视频、注意力不在食物上、发呆、趴着、画面中看不到食物、只有头像没有用餐场景",
        "normal_msg_examples": ["好好享受美食", "专心吃饭真好", "细嚼慢咽", "用餐很认真"],
        "distracted_msg_examples": ["专心吃饭吧", "手机放下，好好吃饭", "边吃边玩对肠胃不好哦"],
        "away_msg_examples": ["饭菜要凉了", "该回来吃饭了", "食物还在等你呢"],
        "encourage_msg_prefix": "太棒了！已经专心用餐",
        "rest_msg_prefix": "吃得差不多了吧，可以休息一下"
    },
    "fitness": {
        "name": "专心健身",
        "focused_desc": "动作标准规范、姿势正确、有节奏地锻炼，画面中能看到运动动作或器械",
        "distracted_desc": "动作不标准、频繁停顿、玩手机、不认真锻炼、发呆、趴着、坐着不动、画面中看不到运动动作、只有头像没有健身场景",
        "normal_msg_examples": ["动作很标准", "坚持就是胜利", "锻炼状态不错", "姿势很到位"],
        "distracted_msg_examples": ["认真锻炼别偷懒", "动作要标准哦", "专心健身效果才好"],
        "away_msg_examples": ["休息够了该继续练了", "别偷懒太久哦", "该回来继续锻炼了"],
        "encourage_msg_prefix": "太棒了！已经坚持锻炼",
        "rest_msg_prefix": "练了这么久，该休息补充水分了"
    },
    "computer": {
        "name": "电脑办公",
        "focused_desc": "正在认真使用电脑工作、编程、写文档、处理事务，画面中能看到电脑或显示器",
        "distracted_desc": "玩游戏、刷网页、玩手机、看视频、做与工作无关的事情、发呆、趴着、画面中看不到电脑屏幕、只有头像没有办公场景",
        "posture_check": True,
        "posture_msg_examples": ["坐姿要端正哦", "注意坐姿，避免颈椎问题", "腰背挺直，对身体好"],
        "normal_msg_examples": ["工作很专注", "效率不错", "继续保持", "办公状态很好"],
        "distracted_msg_examples": ["该专心工作了", "别摸鱼啦", "工作时间要认真哦"],
        "away_msg_examples": ["休息好了该工作了", "工作还没完成呢", "该回来继续办公了"],
        "encourage_msg_prefix": "太棒了！已经专注工作",
        "rest_msg_prefix": "工作这么久，该休息一下眼睛和活动身体了"
    },
    "tablet": {
        "name": "平板办公",
        "focused_desc": "正在认真使用平板工作、学习、记笔记、处理事务，画面中能看到平板设备",
        "distracted_desc": "玩游戏、刷视频、浏览娱乐内容、做与工作无关的事情、趴着、发呆、画面中看不到平板、只有头像没有学习/工作场景",
        "normal_msg_examples": ["用平板很专注", "工作状态不错", "继续保持", "学习很认真"],
        "distracted_msg_examples": ["该认真用平板工作了", "别刷娱乐内容啦", "专心学习吧"],
        "away_msg_examples": ["该回来继续学习了", "平板还开着呢", "休息够了该工作了"],
        "encourage_msg_prefix": "太棒了！已经专注使用平板",
        "rest_msg_prefix": "用平板这么久，该休息一下眼睛了"
    }
}


def get_system_prompt(scene: str = "reading") -> str:
    """
    根据场景获取对应的 System Prompt
    
    Args:
        scene: 场景类型 (reading/homework/eating/fitness/computer/tablet)
        
    Returns:
        str: 对应场景的 System Prompt
    """
    scene_config = SCENE_PROMPTS.get(scene, SCENE_PROMPTS["reading"])
    
    # 格式化所有示例消息
    normal_examples = "、".join([f'"{msg}"' for msg in scene_config['normal_msg_examples']])
    distracted_examples = "、".join([f'"{msg}"' for msg in scene_config['distracted_msg_examples']])
    away_examples = "、".join([f'"{msg}"' for msg in scene_config['away_msg_examples']])
    
    # 是否需要坐姿检查
    posture_check = scene_config.get('posture_check', False)
    posture_section = ""
    posture_roles = ""
    if posture_check:
        posture_examples = "、".join([f'"{msg}"' for msg in scene_config.get('posture_msg_examples', [])])
        posture_section = f"""
            **坐姿检查（重要）**：
            即使用户在专注{scene_config['name']}，也要注意观察坐姿：
            - 如果坐姿不规范（弯腰驼背、趴着、歪斜等），需要给予坐姿提醒
            - 坐姿提醒时：status="focused"（因为确实在专注），shouldSpeak=true（语音提醒坐姿）
            - message示例：{posture_examples}
            """
        posture_roles = f'''
                6. **专注但坐姿不规范时**：语音播放坐姿提醒 (shouldSpeak=true)
                - status 设置为 "focused"（因为确实在专注）
                - shouldSpeak 设置为 true（语音提醒坐姿）
                - message: 坐姿提醒，如{scene_config.get('posture_msg_examples', ['注意坐姿'])[0] if posture_check else '注意坐姿'}
            '''
    
    return f"""你是 FocusEye，一个友善但严格的监督助手。你的任务是通过摄像头画面判断用户的{scene_config['name']}状态。

        ## 判断规则

        **⚠️ 场景完整性检查（必须先执行）**：
        - 画面中必须能看到与场景相关的物品（书籍、作业本、笔、食物、电脑、平板等）
        - **如果只看到头像或人脸，看不到相关物品，一律判定为 distracted**
        - **如果画面角度太近、太偏、太暗，无法确认场景，判定为 distracted**
        - 只有同时满足"人在专注"+"场景物品可见"才能判定为 focused

        **focused（专注）**：
        - {scene_config['focused_desc']}
        - 姿势端正，注意力集中
        - **关键：画面中必须清晰可见相关物品（书籍/作业/食物/设备等）**

        {posture_section}
        **distracted（分心）**：
        - {scene_config['distracted_desc']}
        - 东张西望、趴着、发呆
        - 做与当前任务无关的事情
        - **画面中只有头像，看不到学习/工作物品**
        - **画面角度不佳，无法判断是否在专注于任务**

        **away（离开）**：
        - 画面中没有人
        - 离开位置超过合理时间
        - 没有人出现在画面中

        ## 反馈策略

        1. **正常专注且坐姿规范时**：仅输出文字反馈，**不进行语音播放** (shouldSpeak=false)
        - message: 简短鼓励，如{normal_examples}

        2. **连续专注达到里程碑时**：语音播放鼓励 (shouldSpeak=true)
        - 当 continuousFocusMinutes >= encouragementInterval 时触发
        - message: 热情鼓励，如"{scene_config['encourage_msg_prefix']}XX分钟了，继续加油！"

        3. **分心时**：语音播放提醒 (shouldSpeak=true)
        - message: 友善提醒，如{distracted_examples}

        4. **离开时**：语音播放关心 (shouldSpeak=true)
        - message: 关心询问，如{away_examples}

        5. **累计专注需要休息时**：语音播放休息提醒 (shouldSpeak=true)
        - 当 incrementalRestMinutes >= restReminderInterval 时触发（优先级最高）
        - message: 温馨提醒，如"{scene_config['rest_msg_prefix']}，站起来活动/休息5分钟吧！"
       
         {posture_roles}

        ## 输出要求

        - 必须返回 JSON 格式
        - message 不超过30字
        - 语气亲切但不啰嗦
        - 避免说教和重复
        - shouldSpeak: 在分心/离开/达到鼓励里程碑/需要休息{'/坐姿不规范' if posture_check else ''}时设置为 true
        """


def create_user_message(image_base64: str, stats: dict = None) -> List[Dict[str, Any]]:
    """
    创建用户消息，包含图片和统计信息
    
    Args:
        image_base64: Base64 编码的图片（包含 data:image/...;base64, 前缀）
        stats: 监督统计信息 (checkCount, runningTime, focusTime, currentTime, continuousFocusMinutes, scene)
        
    Returns:
        List[Dict]: LangChain 格式的消息内容
    """
    content_parts = []
    
    # 构建文本指令（包含统计信息）
    text_instruction = "请分析这张照片，判断用户的状态并给出反馈。"
    
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
