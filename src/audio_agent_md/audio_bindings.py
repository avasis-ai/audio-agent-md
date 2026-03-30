"""Audio bindings and emotional resonance system for voice agents."""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class EmotionalTone(Enum):
    """Available emotional tones for voice agents."""
    CALM = "calm"
    EXCITED = "excited"
    SERIOUS = "serious"
    EMPATHETIC = "empathetic"
    AUTHORITATIVE = "authoritative"
    PLAYFUL = "playful"
    EMPATHETIC_SAD = "empathetic_sad"
    URGENCY = "urgency"
    WHISPER = "whisper"
    NEUTRAL = "neutral"


@dataclass
class VoiceProfile:
    """Defines voice characteristics for an agent."""
    speaker_id: str
    name: str
    base_pitch: float  # 0.5 to 2.0, 1.0 is normal
    base_speed: float  # 0.5 to 2.0, 1.0 is normal
    emotional_range: Dict[str, float]  # emotion: intensity 0.0-1.0
    pause_pattern: List[float]  # pauses in seconds
    interruption_threshold: float  # 0.0-1.0, lower = easier to interrupt
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "speaker_id": self.speaker_id,
            "name": self.name,
            "base_pitch": self.base_pitch,
            "base_speed": self.base_speed,
            "emotional_range": self.emotional_range,
            "pause_pattern": self.pause_pattern,
            "interruption_threshold": self.interruption_threshold
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceProfile':
        """Create from dictionary."""
        return cls(
            speaker_id=data["speaker_id"],
            name=data["name"],
            base_pitch=float(data.get("base_pitch", 1.0)),
            base_speed=float(data.get("base_speed", 1.0)),
            emotional_range=data.get("emotional_range", {}),
            pause_pattern=data.get("pause_pattern", [0.5, 1.0]),
            interruption_threshold=float(data.get("interruption_threshold", 0.5))
        )


@dataclass
class AudioEffect:
    """Defines audio processing effects."""
    effect_type: str
    parameters: Dict[str, float]
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "effect_type": self.effect_type,
            "parameters": self.parameters,
            "enabled": self.enabled
        }


@dataclass
class VocalSignature:
    """Defines vocal patterns for voice agents."""
    signature_id: str
    name: str
    emotional_shifts: List[Dict[str, Any]]
    pacing_patterns: List[str]
    catchphrases: List[str]
    pause_defaults: float = 0.5
    filler_words: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "signature_id": self.signature_id,
            "name": self.name,
            "emotional_shifts": self.emotional_shifts,
            "pacing_patterns": self.pacing_patterns,
            "catchphrases": self.catchphrases,
            "pause_defaults": self.pause_defaults,
            "filler_words": self.filler_words
        }


class EmotionalResonanceMapper:
    """Maps semantic tokens to audio waveform modifiers."""
    
    # Emotional tone mappings for waveform modulation
    TONE_MAPPINGS = {
        EmotionalTone.CALM: {
            "pitch_modulation": -0.1,
            "speed_modulation": -0.1,
            "volume_modulation": -0.1,
            "frequency_modulation": 0.0
        },
        EmotionalTone.EXCITED: {
            "pitch_modulation": 0.3,
            "speed_modulation": 0.2,
            "volume_modulation": 0.2,
            "frequency_modulation": 0.1
        },
        EmotionalTone.SERIOUS: {
            "pitch_modulation": -0.2,
            "speed_modulation": 0.0,
            "volume_modulation": -0.1,
            "frequency_modulation": 0.0
        },
        EmotionalTone.URGENCY: {
            "pitch_modulation": 0.2,
            "speed_modulation": 0.3,
            "volume_modulation": 0.3,
            "frequency_modulation": 0.2
        },
        EmotionalTone.WHISPER: {
            "pitch_modulation": 0.0,
            "speed_modulation": 0.0,
            "volume_modulation": -0.6,
            "frequency_modulation": 0.0
        }
    }
    
    @staticmethod
    def apply_emotion(
        text: str,
        emotion: EmotionalTone,
        intensity: float = 1.0
    ) -> Tuple[np.ndarray, float]:
        """
        Apply emotional modification to text for TTS generation.
        
        Args:
            text: Text to process
            emotion: Emotional tone to apply
            intensity: Intensity of emotion (0.0-1.0)
            
        Returns:
            Tuple of (modified_text, emotional_modifier)
        """
        if emotion not in EmotionalResonanceMapper.TONE_MAPPINGS:
            return text, 1.0
        
        mapping = EmotionalResonanceMapper.TONE_MAPPINGS[emotion]
        modifier = 1.0 + (intensity * 0.1) if emotion == EmotionalTone.EXCITED else 1.0 - (intensity * 0.1)
        
        # Apply text transformations based on emotion
        modified_text = text
        
        if emotion == EmotionalTone.EXCITED:
            modified_text = text.upper()
            # Add exclamation marks for excitement
            modified_text = modified_text.replace("!", "")
            modified_text = modified_text + "!" * min(len(text) // 5 + 1, 3)
        
        elif emotion == EmotionalTone.CALM:
            modified_text = text.lower()
            # Add more pauses
            modified_text = modified_text.replace(". ", ". ")
            modified_text = modified_text.replace(" ", "  ")
        
        elif emotion == EmotionalTone.URGENCY:
            modified_text = text.strip()
            # Remove filler words for urgency
            for filler in ["um", "uh", "like", "you know"]:
                modified_text = modified_text.replace(f" {filler} ", " ")
        
        # Calculate emotional modifier
        emotional_modifier = sum(
            v * intensity for v in mapping.values()
        ) / len(mapping.values())
        
        return modified_text, emotional_modifier
    
    @staticmethod
    def generate_emotional_shift(
        start_emotion: EmotionalTone,
        end_emotion: EmotionalTone,
        duration: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate an emotional shift pattern.
        
        Args:
            start_emotion: Starting emotional tone
            end_emotion: Ending emotional tone
            duration: Duration of shift in seconds
            
        Returns:
            Emotional shift configuration
        """
        start_mapping = EmotionalResonanceMapper.TONE_MAPPINGS.get(start_emotion, {})
        end_mapping = EmotionalResonanceMapper.TONE_MAPPINGS.get(end_emotion, {})
        
        shift = []
        steps = int(duration * 10)  # 10 steps per second
        
        for i in range(steps + 1):
            progress = i / steps
            interpolated = {
                key: start_mapping.get(key, 0) + (end_mapping.get(key, 0) - start_mapping.get(key, 0)) * progress
                for key in start_mapping.keys() & end_mapping.keys()
            }
            
            shift.append({
                "progress": progress,
                "modifications": interpolated
            })
        
        return {
            "type": "emotional_shift",
            "start_emotion": start_emotion.value,
            "end_emotion": end_emotion.value,
            "duration": duration,
            "steps": shift
        }


class PacingController:
    """Controls speech pacing and timing."""
    
    def __init__(self, profile: VoiceProfile):
        """
        Initialize pacing controller.
        
        Args:
            profile: Voice profile to use
        """
        self.profile = profile
        self._current_speed = profile.base_speed
        self._current_pause = 0.5
    
    def calculate_pause(
        self,
        context: str,
        emotion: Optional[EmotionalTone] = None
    ) -> float:
        """
        Calculate pause duration based on context.
        
        Args:
            context: Context of the speech
            emotion: Current emotional tone
            
        Returns:
            Pause duration in seconds
        """
        base_pause = self._get_base_pause(emotion)
        
        # Adjust for sentence structure
        if context.endswith((".", "!", "?")):
            base_pause *= 1.5
        elif context.endswith(","):
            base_pause *= 0.8
        
        # Adjust for emotion
        if emotion == EmotionalTone.URGENCY:
            base_pause *= 0.5
        elif emotion == EmotionalTone.CALM:
            base_pause *= 1.3
        
        # Random variation
        import random
        variation = random.uniform(0.8, 1.2)
        
        return base_pause * variation
    
    def _get_base_pause(self, emotion: Optional[EmotionalTone]) -> float:
        """Get base pause duration for emotion."""
        if emotion in [EmotionalTone.URGENCY, EmotionalTone.EXCITED]:
            return 0.3
        elif emotion in [EmotionalTone.CALM, EmotionalTone.EMPATHETIC]:
            return 0.8
        else:
            return 0.5
    
    def get_pacing_modifier(self, speed: float, pause: float) -> Tuple[float, float]:
        """
        Get pacing modifiers for TTS engine.
        
        Args:
            speed: Speech speed
            pause: Pause duration
            
        Returns:
            Tuple of (speed_modifier, pause_modifier)
        """
        speed_modifier = speed / self.profile.base_speed
        pause_modifier = pause / self.profile.pause_pattern[0] if self.profile.pause_pattern else 1.0
        
        return speed_modifier, pause_modifier


class InterruptionHandler:
    """Handles interruptions during voice generation."""
    
    def __init__(self, threshold: float = 0.5):
        """
        Initialize interruption handler.
        
        Args:
            threshold: Interruption threshold (0.0-1.0)
        """
        self.threshold = threshold
        self._interruption_history: List[Dict[str, Any]] = []
    
    def should_interrupt(
        self,
        current_energy: float,
        urgency: float,
        context: str
    ) -> bool:
        """
        Determine if an interruption should occur.
        
        Args:
            current_energy: Current speaker energy level
            urgency: Urgency of interruption
            context: Context of the interruption
            
        Returns:
            True if interruption should occur
        """
        # Calculate interruptibility based on threshold
        interruptibility = 1.0 - self.threshold
        
        # Factor in urgency
        urgency_factor = urgency * 0.5
        
        # Factor in context
        context_factor = 0.0
        if any(word in context.lower() for word in ["urgent", "important", "stop"]):
            context_factor = 0.3
        
        # Factor in energy
        energy_factor = (1.0 - current_energy) * 0.2
        
        # Calculate total interruptibility
        total_interruptibility = (
            interruptibility + urgency_factor + context_factor + energy_factor
        )
        
        # Store history
        self._interruption_history.append({
            "timestamp": datetime.now().isoformat(),
            "interrupted": total_interruptibility > self.threshold,
            "urgency": urgency
        })
        
        return total_interruptibility > self.threshold
    
    def get_interruptibility_score(self) -> float:
        """Get current interruptibility score."""
        return self.threshold
    
    def adjust_threshold(self, new_threshold: float) -> None:
        """Adjust interruption threshold."""
        self.threshold = max(0.0, min(1.0, new_threshold))
