/**
 * API 通信工具
 */

// API 基础 URL（生产环境会被替换）
// 开发环境：如果在移动设备访问，需要使用电脑的局域网IP
const API_BASE_URL = import.meta.env.VITE_API_URL || (
  // 如果是本机访问、通过隧道访问或 HTTPS 访问，使用代理
  window.location.hostname === 'localhost' || 
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname.includes('lhr.life') ||
  window.location.hostname.includes('vicp.fun') ||  // 支持 vicp.fun 隧道
  window.location.protocol === 'https:'  // 所有 HTTPS 访问都使用代理
    ? '/api'  
    // 其他情况（局域网 HTTP 直接访问），使用局域网 IP
    : 'http://192.168.1.25:5001/api'
)

/**
 * 分析图片
 * @param {string} imageBase64 - Base64 编码的图片
 * @param {Object} stats - 监督统计信息
 * @param {string} voiceParameter - 声音参数
 * @returns {Promise<Object>} 分析结果
 */
export async function analyzeImage(imageBase64, stats = null) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: imageBase64,
        stats: stats  // 传递统计信息
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('API 调用失败:', error)
    return {
      success: false,
      status: 'error',
      message: '网络错误，请稍后重试',
      error: error.message
    }
  }
}

/**
 * 健康检查
 * @returns {Promise<Object>} 健康状态
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET'
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('健康检查失败:', error)
    return {
      success: false,
      status: 'unhealthy',
      error: error.message
    }
  }
}
