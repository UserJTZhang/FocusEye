<template>
  <div class="app-container">
    <!-- 视频预览区域 -->
    <div class="video-container" :class="{ minimized: isMonitoring }">
      <video 
        ref="videoRef" 
        autoplay 
        playsinline
        :class="{ mirror: isFrontCamera }"
      ></video>
      <canvas ref="canvasRef" style="display: none;"></canvas>
      
      <!-- 切换摄像头按钮 -->
      <button 
        v-if="cameraStarted && !isMonitoring" 
        @click="switchCamera" 
        class="switch-camera-btn"
        title="切换摄像头"
      >
        <img src="/icon/cameraFlip.png" alt="切换摄像头" />
      </button>
    </div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <!-- 状态指示灯 -->
      <div class="status-indicator" :class="statusClass">
        <span class="dot"></span>
        <span class="label">{{ statusText }}</span>
      </div>

      <!-- 反馈消息 -->
      <div class="feedback-message" v-if="lastMessage">
        <p>{{ lastMessage }}</p>
      </div>

      <!-- 配置选项（仅在摄像头开启且未监督时显示） -->
      <div class="config-section" v-if="cameraStarted && !isMonitoring">
        <div class="config-item">
          <label>监督场景</label>
          <select v-model="monitorScene" @change="saveScene">
            <option value="reading">📚 专心读书</option>
            <option value="homework">✍️ 专心写作业</option>
            <option value="eating">🍽️ 专心吃饭</option>
            <option value="fitness">💪 专心健身</option>
            <option value="computer">💻 电脑办公</option>
            <option value="tablet">📱 平板办公</option>
          </select>
        </div>
        <div class="config-item">
          <label>声音选择</label>
          <select v-model="selectedVoice" @change="saveVoice">
            <option v-for="voice in voiceList" :key="voice.voice_parameter" :value="voice.voice_parameter">
              {{ voice.name }} - {{ voice.characteristics }} ({{ voice.age }})
            </option>
          </select>
        </div>
        <div class="voice-preview" v-if="currentVoiceInfo">
          <div class="voice-info">
            <span class="voice-lang">
              <img src="/icon/language.png" alt="语言" class="language-icon" />
              {{ currentVoiceInfo.language.join('、') }}
            </span>
            <button @click="playVoicePreview" class="btn-preview" :class="{ 'btn-stop': isPlayingPreview }">
              <template v-if="isPlayingPreview">
                <img src="/icon/stop.png" alt="停止" class="stop-icon" />
                停止
              </template>
              <template v-else>
                <img src="/icon/horn.png" alt="试听" class="horn-icon" />
                试听
              </template>
            </button>
          </div>
        </div>
        <div class="config-item">
          <label>鼓励间隔</label>
          <select v-model.number="encouragementInterval" @change="validateIntervals">
            <option :value="1">1分钟</option>
            <option :value="2">2分钟</option>
            <option :value="3">3分钟</option>
            <option :value="5">5分钟</option>
            <option :value="10">10分钟</option>
            <option :value="15">15分钟</option>
            <option :value="20">20分钟</option>
            <option :value="30">30分钟</option>
            <option :value="40">40分钟</option>
            <option :value="50">50分钟</option>
            <option :value="60">60分钟</option>
          </select>
        </div>
        <div class="config-item">
          <label>休息提醒</label>
          <select v-model.number="restReminderInterval" @change="validateIntervals">
            <option :value="5">5分钟</option>
            <option :value="8">8分钟</option>
            <option :value="10">10分钟</option>
            <option :value="15">15分钟</option>
            <option :value="20">20分钟</option>
            <option :value="25">25分钟</option>
            <option :value="30">30分钟</option>
            <option :value="40">40分钟</option>
            <option :value="50">50分钟</option>
            <option :value="60">60分钟</option>
          </select>
        </div>
        <p class="config-hint" v-if="configError">{{ configError }}</p>
      </div>

      <!-- 控制按钮 -->
      <div class="button-group">
        <button 
          v-if="!cameraStarted" 
          @click="startCamera" 
          class="btn btn-primary"
        >
          开启摄像头
        </button>
        
        <template v-else>
          <button 
            v-if="!isMonitoring" 
            @click="startMonitoring" 
            class="btn btn-success"
            :disabled="!!configError"
          >
            开始监督
          </button>
          <button 
            v-else 
            @click="stopMonitoring" 
            class="btn btn-danger"
          >
            停止监督
          </button>
        </template>
      </div>

      <!-- 统计信息 -->
      <div class="stats" v-if="isMonitoring">
        <div class="stat-item">
          <span class="label">运行时长</span>
          <span class="value">{{ runningTime }}</span>
        </div>
        <div class="stat-item">
          <span class="label">检查次数</span>
          <span class="value">{{ checkCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">累计专注</span>
          <span class="value">{{ focusTime }}</span>
        </div>
        <div class="stat-item">
          <span class="label">连续专注</span>
          <span class="value">{{ continuousFocusTime }}</span>
        </div>
      </div>
    </div>

    <!-- 加载指示器 -->
    <div class="loading-overlay" v-if="isAnalyzing">
      <div class="spinner"></div>
      <p>AI 分析中...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { captureImage } from './utils/camera'
import { analyzeImage, checkHealth } from './utils/api'
import { speakMessage, playAudioFile, stopAllAudio, isAudioPlaying } from './utils/tts'
import { formatTime } from './utils/format'
import './App.css'

// 引用
const videoRef = ref(null)
const canvasRef = ref(null)

// 状态管理
const cameraStarted = ref(false)
const isMonitoring = ref(false)
const isAnalyzing = ref(false)
const isFrontCamera = ref(true)

// 监督数据
const lastMessage = ref('')
const currentStatus = ref('idle') // idle, focused, distracted, away
const checkCount = ref(0)
const focusCount = ref(0)
const startTime = ref(null)
const runningTime = ref('00:00:00')
const focusTime = ref('00:00:00')
const continuousFocusTime = ref('00:00:00') // 连续专注时长
const lastDistractionTime = ref(null) // 上次分心的时间
const lastCheckTime = ref(null) // 上次检查的时间
const totalFocusMillis = ref(0) // 累计专注时长（毫秒）
const lastEncouragementMinutes = ref(0) // 上次鼓励时的连续专注时长（分钟）
const lastRestReminderMinutes = ref(0) // 上次休息提醒时的累计专注时长（分钟）

// 配置数据
const monitorInterval = ref(60) // 监督间隔（秒）
const monitorIntervalRandom = ref(10) // 随机波动（秒）
const monitorScene = ref(localStorage.getItem('monitorScene') || 'reading') // 监督场景
const encouragementInterval = ref(parseInt(localStorage.getItem('encouragementInterval')) || 20) // 鼓励间隔（分钟）
const restReminderInterval = ref(parseInt(localStorage.getItem('restReminderInterval')) || 30) // 休息提醒间隔（分钟）
const configError = ref('') // 配置错误提示

// 声音配置
const voiceList = ref([]) // 声音列表
const selectedVoice = ref(localStorage.getItem('selectedVoice') || 'longanyang') // 选中的声音
const isPlayingPreview = ref(false) // 是否正在播放试听

// 定时器
let monitorTimer = null
let statsTimer = null

// 媒体流
let mediaStream = null

// 屏幕唤醒锁（防止息屏）
let wakeLock = null

// 计算属性
const statusClass = computed(() => {
  return {
    'status-idle': currentStatus.value === 'idle',
    'status-focused': currentStatus.value === 'focused',
    'status-distracted': currentStatus.value === 'distracted',
    'status-away': currentStatus.value === 'away',
    'status-error': currentStatus.value === 'error'
  }
})

const statusText = computed(() => {
  const statusMap = {
    idle: '待机中',
    focused: '专注中',
    distracted: '分心了',
    away: '离开了',
    error: '错误'
  }
  return statusMap[currentStatus.value] || '未知'
})

// 当前选中声音的详细信息
const currentVoiceInfo = computed(() => {
  return voiceList.value.find(v => v.voice_parameter === selectedVoice.value)
})

// 开启摄像头
async function startCamera(useFrontCamera = true) {
  console.log('🎥 正在开启摄像头...', useFrontCamera ? '前置' : '后置')
  try {
    // 先停止现有的媒体流
    if (mediaStream) {
      mediaStream.getTracks().forEach(track => track.stop())
    }

    const constraints = {
      video: {
        facingMode: useFrontCamera ? 'user' : 'environment',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    }

    mediaStream = await navigator.mediaDevices.getUserMedia(constraints)
    
    if (videoRef.value) {
      videoRef.value.srcObject = mediaStream
      cameraStarted.value = true
      console.log('✅ 摄像头已开启，cameraStarted =', cameraStarted.value)
      
      // 检测是否为前置摄像头
      const videoTrack = mediaStream.getVideoTracks()[0]
      const settings = videoTrack.getSettings()
      isFrontCamera.value = settings.facingMode === 'user'
      console.log('📷 摄像头类型:', isFrontCamera.value ? '前置' : '后置')
    }
  } catch (error) {
    console.error('❌ 摄像头启动失败:', error)
    alert('无法访问摄像头，请检查权限设置')
  }
}

// 切换摄像头
async function switchCamera() {
  console.log('🔄 切换摄像头...')
  await startCamera(!isFrontCamera.value)
}

// 请求屏幕保持常亮（防止息屏）
async function requestWakeLock() {
  try {
    console.log('🔆 尝试启用屏幕保持常亮...')
    
    // 检查浏览器支持
    if (!('wakeLock' in navigator)) {
      console.warn('⚠️ 当前浏览器不支持 Wake Lock API')
      console.warn('   支持的浏览器：Chrome 84+, Edge 84+, Safari 16.4+')
      return
    }
    
    // 检查页面可见性
    if (document.hidden) {
      console.warn('⚠️ 页面不可见，无法启用 Wake Lock')
      return
    }
    
    // 检查是否为安全上下文（HTTPS 或 localhost）
    if (!window.isSecureContext) {
      console.warn('⚠️ 非安全上下文（需要 HTTPS 或 localhost）')
      return
    }
    
    // 释放旧的 Wake Lock
    if (wakeLock) {
      await wakeLock.release()
      wakeLock = null
    }
    
    // 请求新的 Wake Lock
    wakeLock = await navigator.wakeLock.request('screen')
    console.log('✅ 屏幕保持常亮已启用')
    
    // 监听释放事件
    wakeLock.addEventListener('release', () => {
      console.log('🌙 屏幕保持常亮已释放')
      wakeLock = null
    })
  } catch (err) {
    console.error('❌ 无法启用屏幕保持常亮:', err.name, err.message)
    if (err.name === 'NotAllowedError') {
      console.warn('   原因：权限被拒绝或页面不在前台')
    }
  }
}

// 释放屏幕唤醒锁
async function releaseWakeLock() {
  if (wakeLock) {
    try {
      await wakeLock.release()
      console.log('🌙 已释放屏幕保持常亮')
    } catch (err) {
      console.error('❌ 释放 Wake Lock 失败:', err)
    }
    wakeLock = null
  }
}

// 播放欢迎音效
function playWelcomeSound() {
  // 根据用户选择的音色播放对应的欢迎语
  const voiceParam = selectedVoice.value || 'longanyang'
  const audioUrl = `/voice/${voiceParam}.mp3`
  
  console.log('🎵 播放欢迎语:', voiceParam)
  playAudioFile(audioUrl, 0.6).catch(err => {
    console.warn('⚠️ 欢迎音效播放失败:', err)
  })
}

// 开始监督
async function startMonitoring() {
  console.log('🚀 开始监督，cameraStarted =', cameraStarted.value)
  if (!cameraStarted.value) {
    alert('请先开启摄像头')
    return
  }

  isMonitoring.value = true
  startTime.value = Date.now()
  checkCount.value = 0
  focusCount.value = 0
  lastDistractionTime.value = null
  lastCheckTime.value = Date.now()
  totalFocusMillis.value = 0
  lastEncouragementMinutes.value = 0
  lastRestReminderMinutes.value = 0

  // 播放欢迎音效
  playWelcomeSound()

  // 请求保持屏幕常亮（防止息屏）
  await requestWakeLock()

  // 启动随机间隔检查
  scheduleNextCheck()
  console.log(`⏰ 已启动随机间隔检测：${monitorInterval.value}±${monitorIntervalRandom.value}秒`)

  // 更新统计信息（每秒）
  statsTimer = setInterval(updateStats, 1000)
}

// 计算随机间隔时间
function getRandomInterval() {
  const base = monitorInterval.value * 1000
  const random = monitorIntervalRandom.value * 1000
  // 在 [base - random, base + random] 范围内随机
  const offset = Math.random() * (random * 2) - random
  return Math.max(1000, base + offset) // 最小1秒
}

// 调度下一次检查
function scheduleNextCheck() {
  if (monitorTimer) {
    clearTimeout(monitorTimer)
  }
  
  const nextInterval = getRandomInterval()
  console.log(`⏰ 下次检查将在 ${Math.round(nextInterval / 1000)} 秒后进行`)
  
  monitorTimer = setTimeout(async () => {
    await performCheck()
    // 检查完成后，如果还在监督中，调度下一次
    if (isMonitoring.value) {
      scheduleNextCheck()
    }
  }, nextInterval)
}

// 停止监督
function stopMonitoring() {
  isMonitoring.value = false
  
  if (monitorTimer) {
    clearTimeout(monitorTimer)  // 改用 clearTimeout
    monitorTimer = null
  }
  
  if (statsTimer) {
    clearInterval(statsTimer)
    statsTimer = null
  }

  // 释放屏幕唤醒锁
  releaseWakeLock()
  
  // 停止所有音频播放
  console.log('🔇 停止所有音频')
  stopAllAudio()
  isPlayingPreview.value = false  // 重置试听状态

  currentStatus.value = 'idle'
  lastMessage.value = ''
}

// 执行检查
async function performCheck() {
  if (isAnalyzing.value) {
    console.log('⏭️ 跳过：上一次分析还在进行中')
    return
  }

  try {
    isAnalyzing.value = true
    checkCount.value++
    console.log(`\n📸 第 ${checkCount.value} 次检查开始...`)

    // 截取图片
    const imageBase64 = captureImage(
      videoRef.value, 
      canvasRef.value,
      { maxSize: 800, quality: 0.5 }
    )
    console.log('✅ 图片已截取，大小约:', Math.round(imageBase64.length / 1024), 'KB')

    // 准备统计信息
    const elapsed = Date.now() - startTime.value
    const currentTime = new Date().toLocaleString('zh-CN')
    
    // 计算连续专注时长（分钟）
    let continuousFocusMinutes = 0
    if (!lastDistractionTime.value) {
      // 从未分心，连续专注时长 = 总运行时长
      continuousFocusMinutes = Math.floor(elapsed / 60000)
    } else {
      // 从上次分心后的专注时长
      continuousFocusMinutes = Math.floor((Date.now() - lastDistractionTime.value) / 60000)
    }
    
    // 计算自上次鼓励后的增量专注时长
    const incrementalFocusMinutes = continuousFocusMinutes - lastEncouragementMinutes.value
    
    // 计算累计专注时长（分钟）- 实时计算，加上当前间隔
    let totalFocusMinutes = Math.floor(totalFocusMillis.value / 60000)
    if (lastCheckTime.value) {
      // 加上这次预计的间隔时间（假设这次也是专注）
      const currentInterval = Date.now() - lastCheckTime.value
      totalFocusMinutes = Math.floor((totalFocusMillis.value + currentInterval) / 60000)
    }
    
    // 计算自上次休息提醒后的累计专注时长
    const incrementalRestMinutes = totalFocusMinutes - lastRestReminderMinutes.value
    
    // 判断是否应该抑制鼓励（只在达到休息提醒门槛时才抑制）
    const aboutToRest = incrementalRestMinutes >= restReminderInterval.value
    
    const stats = {
      checkCount: checkCount.value,
      runningTime: formatTime(elapsed),
      focusTime: formatTime(totalFocusMillis.value),  // 使用实际累计时间
      currentTime: currentTime,
      scene: monitorScene.value,  // 监督场景
      continuousFocusMinutes: continuousFocusMinutes,
      incrementalFocusMinutes: incrementalFocusMinutes,  // 增量连续专注时长
      totalFocusMinutes: totalFocusMinutes,  // 累计专注时长（分钟）
      incrementalRestMinutes: incrementalRestMinutes,  // 增量累计专注时长
      encouragementInterval: encouragementInterval.value,
      restReminderInterval: restReminderInterval.value,
      suppressEncouragement: aboutToRest  // 是否抑制鼓励
    }
    
    // 调用 API 分析
    console.log('📡 正在调用 API 分析...')
    console.log('📊 统计信息:', stats)
    console.log(`   - 连续专注: ${continuousFocusMinutes} 分钟`)
    console.log(`   - 上次鼓励: ${lastEncouragementMinutes.value} 分钟`)
    console.log(`   - 增量专注: ${incrementalFocusMinutes} 分钟`)
    console.log(`   - 鼓励门槛: ${encouragementInterval.value} 分钟`)
    console.log(`   - 累计专注: ${totalFocusMinutes} 分钟`)
    console.log(`   - 上次休息提醒: ${lastRestReminderMinutes.value} 分钟`)
    console.log(`   - 增量累计: ${incrementalRestMinutes} 分钟`)
    console.log(`   - 休息门槛: ${restReminderInterval.value} 分钟`)
    console.log(`   - 鼓励条件: ${incrementalFocusMinutes >= encouragementInterval.value}`)
    console.log(`   - 休息条件: ${incrementalRestMinutes >= restReminderInterval.value}`)
    console.log(`   - 即将休息: ${aboutToRest}（抑制鼓励: ${aboutToRest}）`)
    const result = await analyzeImage(imageBase64, stats)
    console.log('📊 分析结果:', result)
    console.log(`   - shouldSpeak: ${result.shouldSpeak}`)

    if (result.success) {
      currentStatus.value = result.status
      lastMessage.value = result.message
      console.log(`✅ 状态: ${result.status}, 消息: ${result.message}`)

      // 统计专注次数和更新分心时间
      if (result.status === 'focused') {
        focusCount.value++
        // 累加实际专注时间（从上次检查到现在）
        if (lastCheckTime.value) {
          const interval = Date.now() - lastCheckTime.value
          totalFocusMillis.value += interval
          console.log(`💚 本次专注: ${Math.round(interval/1000)}秒, 累计: ${formatTime(totalFocusMillis.value)}`)
        }
        
        // 如果这次鼓励或休息提醒了，更新相应的记录
        if (result.shouldSpeak) {
          // 使用之前计算好的连续专注时长（已包含当前间隔）
          const currentContinuousFocus = continuousFocusMinutes
          
          // 使用之前计算好的累计专注时长（已包含当前间隔）
          const currentTotalFocus = totalFocusMinutes
          
          // 判断是休息提醒还是鼓励（根据 message 内容）
          const isRestReminder = result.message.includes('休息') || result.message.includes('放松') || result.message.includes('活动')
          
          if (isRestReminder) {
            // 休息提醒：同时更新休息和鼓励记录
            lastRestReminderMinutes.value = currentTotalFocus
            lastEncouragementMinutes.value = currentContinuousFocus  // 休息提醒也算一次鼓励
            console.log(`🛑 已提醒休息，记录累计时长: ${currentTotalFocus} 分钟`)
            console.log(`   同时更新鼓励记录: ${currentContinuousFocus} 分钟（休息提醒也算鼓励）`)
          } else {
            // 普通鼓励
            lastEncouragementMinutes.value = currentContinuousFocus
            console.log(`🎉 已鼓励，记录连续时长: ${currentContinuousFocus} 分钟`)
          }
        }
      } else if (result.status === 'distracted' || result.status === 'away') {
        // 记录分心时间
        lastDistractionTime.value = Date.now()
        lastEncouragementMinutes.value = 0  // 重置上次鼓励时长
        console.log('💔 已记录分心时间，连续专注时长将重置')
      }
      
      // 更新上次检查时间
      lastCheckTime.value = Date.now()

      // 仅在需要时播放语音反馈
      if (result.shouldSpeak) {
        console.log('🔊 播放语音反馈...')
        speakMessage(result.message)
      } else {
        console.log('🔇 跳过语音播放（正常专注状态）')
      }
    } else {
      currentStatus.value = 'error'
      lastMessage.value = result.message || '分析失败'
      console.error('❌ 分析失败:', result.message || result.error)
    }
  } catch (error) {
    console.error('❌ 检查失败:', error)
    currentStatus.value = 'error'
    lastMessage.value = '网络错误，请检查连接'
  } finally {
    isAnalyzing.value = false
    console.log('✅ 本次检查完成\n')
  }
}

// 更新统计信息
function updateStats() {
  if (!startTime.value) return

  const elapsed = Date.now() - startTime.value
  runningTime.value = formatTime(elapsed)

  // 使用实际累计专注时间
  focusTime.value = formatTime(totalFocusMillis.value)
  
  // 计算连续专注时长
  if (!lastDistractionTime.value) {
    // 从未分心，连续专注 = 总运行时长
    continuousFocusTime.value = formatTime(elapsed)
  } else {
    // 从上次分心后的时间
    const continuousElapsed = Date.now() - lastDistractionTime.value
    continuousFocusTime.value = formatTime(continuousElapsed)
  }
}

// 页面可见性监听
async function handleVisibilityChange() {
  if (document.hidden) {
    // 页面切换到后台时释放 wake lock
    releaseWakeLock()
  } else if (isMonitoring.value) {
    // 页面重新可见且正在监督时，重新请求 wake lock
    await requestWakeLock()
  }
}

// 保存场景
function saveScene() {
  localStorage.setItem('monitorScene', monitorScene.value)
  console.log(`✅ 场景已保存: ${monitorScene.value}`)
}

// 保存声音选择
function saveVoice() {
  localStorage.setItem('selectedVoice', selectedVoice.value)
  console.log(`✅ 声音已保存: ${selectedVoice.value}`)
}

// 试听声音
function playVoicePreview() {
  const voiceInfo = currentVoiceInfo.value
  if (!voiceInfo || !voiceInfo.audio_url) return
  
  // 如果正在播放，则停止
  if (isPlayingPreview.value) {
    console.log('⏸️ 停止试听')
    stopAllAudio()
    isPlayingPreview.value = false
    return
  }
  
  // 播放试听
  console.log('🎵 试听音色:', voiceInfo.name)
  isPlayingPreview.value = true
  playAudioFile(voiceInfo.audio_url, 0.6)
    .then(() => {
      isPlayingPreview.value = false
    })
    .catch(error => {
      console.error('播放试听失败:', error)
      isPlayingPreview.value = false
    })
}

// 加载声音配置
async function loadVoiceConfig() {
  try {
    const response = await fetch('/voice_config.json')
    const data = await response.json()
    voiceList.value = data.voices || []
    console.log(`✅ 声音配置已加载: ${voiceList.value.length} 个声音`)
  } catch (error) {
    console.error('⚠️ 加载声音配置失败:', error)
  }
}

// 验证配置
function validateIntervals() {
  if (encouragementInterval.value >= restReminderInterval.value) {
    configError.value = '⚠️ 鼓励间隔必须小于休息提醒间隔'
    return false
  }
  configError.value = ''
  // 保存到 localStorage
  localStorage.setItem('encouragementInterval', encouragementInterval.value.toString())
  localStorage.setItem('restReminderInterval', restReminderInterval.value.toString())
  console.log(`✅ 配置已保存: 鼓励间隔=${encouragementInterval.value}分钟, 休息提醒=${restReminderInterval.value}分钟`)
  return true
}

// 获取配置
async function loadConfig() {
  try {
    const result = await checkHealth()
    if (result.success && result.config) {
      monitorInterval.value = result.config.monitorInterval || 60
      monitorIntervalRandom.value = result.config.monitorIntervalRandom || 10
      // 鼓励和休息间隔从 localStorage 读取，不再从后端获取
      console.log(`✅ 配置已加载: 监督间隔=${monitorInterval.value}±${monitorIntervalRandom.value}秒, 鼓励间隔=${encouragementInterval.value}分钟, 休息提醒=${restReminderInterval.value}分钟`)
    }
  } catch (error) {
    console.warn('⚠️ 加载配置失败，使用默认值', error)
  }
}

// 初始化时验证配置
function initConfig() {
  validateIntervals()
}

// 生命周期
onMounted(() => {
  document.addEventListener('visibilitychange', handleVisibilityChange)
  loadConfig()  // 加载配置
  loadVoiceConfig()  // 加载声音配置
  initConfig()  // 初始化配置验证
})

onUnmounted(() => {
  // 清理资源
  stopMonitoring()
  releaseWakeLock()
  
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }
  
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})
</script>
