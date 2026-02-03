'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { TrendingUp, ArrowLeft, Brain } from 'lucide-react'
import { getSessions, getKnowledgeMap } from '@/lib/api'
import RadarChart from '@/components/RadarChart'
import ProgressChart from '@/components/ProgressChart'

export default function DashboardPage() {
  const router = useRouter()
  const [sessions, setSessions] = useState<any[]>([])
  const [knowledgeMap, setKnowledgeMap] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [sessionsData, knowledgeData] = await Promise.all([
        getSessions('demo_user'),
        getKnowledgeMap('demo_user'),
      ])
      
      setSessions(sessionsData.sessions || [])
      setKnowledgeMap(knowledgeData)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-50">
        <div className="text-center">
          <Brain className="w-16 h-16 animate-pulse text-indigo-600 mx-auto mb-4" />
          <p className="text-xl font-semibold text-gray-700">Loading your progress...</p>
        </div>
      </div>
    )
  }

  const topics = knowledgeMap?.topics || {}
  const topicNames = Object.keys(topics)
  const averageScore = topicNames.length > 0
    ? topicNames.reduce((sum, topic) => sum + topics[topic], 0) / topicNames.length
    : 0

  const improvement = knowledgeMap?.history && knowledgeMap.history.length > 1
    ? ((averageScore - knowledgeMap.history[0]?.average) / knowledgeMap.history[0]?.average * 100)
    : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push('/')}
            className="flex items-center gap-2 text-indigo-600 hover:text-indigo-700 mb-4 font-medium"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </button>
          
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Forge Dashboard
          </h1>
          <p className="text-gray-600">Track how you're forging your interview skills</p>
        </div>

        {/* Stats Overview */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Total Sessions"
            value={sessions.length}
            icon={<Brain className="w-6 h-6" />}
            color="blue"
          />
          <StatCard
            title="Average Score"
            value={`${(averageScore * 10).toFixed(1)}/10`}
            icon={<TrendingUp className="w-6 h-6" />}
            color="green"
          />
          <StatCard
            title="Overall Improvement"
            value={`${improvement > 0 ? '+' : ''}${improvement.toFixed(0)}%`}
            icon={<TrendingUp className="w-6 h-6" />}
            color="purple"
          />
        </div>

        {/* Knowledge Map */}
        {topicNames.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-bold mb-6">Knowledge Map</h2>
            <p className="text-gray-600 mb-6">
              Visual representation of your strengths and areas for improvement
            </p>
            <RadarChart data={topics} />
          </div>
        )}

        {/* Progress Over Time */}
        {knowledgeMap?.history && knowledgeMap.history.length > 1 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-bold mb-6">Progress Over Time</h2>
            <ProgressChart history={knowledgeMap.history} />
          </div>
        )}

        {/* Topic Breakdown */}
        {topicNames.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-2xl font-bold mb-6">Topic Breakdown</h2>
            <div className="space-y-4">
              {topicNames.map((topic) => (
                <TopicBar
                  key={topic}
                  topic={topic}
                  score={topics[topic]}
                />
              ))}
            </div>
          </div>
        )}

        {/* Session History */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold mb-6">Session History</h2>
          {sessions.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No sessions yet. Start your first interview!</p>
          ) : (
            <div className="space-y-3">
              {sessions.map((session, idx) => (
                <SessionHistoryCard key={session.id || idx} session={session} />
              ))}
            </div>
          )}
        </div>

        {/* Call to Action */}
        <div className="mt-8 text-center">
          <button
            onClick={() => router.push('/session')}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:shadow-lg transition-all duration-200 hover:scale-105"
          >
            Start New Interview Session
          </button>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color }: any) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-md">
      <div className={`inline-flex p-3 rounded-lg mb-4 ${colorClasses[color]}`}>
        {icon}
      </div>
      <p className="text-gray-500 text-sm mb-1">{title}</p>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
    </div>
  )
}

function TopicBar({ topic, score }: { topic: string; score: number }) {
  const percentage = score * 100
  const formattedTopic = topic.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')

  const getColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500'
    if (score >= 0.6) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <span className="font-medium text-gray-700">{formattedTopic}</span>
        <span className="text-sm font-semibold text-gray-600">{(score * 10).toFixed(1)}/10</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className={`h-3 rounded-full transition-all duration-500 ${getColor(score)}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

function SessionHistoryCard({ session }: { session: any }) {
  const date = new Date(session.date || session.started_at)
  const dateStr = date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition-colors">
      <div className="flex justify-between items-center">
        <div>
          <p className="font-medium text-gray-800">Session {session.id}</p>
          <p className="text-sm text-gray-500">{dateStr}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">
            {session.questions_asked || session.questions?.length || 0} questions
          </p>
          <p className="text-sm font-semibold text-indigo-600">
            {session.average_score ? `${(session.average_score).toFixed(1)}/10` : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}
