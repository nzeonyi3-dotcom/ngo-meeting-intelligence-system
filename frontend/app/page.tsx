'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import HealthStatusBadge from '@/components/HealthStatusBadge'

interface AppInfo {
  name: string
  version: string
}

export default function Home() {
  const [appInfo, setAppInfo] = useState<AppInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAppInfo = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/api/v1/info`, {
          timeout: 5000,
        })
        setAppInfo({
          name: response.data.name,
          version: response.data.version,
        })
      } catch (err) {
        setError('Failed to fetch application information')
      } finally {
        setLoading(false)
      }
    }

    fetchAppInfo()
  }, [])

  return (
    <main className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md mx-4">
        <div className="bg-white rounded-lg shadow-xl p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              {appInfo?.name || 'NGO Meeting Intelligence System'}
            </h1>
            <p className="text-gray-600 text-sm">
              Version {appInfo?.version || '1.0.0'}
            </p>
          </div>

          {/* Status Section */}
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <h2 className="text-sm font-semibold text-gray-700 mb-4">System Status</h2>

            <div className="flex items-center justify-center">
              <HealthStatusBadge />
            </div>
          </div>

          {/* Information Section */}
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
              <p className="text-gray-600 mt-4">Loading system information...</p>
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
              <p className="text-red-700 text-sm">{error}</p>
              <p className="text-red-600 text-xs mt-2">Backend API may be unavailable</p>
            </div>
          ) : (
            <div className="bg-indigo-50 rounded-lg p-6 text-center">
              <p className="text-gray-700 text-sm mb-2">Application is running successfully</p>
              <p className="text-indigo-600 font-semibold">Ready to serve</p>
            </div>
          )}

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex justify-center space-x-4 text-sm">
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="text-indigo-600 hover:text-indigo-700 font-medium"
              >
                API Docs
              </a>
              <span className="text-gray-300">•</span>
              <a
                href="http://localhost:8000/redoc"
                target="_blank"
                rel="noopener noreferrer"
                className="text-indigo-600 hover:text-indigo-700 font-medium"
              >
                ReDoc
              </a>
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-8 text-center text-sm text-gray-600">
          <p>A production-ready NGO meeting intelligence system</p>
        </div>
      </div>
    </main>
  )
}
