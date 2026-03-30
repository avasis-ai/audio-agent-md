# AGENTS.md - Audio Agent MD Project Context

This folder is home. Treat it that way.

## Project: Audio-Agent.md (#42)

### Identity
- **Name**: Audio-Agent-md
- **License**: MIT
- **Org**: avasis-ai
- **PyPI**: audio-agent-md
- **Version**: 0.1.0
- **Tagline**: Procedural, executable skills for real-time voice agents

### What It Does
Moving SKILL.md beyond text manipulation, this format defines vocal tone, interruption handling, emotional resonance, and pacing for open-source voice models. Developers can copy-paste a Late Night Radio Host or Strict Teacher voice persona instantly.

### Inspired By
- VibeVoice
- Whisper
- Multimodal + Voice interfaces

### Core Components

#### `/parser/`
- Audio markdown parsing
- Voice profile extraction
- Emotional shift parsing

#### `/audio-bindings/`
- Voice profile management
- Emotional resonance mapping
- Pacing control
- Interruption handling

### Technical Architecture

**Key Dependencies:**
- `numpy>=1.24` - Numerical computing (Trust score: 8.7)
- `pyyaml>=6.0` - Configuration parsing (Trust score: 7.4)
- `click>=8.0` - CLI framework (Trust score: 8.8)

**Core Modules:**
1. `parser.py` - Audio markdown parser
2. `audio_bindings.py` - Voice bindings and emotional system
3. `cli.py` - Command-line interface

### AI Coding Agent Guidelines

#### When Contributing:

1. **Understand the domain**: Voice AI is the frontier of consumer interaction
2. **Use Context7**: Check trust scores for new libraries before adding dependencies
3. **Emotional resonance**: Map semantic tokens to waveform modifiers efficiently
4. **Real-time performance**: Minimize latency in emotional shifts
5. **Voice quality**: Ensure natural, expressive speech output

#### What to Remember:

- **Zero-latency shifts**: Emotional transitions must be instantaneous
- **Emotional range**: Voice agents should have varied emotional capabilities
- **Interruption awareness**: Know when to yield to user input
- **Pacing control**: Natural pauses make speech more human
- **Voice profiles**: Define unique characteristics for each persona

#### Common Patterns:

**Create voice profile:**
```python
from audio_agent_md.audio_bindings import VoiceProfile, EmotionalTone

profile = VoiceProfile(
    speaker_id="radio_host",
    name="Alex Night",
    pitch=1.1,
    speed=0.9,
    emotional_range={
        EmotionalTone.CALM: 0.8,
        EmotionalTone.EXCITED: 0.6
    },
    interruption_threshold=0.3
)
```

**Apply emotion:**
```python
from audio_agent_md.audio_bindings import EmotionalResonanceMapper, EmotionalTone

modified_text, modifier = EmotionalResonanceMapper.apply_emotion(
    text,
    EmotionalTone.EXCITED,
    intensity=0.9
)
```

**Control pacing:**
```python
from audio_agent_md.audio_bindings import PacingController

controller = PacingController(profile)
pause = controller.calculate_pause("Hello.", EmotionalTone.CALM)
```

### Project Status

- ✅ Initial implementation complete
- ✅ Voice profile system
- ✅ Emotional tone mapping
- ✅ Pacing controller
- ✅ Interruption handler
- ✅ Markdown parser
- ✅ CLI interface
- ✅ Comprehensive test suite
- ⚠️ Real TTS integration pending
- ⚠️ Audio effects rendering pending

### How to Work with This Project

1. **Read `SOUL.md`** - Understand who you are
2. **Read `USER.md`** - Know who you're helping
3. **Check `memory/YYYY-MM-DD.md`** - Recent context
4. **Read `MEMORY.md`** - Long-term decisions (main session only)
5. **Execute**: Code → Test → Commit

### Red Lines

- **No stubs or TODOs**: Every function must have real implementation
- **Type hints required**: All function signatures must include types
- **Docstrings mandatory**: Explain what, why, and how
- **Test coverage**: New features need tests
- **Performance**: Real-time generation must be low-latency

### Development Workflow

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
isort src/ tests/

# Check syntax
python -m py_compile src/audio_agent_md/*.py

# Run CLI
audio-agent --help

# Commit
git add -A && git commit -m "feat: add emotional shift"
```

### Key Files to Understand

- `src/audio_agent_md/audio_bindings.py` - Core voice and emotion system
- `src/audio_agent_md/parser.py` - Audio markdown parser
- `src/audio_agent_md/cli.py` - Command-line interface
- `tests/test_audio_agent.py` - Comprehensive tests

### Security Considerations

- **Local processing**: All audio processing local
- **No external calls**: No API dependencies for core features
- **Trusted dependencies**: All verified via Context7
- **MIT License**: Open source, community-driven

### Next Steps

1. Integrate with real TTS engines
2. Add more emotional tones
3. Build audio effects library
4. Create web-based skill editor
5. Add voice cloning support
6. Implement real-time audio streaming

### Unique Defensible Moat

The **proprietary markup language** maps semantic text tokens directly to latent audio waveform modifiers, enabling zero-latency emotional shifts during real-time generation. This requires:

- Understanding of waveform synthesis
- Real-time processing optimization
- Emotional token mapping
- Latency minimization techniques
- Audio quality maintenance

This is a complex, specialized skill that requires deep understanding of both audio synthesis and semantic mapping.

---

**This file should evolve as you learn more about the project.**
