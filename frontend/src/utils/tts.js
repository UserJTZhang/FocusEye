/**
 * 文本转语音 (TTS) 工具
 * 使用阿里云 CosyVoice HTTP API
 */

// 全局当前播放的音频对象（确保同时只播放一个）
let globalCurrentAudio = null

/**
 * 停止全局当前播放的音频
 */
function stopGlobalAudio() {
  if (globalCurrentAudio) {
    console.log('⏸️ 停止全局音频')
    globalCurrentAudio.pause()
    globalCurrentAudio.currentTime = 0
    globalCurrentAudio = null
  }
}

/**
 * 语音播放队列
 */
class SpeechQueue {
  constructor() {
    this.queue = []
    this.isSpeaking = false
    this.currentAudio = null  // 存储当前正在播放的音频对象
  }

  /**
   * 添加到队列
   * @param {string} text - 要播放的文本
   */
  add(text) {
    // 打断全局正在播放的任何音频
    stopGlobalAudio()
    
    // 清空队列，只保留最新的
    this.queue = [text]
    this.isSpeaking = false
    this.process()
  }

  /**
   * 处理队列
   */
  async process() {
    if (this.isSpeaking || this.queue.length === 0) {
      return
    }

    this.isSpeaking = true
    const text = this.queue.shift()

    try {
      await this.speak(text)
    } catch (error) {
      console.error('🔊 语音播放失败:', error)
    } finally {
      this.isSpeaking = false
      // 继续处理下一个
      if (this.queue.length > 0) {
        this.process()
      }
    }
  }

  /**
   * 使用阿里云 CosyVoice API 播放语音（HTTP 方式）
   * @param {string} text - 文本
   * @returns {Promise<void>}
   */
  async speak(text) {
    await this.speakHttp(text)
  }

  /**
   * HTTP API 方式合成语音
   */
  async speakHttp(text) {
    try {
      console.log('🎤 调用 CosyVoice API:', text)
      
      // 从 localStorage 读取用户选择的声音，默认使用龙安洋
      const selectedVoice = localStorage.getItem('selectedVoice') || 'longanyang'
      console.log('🎵 使用声音:', selectedVoice)
      
      const response = await fetch('/api/tts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: text,
          model: 'cosyvoice-v3-flash',
          voice: selectedVoice
        })
      })

      if (!response.ok) {
        // 尝试获取错误详情
        let errorDetail = `TTS API 错误: ${response.status}`
        try {
          const errorData = await response.json()
          errorDetail = errorData.error || errorData.message || errorDetail
        } catch (e) {
          // 无法解析错误响应
        }
        console.error('❌', errorDetail)
        throw new Error(errorDetail)
      }

      const audioBlob = await response.blob()
      console.log('🎵 音频大小:', Math.round(audioBlob.size / 1024), 'KB')
      await this.playAudio(audioBlob)
      
    } catch (error) {
      console.error('❌ HTTP TTS 失败:', error)
      throw error
    }
  }

  /**
   * 播放音频 Blob
   */
  async playAudio(audioBlob) {
    return new Promise((resolve, reject) => {
      try {
        const audio = new Audio(URL.createObjectURL(audioBlob))
        this.currentAudio = audio  // 记录到实例
        globalCurrentAudio = audio  // 记录到全局
        
        audio.onended = () => {
          URL.revokeObjectURL(audio.src)
          console.log('✅ 语音播放完成')
          this.currentAudio = null
          if (globalCurrentAudio === audio) {
            globalCurrentAudio = null
          }
          resolve()
        }
        
        audio.onerror = (error) => {
          URL.revokeObjectURL(audio.src)
          console.error('❌ 音频播放错误:', error)
          this.currentAudio = null
          if (globalCurrentAudio === audio) {
            globalCurrentAudio = null
          }
          reject(error)
        }
        
        console.log('🔊 开始播放语音...')
        audio.play().catch(err => {
          console.error('❌ play() 失败:', err)
          this.currentAudio = null
          if (globalCurrentAudio === audio) {
            globalCurrentAudio = null
          }
          reject(err)
        })
        
      } catch (error) {
        this.currentAudio = null
        if (globalCurrentAudio === audio) {
          globalCurrentAudio = null
        }
        reject(error)
      }
    })
  }

  /**
   * 清空队列
   */
  clear() {
    // 停止当前播放的音频
    stopGlobalAudio()
    this.currentAudio = null
    this.queue = []
    this.isSpeaking = false
  }
}

// 创建全局实例
const speechQueue = new SpeechQueue()

/**
 * 播放语音消息
 * @param {string} message - 消息文本
 */
export function speakMessage(message) {
  if (message && message.trim()) {
    speechQueue.add(message)
  }
}

/**
 * 停止所有语音
 */
export function stopSpeaking() {
  speechQueue.clear()
}

/**
 * 检查 TTS 支持
 * @returns {boolean} 是否支持
 */
export function isTTSSupported() {
  return true // WebSocket TTS 始终可用
}

/**
 * 播放音频文件（用于欢迎音效、试听等）
 * @param {string} url - 音频文件 URL
 * @param {number} volume - 音量 (0-1)
 * @returns {Promise<void>}
 */
export function playAudioFile(url, volume = 0.6) {
  return new Promise((resolve, reject) => {
    try {
      // 先停止全局当前播放的音频
      stopGlobalAudio()
      
      const audio = new Audio(url)
      audio.volume = volume
      globalCurrentAudio = audio
      
      audio.onended = () => {
        console.log('✅ 音频播放完成:', url)
        if (globalCurrentAudio === audio) {
          globalCurrentAudio = null
        }
        resolve()
      }
      
      audio.onerror = (error) => {
        console.error('❌ 音频播放错误:', error)
        if (globalCurrentAudio === audio) {
          globalCurrentAudio = null
        }
        reject(error)
      }
      
      console.log('🔊 播放音频文件:', url)
      audio.play().catch(err => {
        console.warn('⚠️ 播放失败:', err)
        if (globalCurrentAudio === audio) {
          globalCurrentAudio = null
        }
        reject(err)
      })
      
    } catch (error) {
      console.error('❌ 音频加载失败:', error)
      reject(error)
    }
  })
}

/**
 * 停止所有音频播放
 */
export function stopAllAudio() {
  stopGlobalAudio()
  speechQueue.clear()
}

/**
 * 检查是否有音频正在播放
 * @returns {boolean}
 */
export function isAudioPlaying() {
  return globalCurrentAudio !== null
}
