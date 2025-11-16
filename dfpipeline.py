import cv2
import numpy as np
import librosa
from scipy.signal import welch
from moviepy.editor import VideoFileClip

class SimpleDeepfakeDetector:
    def __init__(self):
        # Initialize Haar face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def process_video(self, video_path):
        scores = {
            'facial': 0,
            'frequency': 0,
            'audio_visual': 0
        }

        # Load video
        video = VideoFileClip(video_path)
        frames = [frame for frame in video.iter_frames()]
        audio = video.audio

        # Compute scores
        scores['facial'] = self._analyze_face_movement(frames)
        scores['frequency'] = self._analyze_frequency_domain(frames)
        scores['audio_visual'] = self._analyze_audio_visual_sync(frames, audio)

        return self._calculate_final_score(scores)

    def _analyze_face_movement(self, frames):
        """Face movement consistency using Haar Cascades"""
        facial_scores = []

        for frame in frames[::10]:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                areas = [w * h for (_, _, w, h) in faces]

                if np.mean(areas) != 0:
                    score = 1 - (np.std(areas) / np.mean(areas))
                    facial_scores.append(score)

        return np.mean(facial_scores) if facial_scores else 0.5

    def _analyze_frequency_domain(self, frames):
        """Frequency analysis using FFT"""
        freq_scores = []

        for frame in frames[::10]:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            f_transform = np.fft.fft2(gray)
            f_shift = np.fft.fftshift(f_transform)

            spectrum = np.log(np.abs(f_shift) + 1)
            score = 1 - (np.std(spectrum) / np.mean(spectrum))
            freq_scores.append(score)

        return np.mean(freq_scores) if freq_scores else 0.5

    def _analyze_audio_visual_sync(self, frames, audio):
        """Simplified audio-visual sync estimation"""
        if audio is None:
            return 0.5

        try:
            audio_data = audio.to_soundarray()
            audio_energy = np.abs(audio_data.mean(axis=1))

            frame_diffs = [
                np.mean(np.abs(frames[i + 1] - frames[i]))
                for i in range(len(frames) - 1)
            ]

            # Normalize safely
            audio_energy = (audio_energy - audio_energy.min()) / (audio_energy.max() - audio_energy.min() + 1e-6)
            frame_diffs = (frame_diffs - np.min(frame_diffs)) / (np.max(frame_diffs) - np.min(frame_diffs) + 1e-6)

            # Correlation
            correlation = np.corrcoef(
                audio_energy[:len(frame_diffs)],
                frame_diffs
            )[0, 1]

            return float(abs(correlation))

        except Exception:
            return 0.5

    def _calculate_final_score(self, scores):
        """Weighted combination of components"""
        weights = {'facial': 0.4, 'frequency': 0.3, 'audio_visual': 0.3}

        final_score = sum(
            scores[c] * weights[c] for c in scores
        )

        return {
            'final_score': final_score,
            'component_scores': scores,
            'interpretation': {
                'verdict': 'Real' if final_score > 0.7 else 'Likely Deepfake',
                'confidence': abs(final_score - 0.5) * 2,
                'anomalies': [c for c in scores if scores[c] < 0.7]
            }
        }


# Standalone usage
def analyze_video(video_path):
    detector = SimpleDeepfakeDetector()
    results = detector.process_video(video_path)
    return results
