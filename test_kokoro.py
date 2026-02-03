import sys
print("Starting test_kokoro.py...", flush=True)
import os
import mlx.core as mx
import soundfile as sf
from mlx_audio.tts import load

def main():
    print("Loading Kokoro model...")
    # Trying the repo ID found in the source code default
    repo_id = "prince-canuma/Kokoro-82M" 
    
    try:
        model = load(repo_id)
        print(f"Model loaded: {type(model)}")
        
        text = "Hello! This is a test of the elite audio system."
        print(f"Generating audio for: '{text}'")
        
        # generate returns a generator
        generator = model.generate(text, voice="af_heart", speed=1.0)
        
        all_audio = []
        sample_rate = 24000
        
        for i, result in enumerate(generator):
            print(f"Segment {i}: {result.audio_duration} ({result.samples} samples)")
            # result.audio is mx.array
            # Convert to numpy/list
            audio_np = list(result.audio) # simple list conversion for concat?
            # Better use numpy if available or just collect mx arrays
            all_audio.append(result.audio)
            sample_rate = result.sample_rate
            
        if all_audio:
            # Concatenate
            full_audio = mx.concatenate(all_audio, axis=0)
            print(f"Total audio shape: {full_audio.shape}")
            
            # Save to file
            output_path = "/tmp/kokoro_test.wav"
            # soundfile expects numpy
            import numpy as np
            full_audio_np = np.array(full_audio)
            
            sf.write(output_path, full_audio_np, sample_rate)
            print(f"Saved to {output_path}")
            
            # Play it on Mac
            os.system(f"afplay {output_path}")
        else:
            print("No audio generated.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
