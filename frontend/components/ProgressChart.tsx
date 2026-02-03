'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface ProgressChartProps {
  history: Array<{
    session: number
    [key: string]: number
  }>
}

export default function ProgressChart({ history }: ProgressChartProps) {
  // Get all topic names from the history
  const allTopics = new Set<string>()
  history.forEach(entry => {
    Object.keys(entry).forEach(key => {
      if (key !== 'session' && key !== 'average') {
        allTopics.add(key)
      }
    })
  })

  const topics = Array.from(allTopics)
  
  // Colors for different topics
  const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6']

  // Transform data for recharts (scale 0-1 to 0-10)
  const chartData = history.map(entry => {
    const transformed: any = {
      session: `Session ${entry.session}`,
    }
    topics.forEach(topic => {
      if (entry[topic] !== undefined) {
        transformed[topic] = (entry[topic] * 10).toFixed(1)
      }
    })
    return transformed
  })

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="session" tick={{ fill: '#6b7280', fontSize: 12 }} />
        <YAxis domain={[0, 10]} tick={{ fill: '#6b7280' }} label={{ value: 'Score (0-10)', angle: -90, position: 'insideLeft' }} />
        <Tooltip 
          contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
        />
        <Legend />
        {topics.map((topic, idx) => (
          <Line
            key={topic}
            type="monotone"
            dataKey={topic}
            stroke={colors[idx % colors.length]}
            strokeWidth={2}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name={topic.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}
