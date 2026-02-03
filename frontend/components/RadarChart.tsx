'use client'

import { Radar, RadarChart as RechartsRadar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'

interface RadarChartProps {
  data: Record<string, number>
}

export default function RadarChart({ data }: RadarChartProps) {
  // Transform data for recharts
  const chartData = Object.entries(data).map(([topic, score]) => ({
    topic: topic.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    score: score * 10, // Convert 0-1 to 0-10 scale
  }))

  return (
    <ResponsiveContainer width="100%" height={400}>
      <RechartsRadar data={chartData}>
        <PolarGrid strokeDasharray="3 3" />
        <PolarAngleAxis dataKey="topic" tick={{ fill: '#6b7280', fontSize: 12 }} />
        <PolarRadiusAxis angle={90} domain={[0, 10]} tick={{ fill: '#6b7280' }} />
        <Radar
          name="Skill Level"
          dataKey="score"
          stroke="#6366f1"
          fill="#6366f1"
          fillOpacity={0.6}
        />
      </RechartsRadar>
    </ResponsiveContainer>
  )
}
