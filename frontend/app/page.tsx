'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { Mic, TrendingUp, Brain, Zap } from 'lucide-react'
import { getSessions } from '@/lib/api'

export default function Home() {
  const [sessions, setSessions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    try {
      const data = await getSessions('demo_user')
      setSessions(data.sessions || [])
    } catch (error) {
      console.error('Failed to load sessions:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen p-8 bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Forge
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Forge your interview skills. AI-powered practice that learns your weaknesses and sharpens your strengths.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <FeatureCard
            icon={<Mic className="w-8 h-8" />}
            title="Voice Based"
            description="Natural conversation with AI interviewer using Daily + Pipecat"
          />
          <FeatureCard
            icon={<Brain className="w-8 h-8" />}
            title="Self-Improving"
            description="Learns your weak areas and focuses practice there"
          />
          <FeatureCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="Track Progress"
            description="See your improvement over time with visual dashboards"
          />
          <FeatureCard
            icon={<Zap className="w-8 h-8" />}
            title="Instant Feedback"
            description="Real-time evaluation and personalized insights"
          />
        </div>

        {/* Main Actions */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex flex-col md:flex-row gap-6 items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-2">Ready to practice?</h2>
              <p className="text-gray-600">
                Start a new interview session and get personalized feedback
              </p>
            </div>
            <Link
              href="/session"
              className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:shadow-lg transition-all duration-200 hover:scale-105 flex items-center gap-2"
            >
              <Mic className="w-5 h-5" />
              Start Interview Session
            </Link>
          </div>
        </div>

        {/* Session History */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Your Progress</h2>
            {sessions.length > 0 && (
              <Link
                href="/dashboard"
                className="text-indigo-600 hover:text-indigo-700 font-medium flex items-center gap-1"
              >
                View Dashboard
                <TrendingUp className="w-4 h-4" />
              </Link>
            )}
          </div>

          {loading ? (
            <p className="text-gray-500">Loading sessions...</p>
          ) : sessions.length === 0 ? (
            <div className="text-center py-12">
              <Brain className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p className="text-gray-500 mb-2">No sessions yet</p>
              <p className="text-sm text-gray-400">
                Start your first interview to begin tracking your progress
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {sessions.map((session, idx) => (
                <SessionCard key={session.id || idx} session={session} />
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Built for WeaveHacks 2025 | Powered by Daily, Pipecat, Claude, Redis & Weave</p>
        </div>
      </div>
    </main>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
      <div className="text-indigo-600 mb-3">{icon}</div>
      <h3 className="font-bold mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  )
}

function SessionCard({ session }: { session: any }) {
  const date = new Date(session.date || session.started_at)
  const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition-colors">
      <div className="flex justify-between items-start">
        <div>
          <p className="font-medium">Session {session.id || 'N/A'}</p>
          <p className="text-sm text-gray-500">{dateStr}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">
            {session.questions_asked || session.questions?.length || 0} questions
          </p>
          <p className="text-sm font-medium text-indigo-600">
            Avg Score: {session.average_score?.toFixed(1) || 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}
