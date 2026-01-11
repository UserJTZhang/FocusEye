/**
 * 摄像头和图片处理工具
 */

/**
 * 从视频流截取图片并压缩
 * @param {HTMLVideoElement} videoElement - 视频元素
 * @param {HTMLCanvasElement} canvasElement - Canvas 元素
 * @param {Object} options - 配置选项
 * @returns {string} Base64 编码的图片
 */
export function captureImage(videoElement, canvasElement, options = {}) {
  const {
    maxSize = 800,      // 最大边长
    quality = 0.5,      // 压缩质量
    format = 'image/jpeg' // 图片格式
  } = options

  if (!videoElement || !canvasElement) {
    throw new Error('视频或 Canvas 元素不存在')
  }

  // 获取视频尺寸
  const videoWidth = videoElement.videoWidth
  const videoHeight = videoElement.videoHeight

  if (videoWidth === 0 || videoHeight === 0) {
    throw new Error('视频尺寸无效')
  }

  // 计算压缩后的尺寸（保持宽高比）
  let targetWidth = videoWidth
  let targetHeight = videoHeight

  if (videoWidth > videoHeight) {
    if (videoWidth > maxSize) {
      targetWidth = maxSize
      targetHeight = (videoHeight * maxSize) / videoWidth
    }
  } else {
    if (videoHeight > maxSize) {
      targetHeight = maxSize
      targetWidth = (videoWidth * maxSize) / videoHeight
    }
  }

  // 设置 Canvas 尺寸
  canvasElement.width = targetWidth
  canvasElement.height = targetHeight

  // 绘制视频帧到 Canvas
  const ctx = canvasElement.getContext('2d')
  ctx.drawImage(videoElement, 0, 0, targetWidth, targetHeight)

  // 转换为 Base64
  const base64Image = canvasElement.toDataURL(format, quality)

  return base64Image
}

/**
 * 请求摄像头权限
 * @param {Object} constraints - 约束条件
 * @returns {Promise<MediaStream>} 媒体流
 */
export async function requestCamera(constraints = {}) {
  const defaultConstraints = {
    video: {
      facingMode: 'user',
      width: { ideal: 1280 },
      height: { ideal: 720 }
    },
    audio: false
  }

  const finalConstraints = { ...defaultConstraints, ...constraints }

  try {
    const stream = await navigator.mediaDevices.getUserMedia(finalConstraints)
    return stream
  } catch (error) {
    console.error('摄像头访问失败:', error)
    throw new Error('无法访问摄像头，请检查权限设置')
  }
}

/**
 * 停止媒体流
 * @param {MediaStream} stream - 媒体流
 */
export function stopMediaStream(stream) {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
  }
}
