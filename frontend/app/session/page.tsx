'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Mic, MicOff, Square, Loader2 } from 'lucide-react'
import { startSession, endSession, getSessionStatus } from '@/lib/api'
import DailyIframe from '@daily-co/daily-js'

export default function SessionPage() {
  const router = useRouter()
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [roomUrl, setRoomUrl] = useState<string | null>(null)
  const [status, setStatus] = useState<'idle' | 'connecting' | 'active' | 'ended'>('idle')
  const [transcript, setTranscript] = useState<string>('')
  const [currentQuestion, setCurrentQuestion] = useState<string>('')
  const [questionsAsked, setQuestionsAsked] = useState(0)
  const [isMuted, setIsMuted] = useState(false)
  const [isInitialized, setIsInitialized] = useState(false)
  const callFrameRef = useRef<any>(null)
  const pollingIntervalRef = useRef<any>(null)

  useEffect(() => {
    // Prevent double initialization (React Strict Mode calls effects twice)
    if (isInitialized) return
    
    // Start session on mount
    setIsInitialized(true)
    handleStartSession()
    
    return () => {
      // Cleanup on unmount
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current)
      }
      if (callFrameRef.current) {
        callFrameRef.current.destroy()
        callFrameRef.current = null
      }
    }
  }, [])

  const handleStartSession = async () => {
    try {
      setStatus('connecting')
      const data = await startSession('demo_user')
      
      setSessionId(data.session_id)
      setRoomUrl(data.daily_room_url)
      
      // Initialize Daily call
      if (data.daily_room_url) {
        initializeDaily(data.daily_room_url, data.daily_token)
      }
      
      setStatus('active')
      
      // Start polling for session status
      pollingIntervalRef.current = setInterval(async () => {
        if (data.session_id) {
          const statusData = await getSessionStatus(data.session_id)
          updateSessionStatus(statusData)
        }
      }, 2000)
    } catch (error) {
      console.error('Failed to start session:', error)
      setStatus('idle')
      alert('Failed to start session. Please make sure the backend is running.')
    }
  }

  const initializeDaily = (url: string, token?: string) => {
    // Destroy any existing instance first
    if (callFrameRef.current) {
      try {
        callFrameRef.current.destroy()
        callFrameRef.current = null
      } catch (e) {
        console.log('Error destroying previous Daily instance:', e)
      }
    }
    
    const callFrame = DailyIframe.createFrame({
      iframeStyle: {
        position: 'fixed',
        width: '100%',
        height: '100%',
        top: 0,
        left: 0,
        zIndex: 9999,
      },
      showLeaveButton: true,
    })
    
    callFrameRef.current = callFrame
    
    callFrame.join({ 
      url,
      token,
    })
    
    callFrame.on('left-meeting', handleEndSession)
  }

  const updateSessionStatus = (statusData: any) => {
    if (statusData.current_question) {
      setCurrentQuestion(statusData.current_question)
    }
    if (statusData.transcript) {
      setTranscript(statusData.transcript)
    }
    if (statusData.questions_asked !== undefined) {
      setQuestionsAsked(statusData.questions_asked)
    }
  }

  const handleEndSession = async () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
    }
    
    if (callFrameRef.current) {
      callFrameRef.current.destroy()
      callFrameRef.current = null
    }
    
    if (sessionId) {
      try {
        await endSession(sessionId)
      } catch (error) {
        console.error('Failed to end session:', error)
      }
    }
    
    setStatus('ended')
    router.push('/dashboard')
  }

  const toggleMute = () => {
    if (callFrameRef.current) {
      callFrameRef.current.setLocalAudio(!isMuted)
      setIsMuted(!isMuted)
    }
  }

  if (status === 'idle' || status === 'connecting') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 to-purple-50">
        <div className="text-center">
          <Loader2 className="w-16 h-16 animate-spin text-indigo-600 mx-auto mb-4" />
          <p className="text-xl font-semibold text-gray-700">
            {status === 'idle' ? 'Preparing interview...' : 'Connecting to voice session...'}
          </p>
          <p className="text-gray-500 mt-2">This may take a few seconds</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Forge Session</h1>
              <p className="text-gray-500">Questions asked: {questionsAsked}</p>
            </div>
            <button
              onClick={handleEndSession}
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
            >
              <Square className="w-5 h-5" />
              End Session
            </button>
          </div>
        </div>

        {/* Current Question */}
        {currentQuestion && (
          <div className="bg-indigo-50 border-2 border-indigo-200 rounded-2xl p-8 mb-6">
            <p className="text-sm text-indigo-600 font-semibold mb-2">CURRENT QUESTION</p>
            <p className="text-xl text-gray-800">{currentQuestion}</p>
          </div>
        )}

        {/* Transcript */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Live Transcript</h2>
            <button
              onClick={toggleMute}
              className={`p-3 rounded-full transition-colors ${
                isMuted 
                  ? 'bg-red-100 text-red-600 hover:bg-red-200' 
                  : 'bg-indigo-100 text-indigo-600 hover:bg-indigo-200'
              }`}
            >
              {isMuted ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 min-h-[200px] max-h-[400px] overflow-y-auto">
            {transcript ? (
              <p className="text-gray-700 whitespace-pre-wrap">{transcript}</p>
            ) : (
              <p className="text-gray-400 italic">
                Speak your answer... The bot is listening.
              </p>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
          <p className="text-sm text-yellow-800">
            <strong>Tip:</strong> Speak clearly and naturally. The AI will evaluate your answer and ask follow-up questions based on your weak areas.
          </p>
        </div>
      </div>
    </div>
  )
}
