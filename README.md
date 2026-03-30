# README.md - Audio Agent MD

## Procedural, Executable Skills for Real-Time Voice Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/audio-agent-md.svg)](https://pypi.org/project/audio-agent-md/)

**Audio Agent MD** moves SKILL.md beyond text manipulation to define vocal tone, interruption handling, emotional resonance, and pacing for open-source voice models. Copy-paste a Late Night Radio Host or Strict Teacher voice persona instantly.

## 🎯 What It Does

- **Voice Characterization**: Define vocal tones and emotional ranges
- **Emotional Resonance**: Map semantic tokens to audio waveform modifiers
- **Interruption Handling**: Control when voice agents can be interrupted
- **Pacing Control**: Define speech speed and pause patterns
- **Audio Effects**: Apply real-time audio processing effects

### Example Use Case

```python
from audio_agent_md.parser import AudioMarkdownParser
from audio_agent_md.audio_bindings import EmotionalTone

# Parse voice skill
parser = AudioMarkdownParser()
skill = parser.parse("""
---
name: Late Night Host
voice:
  pitch: 1.1
  speed: 0.9
  emotional_range:
    excited: 0.7
    calm: 0.9
---

[EMOTION: calm: 0.8] Welcome to the show.
""")

# Apply emotional transformation
from audio_agent_md.audio_bindings import EmotionalResonanceMapper
modified_text, modifier = EmotionalResonanceMapper.apply_emotion(
    "Hello there!",
    EmotionalTone.EXCITED,
    0.9
)
```

## 🚀 Features

- **Emotional Tone System**: 10 emotional tones with smooth transitions
- **Voice Profiles**: Define pitch, speed, pause patterns, and interruption thresholds
- **Vocal Signatures**: Define catchphrases and emotional shift patterns
- **Real-Time Pacing**: Dynamic pause calculation based on context
- **Audio Effects**: Apply effects like reverb, delay, and modulation
- **Interruption Handling**: Intelligent interruption detection

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- NumPy for audio processing

### Install from PyPI

```bash
pip install audio-agent-md
```

### Install from Source

```bash
git clone https://github.com/avasis-ai/audio-agent-md.git
cd audio-agent-md
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
pip install pytest pytest-mock black isort
```

## 🔧 Usage

### Command-Line Interface

```bash
# Check version
audio-agent --version

# Parse a skill
audio-agent parse skill.md --output skill.json

# List available emotions
audio-agent list-emotions

# Apply emotion to text
audio-agent apply "Hello there!" --emotion excited --intensity 0.9

# View sample skills
audio-agent samples
```

### Programmatic Usage

```python
from audio_agent_md.parser import AudioMarkdownParser
from audio_agent_md.audio_bindings import (
    EmotionalResonanceMapper,
    EmotionalTone,
    PacingController,
    InterruptionHandler,
    VoiceProfile
)

# Create voice profile
profile = VoiceProfile(
    speaker_id="radio_host",
    name="Alex Night",
    pitch=1.1,
    speed=0.9,
    emotional_range={
        EmotionalTone.CALM: 0.8,
        EmotionalTone.EXCITED: 0.6,
        EmotionalTone.SERIOUS: 0.7
    },
    interruption_threshold=0.3
)

# Apply emotional transformation
modified_text, modifier = EmotionalResonanceMapper.apply_emotion(
    "Hello there!",
    EmotionalTone.EXCITED,
    0.9
)

# Control pacing
controller = PacingController(profile)
pause_duration = controller.calculate_pause("Hello.", EmotionalTone.CALM)

# Handle interruptions
handler = InterruptionHandler(threshold=0.5)
should_interrupt = handler.should_interrupt(0.2, 0.9, "urgent interruption")
```

## 📚 API Reference

### EmotionalResonanceMapper

Maps semantic tokens to audio waveform modifiers.

#### `apply_emotion(text, emotion, intensity)` → Tuple[str, float]

Apply emotional modification to text.

#### `generate_emotional_shift(start, end, duration)` → Dict

Generate emotional shift pattern.

### PacingController

Controls speech pacing and timing.

#### `calculate_pause(context, emotion)` → float

Calculate pause duration.

### InterruptionHandler

Handles interruptions during voice generation.

#### `should_interrupt(energy, urgency, context)` → bool

Determine if interruption should occur.

## 🧪 Testing

Run tests with pytest:

```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
audio-agent-md/
├── README.md
├── pyproject.toml
├── LICENSE
├── src/
│   └── audio_agent_md/
│       ├── __init__.py
│       ├── audio_bindings.py
│       ├── parser.py
│       └── cli.py
├── tests/
│   └── test_audio_agent.py
├── parser/
└── audio-bindings/
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest tests/ -v`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/avasis-ai/audio-agent-md.git
cd audio-agent-md
pip install -e ".[dev]"
pre-commit install
```

## 📝 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

## 🎯 Vision

Audio Agent MD democratizes voice AI by providing a simple, declarative way to define voice personas. Whether you want a Late Night Radio Host or a Strict Teacher, you can instantly create and deploy emotional, expressive voice agents.

### Key Innovations

- **Emotional Resonance**: Zero-latency emotional shifts during real-time generation
- **Procedural Pacing**: Intelligent pause calculation for natural speech
- **Interruption Awareness**: Context-aware interruption handling
- **Voice Characterization**: Define unique voice profiles
- **Audio Effects**: Real-time audio processing

## 🌟 Impact

This tool enables:

- **Rapid persona creation**: Create voice agents in minutes
- **Emotional expression**: Natural, expressive voice output
- **Real-time interaction**: Responsive interruption handling
- **Custom voices**: Define unique voice characteristics
- **Audio processing**: Apply effects dynamically

## 🛡️ Security & Trust

- **Trusted dependencies**: NumPy (8.7), PyYAML (7.4), Click (8.8) - [Context7 verified](https://context7.com)
- **MIT License**: Open source, community-driven
- **No external API calls**: All processing local

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/avasis-ai/audio-agent-md/wiki)
- **Issues**: [GitHub Issues](https://github.com/avasis-ai/audio-agent-md/issues)
- **Community**: [Voice AI Discord](https://discord.gg/voice-ai)

## 🙏 Acknowledgments

- **VibeVoice**: Inspiration for voice AI
- **Whisper**: Speech recognition patterns
- **Open-source voice community**: Shared knowledge and best practices
- **Audio engineers**: Real-time processing techniques

---

**Made with ❤️ by [Avasis AI](https://avasis.ai)**

*Voice AI is the undisputed frontier of consumer interaction. Create expressive, emotional voice agents in minutes.*
