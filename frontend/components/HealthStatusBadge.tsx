'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

interface HealthStatus {
  status: string
  error?: string
}

export default function HealthStatusBadge() {
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/api/v1/health`, {
          timeout: 5000,
        })
        setHealth({ status: response.data.status })
      } catch (error) {
        setHealth({ status: 'unhealthy', error: 'Backend unavailable' })
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 30000) // Check every 30 seconds

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="inline-flex items-center px-3 py-1 rounded-full bg-gray-200 text-gray-600 text-sm font-medium">
        <span className="mr-2 animate-pulse">●</span>
        Checking...
      </div>
    )
  }

  const isHealthy = health?.status === 'ok'
  const bgColor = isHealthy ? 'bg-green-100' : 'bg-red-100'
  const textColor = isHealthy ? 'text-green-700' : 'text-red-700'
  const dotColor = isHealthy ? 'text-green-500' : 'text-red-500'

  return (
    <div className={`inline-flex items-center px-3 py-1 rounded-full ${bgColor} ${textColor} text-sm font-medium`}>
      <span className={`mr-2 ${dotColor} text-lg`}>●</span>
      {isHealthy ? 'Backend: Healthy' : 'Backend: Unavailable'}
    </div>
  )
}
