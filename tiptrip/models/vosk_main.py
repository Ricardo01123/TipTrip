import ast
import pyaudio
import numpy as np
from logging import Logger
from scipy.signal import butter, lfilter
from vosk import Model, KaldiRecognizer, SetLogLevel

from resources.config import *
from views.chatbot import ChatbotView


SetLogLevel(-1)


def butter_lowpass(cutoff: int, fs: int, order: int = 5):
	nyq: float = 0.5 * fs
	normal_cutoff: float = cutoff / nyq
	numerator, denominator = butter(order, normal_cutoff)
	return numerator, denominator


def lowpass_filter(data, cutoff: int, fs: int, order: int = 5):
	b, a = butter_lowpass(cutoff, fs, order=order)
	y = lfilter(b, a, data)
	return y


def speech_recognition(logger: Logger) -> str | None:
	logger.info("Activating model...")
	model = Model(model_path=MODEL_ABS_PATH)
	recognizer = KaldiRecognizer(model, SAMPLING_RATE)

	logger.info("Activating microphone...")
	mic = pyaudio.PyAudio()
	stream = mic.open(
		format=pyaudio.paInt16,
		channels=CHANNELS,
		rate=SAMPLING_RATE,
		input=True,
		frames_per_buffer=FRAMES_PER_BUFFER
	)
	stream.start_stream()

	logger.info("Recording audio...")
	text: list = []
	while ChatbotView.get_record_flag():
		logger.info("Waiting for sound...")
		try:
			data = stream.read(FRAMES_FLOW)

			if len(data) == 0:
				# ChatbotView.set_record_flag(False)
				break

			# logger.info("Convert audio data to numpy array...")
			# audio_data = np.frombuffer(data, dtype=np.int16)
			# logger.info("Applying lowpass filter...")
			# filtered_data = lowpass_filter(
			# 	audio_data,
			# 	cutoff=CUTOFF,
			# 	fs=SAMPLING_RATE,
			# 	order=ORDER
			# )
			# logger.info("Convert audio data back to bytes...")
			# filtered_data = filtered_data.astype(np.int16).tobytes()

			# if recognizer.AcceptWaveform(filtered_data):
			if recognizer.AcceptWaveform(data):
				logger.info("Getting text...")
				result = recognizer.Result()
				result_dict: dict = ast.literal_eval(result)
				logger.info(f"Speech recognition captured: {result_dict['text']}")
				text.append(result_dict["text"])

		except Exception as e:
			logger.error(
				f"An error ocurred while trying to make speech recognition: {e}")
			ChatbotView.set_record_flag(False)
			return None

	if text != []:
		final_text: str = (". ").join(text)
		logger.info(f"Final speech captured: {final_text}")
		return final_text
	else:
		logger.error(
				f"Failed to recognaize voice")
		# ChatbotView.set_record_flag(False)
		return None
