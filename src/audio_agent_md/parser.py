"""Parser for audio agent markdown skills."""

import re
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from .audio_bindings import (
    VoiceProfile,
    VocalSignature,
    EmotionalTone,
    AudioEffect,
    EmotionalResonanceMapper
)


@dataclass
class AudioSkill:
    """Represents an audio agent skill."""
    skill_id: str
    name: str
    version: str
    description: str
    voice_profile: VoiceProfile
    vocal_signature: Optional[VocalSignature] = None
    emotional_shifts: List[Dict[str, Any]] = field(default_factory=list)
    pacing_config: Dict[str, Any] = field(default_factory=dict)
    effects: List[AudioEffect] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "voice_profile": self.voice_profile.to_dict(),
            "vocal_signature": self.vocal_signature.to_dict() if self.vocal_signature else None,
            "emotional_shifts": self.emotional_shifts,
            "pacing_config": self.pacing_config,
            "effects": [e.to_dict() for e in self.effects],
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AudioSkill':
        """Create from dictionary."""
        return cls(
            skill_id=data["skill_id"],
            name=data["name"],
            version=data["version"],
            description=data["description"],
            voice_profile=VoiceProfile.from_dict(data["voice_profile"]),
            vocal_signature=VocalSignature.from_dict(data["vocal_signature"]) if data.get("vocal_signature") else None,
            emotional_shifts=data.get("emotional_shifts", []),
            pacing_config=data.get("pacing_config", {}),
            effects=[AudioEffect.from_dict(e) for e in data.get("effects", [])],
            created_at=data.get("created_at", datetime.now().isoformat())
        )


class AudioMarkdownParser:
    """Parses audio agent markdown specifications."""
    
    # Pattern for YAML frontmatter
    FRONTMATTER_PATTERN = r'---\s*\n(.*?)\n---'
    
    # Patterns for audio-specific syntax
    EMOTION_PATTERN = re.compile(r'\[EMOTION:?\s*(\w+)\s*:\s*([\d.]+)\]')
    PACE_PATTERN = re.compile(r'\[PACE:\s*([\w-]+)\]')
    PAUSE_PATTERN = re.compile(r'\[PAUSE:\s*([\d.]+)\s*seconds?\]')
    EFFECT_PATTERN = re.compile(r'\[EFFECT:\s*(\w+)\s*:\s*([^]]+)\]')
    
    def __init__(self):
        """Initialize parser."""
        self._parse_errors: List[str] = []
    
    def parse(self, content: str) -> AudioSkill:
        """
        Parse audio agent markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            Parsed AudioSkill
        """
        self._parse_errors = []
        
        # Extract YAML frontmatter
        try:
            frontmatter = self._extract_frontmatter(content)
        except ValueError as e:
            self._parse_errors.append(str(e))
            raise
        
        # Extract body content
        body = self._extract_body(content)
        
        # Parse voice profile
        voice_profile = self._parse_voice_profile(frontmatter)
        
        # Parse vocal signature
        vocal_signature = self._parse_vocal_signature(frontmatter, body)
        
        # Parse emotional shifts
        emotional_shifts = self._parse_emotional_shifts(body)
        
        # Parse pacing configuration
        pacing_config = self._parse_pacing_config(frontmatter, body)
        
        # Parse effects
        effects = self._parse_effects(body)
        
        return AudioSkill(
            skill_id=frontmatter.get("skill_id", "audio_skill"),
            name=frontmatter.get("name", "Unnamed Audio Skill"),
            version=frontmatter.get("version", "0.1.0"),
            description=frontmatter.get("description", ""),
            voice_profile=voice_profile,
            vocal_signature=vocal_signature,
            emotional_shifts=emotional_shifts,
            pacing_config=pacing_config,
            effects=effects,
            created_at=datetime.now().isoformat()
        )
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter."""
        match = re.search(self.FRONTMATTER_PATTERN, content, re.DOTALL)
        
        if not match:
            raise ValueError("Missing YAML frontmatter")
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter: {str(e)}")
    
    def _extract_body(self, content: str) -> str:
        """Extract body content after frontmatter."""
        match = re.search(self.FRONTMATTER_PATTERN, content, re.DOTALL)
        
        if not match:
            return ""
        
        return content[match.end():].strip()
    
    def _parse_voice_profile(self, frontmatter: Dict[str, Any]) -> VoiceProfile:
        """Parse voice profile from frontmatter."""
        profile_data = frontmatter.get("voice", {})
        
        return VoiceProfile(
            speaker_id=profile_data.get("speaker_id", "default"),
            name=profile_data.get("name", "Default Voice"),
            base_pitch=float(profile_data.get("pitch", 1.0)),
            base_speed=float(profile_data.get("speed", 1.0)),
            emotional_range=profile_data.get("emotional_range", {}),
            pause_pattern=profile_data.get("pause_pattern", [0.5, 1.0]),
            interruption_threshold=float(profile_data.get("interruption_threshold", 0.5))
        )
    
    def _parse_vocal_signature(
        self,
        frontmatter: Dict[str, Any],
        body: str
    ) -> Optional[VocalSignature]:
        """Parse vocal signature."""
        signature_data = frontmatter.get("signature", {})
        
        if not signature_data:
            return None
        
        return VocalSignature(
            signature_id=signature_data.get("signature_id", "sig_001"),
            name=signature_data.get("name", "Default Signature"),
            emotional_shifts=signature_data.get("emotional_shifts", []),
            pacing_patterns=signature_data.get("pacing_patterns", []),
            catchphrases=signature_data.get("catchphrases", []),
            pause_defaults=float(signature_data.get("pause_defaults", 0.5)),
            filler_words=signature_data.get("filler_words", [])
        )
    
    def _parse_emotional_shifts(self, body: str) -> List[Dict[str, Any]]:
        """Parse emotional shifts from body."""
        shifts = []
        lines = body.split('\n')
        
        for i, line in enumerate(lines):
            # Find EMOTION markers
            matches = list(self.EMOTION_PATTERN.finditer(line))
            
            for match in matches:
                emotion_str = match.group(1)
                try:
                    emotion = EmotionalTone(emotion_str.lower())
                except ValueError:
                    self._parse_errors.append(f"Unknown emotion: {emotion_str}")
                    continue
                
                intensity = float(match.group(2))
                
                shifts.append({
                    "line": i,
                    "emotion": emotion.value,
                    "intensity": intensity,
                    "position": match.start()
                })
        
        return shifts
    
    def _parse_pacing_config(
        self,
        frontmatter: Dict[str, Any],
        body: str
    ) -> Dict[str, Any]:
        """Parse pacing configuration."""
        config = {
            "base_speed": 1.0,
            "base_pause": 0.5
        }
        
        # Parse PACE markers
        pace_patterns = list(self.PACE_PATTERN.finditer(body))
        
        for match in pace_patterns:
            pace_type = match.group(1)
            config["pace_types"] = config.get("pace_types", {})
            config["pace_types"][pace_type] = match.start()
        
        # Parse PAUSE markers
        pause_patterns = list(self.PAUSE_PATTERN.finditer(body))
        
        for match in pause_patterns:
            pause_duration = float(match.group(1))
            config["pauses"] = config.get("pauses", [])
            config["pauses"].append({
                "position": match.start(),
                "duration": pause_duration
            })
        
        # Merge with frontmatter config
        if "pacing" in frontmatter:
            config.update(frontmatter["pacing"])
        
        return config
    
    def _parse_effects(self, body: str) -> List[AudioEffect]:
        """Parse audio effects."""
        effects = []
        
        # Find all EFFECT markers
        matches = list(self.EFFECT_PATTERN.finditer(body))
        
        for match in matches:
            effect_type = match.group(1)
            params_str = match.group(2)
            
            # Parse parameters
            try:
                params = yaml.safe_load(f"{{{params_str}}}")
            except yaml.YAMLError:
                # Fallback to comma-separated
                params = {}
                for pair in params_str.split(","):
                    if ":" in pair:
                        key, value = pair.split(":", 1)
                        params[key.strip()] = float(value.strip())
            
            effects.append(AudioEffect(
                effect_type=effect_type,
                parameters=params,
                enabled=True
            ))
        
        return effects
    
    def parse_file(self, file_path: str) -> AudioSkill:
        """
        Parse an audio agent markdown file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Parsed AudioSkill
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse(content)
            
        except (IOError, OSError) as e:
            raise ValueError(f"Failed to read file: {str(e)}")
    
    def get_parse_errors(self) -> List[str]:
        """Get parsing errors."""
        return self._parse_errors
