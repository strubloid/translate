import subprocess
import os

def compress_video(input_path, output_path, target_size_mb=64):
    target_size_bytes = target_size_mb * 1024 * 1024

    # Initial bitrate guess in kilobits per second
    bitrate_kbps = 1000

    # Try decreasing bitrate until we hit the target size
    while True:
        temp_output = output_path.replace('.mp4', f'_{bitrate_kbps}kbps.mp4')
        command = [
            'ffmpeg',
            '-i', input_path,
            '-b:v', f'{bitrate_kbps}k',
            '-bufsize', f'{bitrate_kbps}k',
            '-preset', 'medium',
            '-y',  # Overwrite output
            temp_output
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(temp_output):
            output_size = os.path.getsize(temp_output)
            print(f'Bitrate: {bitrate_kbps} kbps -> Output size: {output_size / (1024 * 1024):.2f} MB')

            if output_size <= target_size_bytes:
                os.rename(temp_output, output_path)
                print(f'✔ Final video saved as {output_path}')
                break
            else:
                os.remove(temp_output)

        bitrate_kbps -= 100
        if bitrate_kbps < 100:
            raise Exception("Couldn't compress video below target size without extreme quality loss.")

# Example usage
compress_video("input.mp4", "output_compressed.mp4", target_size_mb=64)
