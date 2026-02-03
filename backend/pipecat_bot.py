"""
Full Pipecat implementation for voice interviews
This is the REAL working version
"""

import os
import asyncio
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.frames.frames import (
    Frame,
    AudioRawFrame,
    TextFrame,
    EndFrame,
    LLMMessagesFrame,
    TTSSpeakFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame
)
from pipecat.services.deepgram.stt import DeepgramSTTService, LiveOptions
from pipecat.services.deepgram.tts import DeepgramTTSService
from pipecat.transports.daily.transport import DailyParams, DailyTransport

from loguru import logger


# Demo limit - set to 3 for quick demos, increase for longer sessions
MAX_QUESTIONS = 3


class InterviewBotProcessor(FrameProcessor):
    """
    Pipecat processor that handles interview logic
    """
    
    def __init__(self, session_id: str, storage, evaluator, **kwargs):
        super().__init__(**kwargs)
        self.session_id = session_id
        self.storage = storage
        self.evaluator = evaluator
        
        # Get session data
        self.session_data = storage.get_session(session_id)
        self.user_id = self.session_data["user_id"]
        
        # Interview state
        self.current_topic = None
        self.last_question = None
        self.questions_asked = 0
        self.waiting_for_answer = False
        self.current_answer = ""
        self.last_text_time = 0
        self._answer_timer = None
        self.session_ended = False
        
        logger.info(f"Interview bot initialized for session {session_id} (max {MAX_QUESTIONS} questions)")
    
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        """Process frames from the pipeline"""
        
        await super().process_frame(frame, direction)
        
        # Handle text from speech-to-text
        if isinstance(frame, TextFrame):
            await self._handle_user_text(frame.text)
        
        # Detect when user starts speaking
        elif isinstance(frame, UserStartedSpeakingFrame):
            self.current_answer = ""
            logger.info("User started speaking")
        
        # Detect when user stops speaking
        elif isinstance(frame, UserStoppedSpeakingFrame):
            logger.info("User stopped speaking")
            # Answer is complete, process it
            if self.current_answer:
                await self._process_answer(self.current_answer)
        
        # Pass frame down the pipeline
        await self.push_frame(frame, direction)
    
    async def _handle_user_text(self, text: str):
        """Handle transcribed text from user"""
        logger.info(f"Received text: {text}")
        
        # Check if it's new text
        is_new_text = (text != self.current_answer)
        
        if is_new_text:
            self.current_answer = text  # Use latest complete transcript
            self.last_text_time = asyncio.get_event_loop().time()
            
            # Cancel existing timer if any
            if hasattr(self, '_answer_timer') and self._answer_timer:
                self._answer_timer.cancel()
            
            # Set timer to process answer after 2 seconds of silence
            self._answer_timer = asyncio.create_task(self._silence_timer())
    
    async def _silence_timer(self):
        """Wait for silence, then process answer"""
        try:
            await asyncio.sleep(2.0)  # Wait 2 seconds
            
            # Check if we're still waiting for answer and have text
            if self.waiting_for_answer and self.current_answer.strip():
                logger.info("Silence detected, processing answer...")
                await self._process_answer(self.current_answer.strip())
                # Note: current_answer and waiting_for_answer are reset in _process_answer
        except asyncio.CancelledError:
            pass  # Timer was cancelled by new text
    
    async def _ask_first_question(self):
        """Ask the first interview question"""
        from question_bank import get_question, get_all_topics
        
        topics = get_all_topics()
        self.current_topic = topics[0]  # Start with first topic
        
        question = get_question(self.current_topic, "easy")
        self.last_question = question
        self.questions_asked = 1
        self.waiting_for_answer = True
        
        # Send to TTS
        intro = f"Hello! I'm your AI interview coach. I'm going to ask you some interview questions to help you improve. Let's start with: {question}"
        await self.push_frame(TTSSpeakFrame(intro))
        
        logger.info(f"Asked first question: {question}")
    
    async def _process_answer(self, answer_text: str):
        """Process user's answer and ask next question"""
        
        if not self.last_question:
            return
        
        logger.info(f"Processing answer for topic: {self.current_topic}")
        
        # Evaluate the answer
        score, weak_points = self.evaluator.evaluate_answer(
            question=self.last_question,
            answer=answer_text,
            topic=self.current_topic
        )
        
        logger.info(f"Score: {score}/10, Weak points: {weak_points}")
        
        # Store the result
        self.storage.add_question(
            session_id=self.session_id,
            question=self.last_question,
            answer=answer_text,
            score=score,
            topic=self.current_topic,
            weak_points=weak_points
        )
        
        self.questions_asked += 1
        
        # Get updated knowledge map
        knowledge_map = self.storage.get_knowledge_map(self.user_id)
        topics_data = knowledge_map.get("topics", {})
        
        # Select next topic
        session = self.storage.get_session(self.session_id)
        previous_topics = [q["topic"] for q in session["questions"]]
        
        if topics_data:
            self.current_topic = self.evaluator.select_next_topic(
                topics_data,
                previous_topics
            )
        else:
            from question_bank import get_all_topics
            topics = get_all_topics()
            self.current_topic = topics[self.questions_asked % len(topics)]
        
        # Determine difficulty
        current_score = topics_data.get(self.current_topic, 0.5)
        if current_score < 0.4:
            difficulty = "easy"
        elif current_score < 0.7:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        # Generate next question
        next_question = self.evaluator.generate_next_question(
            self.current_topic,
            difficulty,
            topics_data
        )
        
        self.last_question = next_question
        
        # Build feedback response
        if score >= 8:
            feedback = "That was a strong answer. "
        elif score >= 6:
            feedback = "Good answer, but there's room for improvement. "
        else:
            feedback = "Let's work on strengthening that. "
        
        # Check if we've hit the question limit
        if self.questions_asked > MAX_QUESTIONS:
            # End session with summary
            await self._end_session_with_summary(feedback, score)
            return
        
        response = f"Thank you. {feedback}Next question: {next_question}"
        
        # Send to TTS
        await self.push_frame(TTSSpeakFrame(response))
        
        logger.info(f"Asked next question: {next_question}")
        
        # Reset for next answer
        self.current_answer = ""
        self.waiting_for_answer = True  # CRITICAL FIX: re-enable answer detection
    
    async def _end_session_with_summary(self, last_feedback: str, last_score: float):
        """End the session with a performance summary"""
        self.session_ended = True
        self.waiting_for_answer = False
        
        # Get final scores
        knowledge_map = self.storage.get_knowledge_map(self.user_id)
        topics_data = knowledge_map.get("topics", {})
        
        # Build summary
        summary_parts = [f"Thank you. {last_feedback}"]
        summary_parts.append(f"That concludes our {MAX_QUESTIONS}-question practice session!")
        summary_parts.append("Here's your performance summary:")
        
        if topics_data:
            for topic, score in sorted(topics_data.items(), key=lambda x: x[1], reverse=True):
                percentage = int(score * 100)
                summary_parts.append(f"{topic.replace('_', ' ').title()}: {percentage}%.")
        
        # Overall advice
        avg_score = sum(topics_data.values()) / len(topics_data) if topics_data else 0.5
        if avg_score >= 0.7:
            summary_parts.append("Great job overall! Keep practicing to stay sharp.")
        elif avg_score >= 0.5:
            summary_parts.append("Good effort! Focus on your weaker areas for improvement.")
        else:
            summary_parts.append("There's room for growth. Consider practicing more with specific examples.")
        
        summary_parts.append("Check your dashboard to see your progress over time. Goodbye!")
        
        summary = " ".join(summary_parts)
        
        # Send summary via TTS
        await self.push_frame(TTSSpeakFrame(summary))
        
        # End the session in storage
        self.storage.end_session(self.session_id)
        
        logger.info(f"Session {self.session_id} ended with summary")


async def run_interview_bot(
    room_url: str,
    room_token: str,
    session_id: str,
    storage,
    evaluator
):
    """
    Run the interview bot with Pipecat
    """
    
    logger.info(f"Starting interview bot for session {session_id}")
    logger.info(f"Room URL: {room_url}")
    
    # Daily transport configuration
    transport = DailyTransport(
        room_url,
        room_token,  # Use the meeting token
        "Forge Interview Bot",
        DailyParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_enabled=True,  # Voice activity detection
            vad_analyzer=None,
            vad_audio_passthrough=True
        )
    )
    
    # Deepgram for speech-to-text - with utterance detection
    from pipecat.services.deepgram.stt import DeepgramSTTService, LiveOptions
    
    stt = DeepgramSTTService(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        live_options=LiveOptions(
            model="nova-2",
            language="en-US",
            interim_results=True,
            utterance_end_ms=1500,  # Integer: 1.5 seconds of silence
            endpointing=300  # Integer: milliseconds of silence to detect end
        )
    )
    
    # Deepgram for text-to-speech (using Deepgram TTS is easier than ElevenLabs)
    tts = DeepgramTTSService(
        api_key=os.getenv("DEEPGRAM_API_KEY"),
        voice="aura-asteria-en"  # Female voice, clear and professional
    )
    
    # Our interview bot processor
    bot = InterviewBotProcessor(
        session_id=session_id,
        storage=storage,
        evaluator=evaluator
    )
    
    # Build pipeline
    pipeline = Pipeline([
        transport.input(),
        stt,
        bot,
        tts,
        transport.output()
    ])
    
    # Create task with just the pipeline
    task = PipelineTask(pipeline)
    
    # Create runner
    runner = PipelineRunner()
    
    # Start the bot
    logger.info("Starting pipeline...")
    
    # Create a task to ask first question after pipeline is ready
    async def ask_after_ready():
        await asyncio.sleep(2)  # Wait for pipeline to be fully ready
        await bot._ask_first_question()
    
    asyncio.create_task(ask_after_ready())
    
    try:
        # Run the pipeline
        await runner.run(task)
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        logger.info("Bot session ended")


def start_bot_async(room_url: str, session_id: str, storage, evaluator):
    """Start bot in a new async context"""
    asyncio.run(run_interview_bot(room_url, session_id, storage, evaluator))
