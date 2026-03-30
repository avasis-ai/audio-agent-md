"""CLI for Audio Agent MD."""

import click
import sys
import os
from pathlib import Path

from .parser import AudioMarkdownParser
from .audio_bindings import EmotionalResonanceMapper, EmotionalTone, PacingController


@click.group()
@click.version_option(version="0.1.0", prog_name="audio-agent")
def main():
    """Audio Agent MD - Procedural, executable skills for real-time voice agents."""
    pass


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', default=None,
              help='Output file for parsed skill')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml']),
              default='json',
              help='Output format')
def parse(input_path: str, output: str, format: str) -> None:
    """Parse an audio agent markdown skill."""
    try:
        parser = AudioMarkdownParser()
        
        click.echo(f"📥 Parsing: {input_path}")
        
        # Parse file
        skill = parser.parse_file(input_path)
        
        # Parse errors
        errors = parser.get_parse_errors()
        if errors:
            click.echo("⚠️  Parse warnings:")
            for error in errors:
                click.echo(f"   - {error}")
        
        # Output skill
        skill_data = skill.to_dict()
        
        if format == 'yaml':
            import yaml
            output_str = yaml.dump(skill_data, default_flow_style=False)
        else:
            import json
            output_str = json.dumps(skill_data, indent=2)
        
        if output:
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w') as f:
                f.write(output_str)
            click.echo(f"✅ Saved to: {output}")
        else:
            click.echo(output_str)
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
def list_emotions() -> None:
    """List available emotional tones."""
    click.echo("\n🎭 Available Emotional Tones:")
    click.echo("=" * 60)
    
    for emotion in EmotionalTone:
        click.echo(f"  - {emotion.value}")
    
    click.echo("\n" + "=" * 60)


@main.command()
@click.argument('text', nargs=-1)
@click.option('--emotion', '-e', type=click.Choice([e.value for e in EmotionalTone]),
              required=True)
@click.option('--intensity', '-i', default=1.0,
              help='Emotion intensity (0.0-1.0)')
def apply(text: tuple, emotion: str, intensity: float) -> None:
    """Apply emotional transformation to text."""
    try:
        text_str = ' '.join(text)
        
        # Apply emotion
        modified_text, modifier = EmotionalResonanceMapper.apply_emotion(
            text_str,
            EmotionalTone(emotion),
            intensity
        )
        
        click.echo(f"\nOriginal: {text_str}")
        click.echo(f"Modified: {modified_text}")
        click.echo(f"Emotion:  {emotion} (intensity: {intensity:.1f})")
        click.echo(f"Modifier: {modifier:.2f}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def samples() -> None:
    """Display sample audio skills."""
    
    samples = {
        "radio_host": """
# Late Night Radio Host

## Voice Profile
- Speaker: Alex Night
- Pitch: 1.1 (slightly deeper)
- Speed: 0.9 (measured pace)
- Emotional Range: CALM (0.8), EXCITED (0.6), SERIOUS (0.7)
- Interruption Threshold: 0.3

## Catchphrases
- "Welcome back to the show"
- "Let's dive into"
- "Here's the thing"

## Pacing
- Base pause: 0.8 seconds
- Emphasize: key points
""".strip(),
        "teacher": """
# Strict Teacher

## Voice Profile
- Speaker: Mrs. Thompson
- Pitch: 1.2 (slightly higher)
- Speed: 1.1 (faster when correcting)
- Emotional Range: SERIOUS (0.9), URGENCY (0.5), CALM (0.3)
- Interruption Threshold: 0.1

## Catchphrases
- "Please focus"
- "Pay attention"
- "This is important"

## Pacing
- Base pause: 0.3 seconds
- Emphasize: instructions
""".strip()
    }
    
    click.echo("\n📚 Sample Audio Skills:")
    click.echo("=" * 60)
    
    for name, sample in samples.items():
        click.echo(f"\n### {name}")
        click.echo(sample)
        click.echo()
    
    click.echo("=" * 60)


if __name__ == '__main__':
    main()
