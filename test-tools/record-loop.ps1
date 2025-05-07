$wslPath = "C:\apps\translate\generated"
# $micName = "Microphone (ME6S)"
$micName = "Microphone (Voicemod Virtual Audio Device (WDM))"


while ($true) {
    $tempFile = "$wslPath/temp.wav"
    $finalFile = "$wslPath/mic.wav"

    # Record 5 seconds to a temporary file
    ffmpeg -y -f dshow -i audio="$micName" -t 6 "$tempFile" | Out-Null

    # Analyze the file for silence using silencedetect
    $silenceOutput = ffmpeg -i "$tempFile" -af silencedetect=n=-28dB:d=0.5 -f null - 2>&1

    # Check if there are any lines indicating non-silence
    if ($silenceOutput -notmatch "silence_start") {
        # If there's no silence_start, assume there was sound and move the file
        Move-Item "$tempFile" "$finalFile" -Force
        Write-Host "Sound detected, saved as mic.wav"
    } else {
        # Otherwise, delete it
        Remove-Item "$tempFile" -Force
        Write-Host "Silence detected, file not saved"
    }

    Start-Sleep -Seconds 2
}
