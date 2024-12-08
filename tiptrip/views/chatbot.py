import wave
import flet as ft
from time import sleep
from os.path import join
from logging import Logger, getLogger
from base64 import b64encode, b64decode

from requests import post, Response
from requests.exceptions import ConnectTimeout

from resources.texts import *
from resources.config import *
from resources.functions import *
from components.bars import TopBar
from components.message import Message
from components.audio_player import AudioPlayer
from resources.styles import txt_messages_style


logger: Logger = getLogger(f"{PROJECT_NAME}.{__name__}")


class ChatbotView(ft.View):
	def __init__(self, page: ft.Page) -> None:
		# Custom attributes
		self.page = page
		self.record_flag: bool = False

		# Custom components
		self.ph: ft.PermissionHandler = ft.PermissionHandler()
		page.overlay.append(self.ph)

		self.gl: ft.Geolocator = ft.Geolocator(
			location_settings=ft.GeolocatorSettings(
				accuracy=ft.GeolocatorPositionAccuracy.LOW
			),
			on_error=lambda error: logger.error(f"Geolocator error: {error}"),
		)
		self.page.overlay.append(self.gl)

		# Audio recorder components
		self.audio_recorder: ft.AudioRecorder = ft.AudioRecorder(
			channels_num=CHANNELS,
			sample_rate=SAMPLING_RATE,
			audio_encoder=ft.AudioEncoder.WAV,
			auto_gain=True,
			cancel_echo=True,
			suppress_noise=True
		)
		self.page.overlay.append(self.audio_recorder)

		# Settings components
		self.swt_audio: ft.Switch = ft.Switch(
			value=self.page.session.get("swt_audio_value"),
			adaptive=True,
			active_color=ft.Colors.WHITE,
			active_track_color=SECONDARY_COLOR,
			on_change=self.swt_audio_changed
		)
		self.ext_settings: ft.ExpansionTile = ft.ExpansionTile(
			trailing=ft.Icon(
				name=ft.Icons.KEYBOARD_ARROW_DOWN,
				color=ft.Colors.BLACK,
				size=22
			),
			title=ft.Text(
				value="Configuraciones de chat",
				color=ft.Colors.BLACK,
				size=16
			),
			tile_padding=ft.padding.symmetric(horizontal=SPACING),
			controls=[
				ft.Container(
					bgcolor=ft.Colors.TRANSPARENT,
					padding=ft.padding.only(
						top=SPACING,
						left=SPACING,
						right=SPACING,
						bottom=0
					),
					alignment=ft.alignment.center_left,
					content=ft.Text(
						value="Respuestas del chatbot usando:",
						color=ft.Colors.BLACK,
						size=16
					)
				),
				ft.Container(
					margin=ft.margin.only(bottom=(SPACING / 2)),
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_EVENLY,
						controls=[
							ft.Text(
								value="Texto",
								color=ft.Colors.BLACK,
								size=16
							),
							self.swt_audio,
							ft.Text(
								value="Audio",
								color=ft.Colors.BLACK,
								size=16
							)
						]
					)
				)
			]
		)

		# ListView (Chat) components
		self.txt_message: ft.TextField = ft.TextField(
			label="Escribe un mensaje",
			on_change=self.validate,
			autofocus=True,
			capitalization=ft.TextCapitalization.SENTENCES,
			autocorrect=True,
			multiline=True,
			shift_enter=True,
			max_length=250,
			max_lines=10,
			**txt_messages_style
		)
		self.page.session.set(
			key="lv_chat_controls",
			value=(
				[
					ft.Row(
						alignment=ft.MainAxisAlignment.START,
						controls=[
							ft.Container(
								expand=9,
								expand_loose=True,
								content=Message(is_bot=True, message=AGENT_WELCOME_MESSAGE)
							),
							ft.Container(expand=1)
						]
					)
				]
				if self.page.session.get("lv_chat_controls") == []
				else self.page.session.get("lv_chat_controls")
			)
		)
		self.lv_chat: ft.ListView = ft.ListView(
			padding=ft.padding.all(value=SPACING),
			spacing=(SPACING / 2),
			auto_scroll=True,
			controls=self.page.session.get("lv_chat_controls")
		)
		self.cca_mic: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=(SPACING * 1.5),
			content=ft.Icon(
				name=ft.Icons.MIC,
				color=ft.Colors.WHITE,
				size=25
			)
		)
		self.cca_send: ft.CircleAvatar = ft.CircleAvatar(
			bgcolor=MAIN_COLOR,
			radius=(SPACING * 1.5),
			content=ft.Icon(
				name=ft.Icons.SEND,
				color=ft.Colors.WHITE,
				size=25
			)
		)
		self.cont_icon: ft.Container = ft.Container(
			expand=1,
			alignment=ft.alignment.center_right,
			content=self.cca_mic,
			data=ft.PermissionType.LOCATION,
			on_click=self.cca_mic_clicked
		)

		# Modals components
		self.dlg_error: ft.AlertDialog = ft.AlertDialog(
			modal=True,
			title=ft.Text(""),
			content=ft.Text(""),
			actions=[
				ft.TextButton("Aceptar", on_click=lambda _: self.page.close(self.dlg_error)),
			],
			actions_alignment=ft.MainAxisAlignment.END,
			on_dismiss=lambda _: self.page.close(self.dlg_error)
		)

		# View native attributes
		super().__init__(
			route="/chatbot",
			bgcolor=ft.Colors.WHITE,
			padding=ft.padding.all(value=0.0),
			spacing=0,
			controls=[
				TopBar(page=self.page, leading=True, logger=logger),
				ft.Container(
					width=self.page.width,
					bgcolor=MAIN_COLOR,
					border_radius=ft.border_radius.only(
						bottom_left=RADIUS,
						bottom_right=RADIUS
					),
					shadow=ft.BoxShadow(
						blur_radius=BLUR,
						color=ft.Colors.GREY_800
					),
					content=self.ext_settings
				),
				ft.Container(
					expand=True,
					width=self.page.width,
					content=self.lv_chat
				),
				ft.Container(
					width=self.page.width,
					padding=ft.padding.all(value=(SPACING / 2)),
					height=CONT_MESSAGE_HEIGHT,
					content=ft.Row(
						alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
						vertical_alignment=ft.CrossAxisAlignment.CENTER,
						spacing=0,
						controls=[
							ft.Container(
								expand=5,
								height=TXT_CONT_SIZE,
								bgcolor=ft.Colors.WHITE,
								padding=ft.padding.symmetric(
									horizontal=SPACING
								),
								border_radius=ft.border_radius.all(
									value=RADIUS
								),
								shadow=ft.BoxShadow(
									blur_radius=(BLUR / 2),
									offset=ft.Offset(0, 2),
									color=ft.Colors.BLACK12
								),
								alignment=ft.alignment.center_left,
								content=ft.Column(
									scroll=ft.ScrollMode.HIDDEN,
									controls=[self.txt_message]
								)
							),
							self.cont_icon,
						]
					)
				)
			]
		)

	def validate(self, _: ft.ControlEvent) -> None:
		if self.txt_message.value == "":
			# self.record_flag = True
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked
		else:
			self.cont_icon.content = self.cca_send
			self.cont_icon.on_click = self.cca_send_clicked
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

	def add_message(self, is_bot: bool, message: str, must_anwser: bool = False) -> None:
		lv_chat_controls: list = self.page.session.get("lv_chat_controls")
		if not is_bot:
			logger.info("Adding user message...")
			lv_chat_controls.append(
				ft.Row(
					alignment=ft.MainAxisAlignment.END,
					controls=[
						ft.Container(expand=1),
						ft.Container(
							expand=9,
							expand_loose=True,
							content=Message(is_bot=is_bot, message=message)
						)
					]
				)
			)
			self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
			self.lv_chat.controls = self.page.session.get("lv_chat_controls")
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)
		else:
			if not must_anwser:
				logger.info("Adding agent message while process the user message...")
				lv_chat_controls.append(
					ft.Row(
						alignment=ft.MainAxisAlignment.START,
						controls=[
							ft.Container(
								expand=9,
								expand_loose=True,
								content=Message(is_bot=is_bot, message=message)
							),
							ft.Container(expand=1)
						]
					)
				)
				self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
				self.lv_chat.controls = self.page.session.get("lv_chat_controls")
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

			else:
				if not "ERROR" in message:
					logger.info("Calling the back-end agent to process the user message...")
					try:
						response: Response = post(
							url=f"{BACK_END_URL}/{AGENT_ENDPOINT}/{self.page.session.get('id')}",
							headers={
								"Content-Type": "application/json",
								"Authorization": f"Bearer {self.page.session.get('session_token')}"
							},
							json={"prompt": lv_chat_controls[-2].controls[1].content.content.value}
						)
					except ConnectTimeout:
						logger.error("Connection timeout while getting favorite places. Replacing last agent message with error message...")
						lv_chat_controls[-1].controls[0].content = Message(
							is_bot=True,
							message=(
								"No se pudo obtener información sobre los sitios turísticos. "
								"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
							)
						)
						try:
							self.page.update()
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.update()
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)
						finally:
							return

					logger.info("Evaluating the agent response...")
					if response.status_code == 201:
						logger.info("Agent response is OK.")

						logger.info("Checking chosen response format...")
						if not self.swt_audio.value:
							logger.info("Agent response is only text")

							logger.info("Replacing last agent message with agent response message...")
							lv_chat_controls[-1].controls[0].content = Message(
								is_bot=True,
								message=response.json()["text"],
							)

						else:
							logger.info("User is asking for audio messages. Splitting message...")
							agent_responses: list[str] = split_text(
								response.json()["text"],
								chunk_size=1000,
								chunk_overlay=100,
								separator="\n"
							)
							for index, agent_response in enumerate(agent_responses):
								logger.info(f"Processing agent response {index + 1} of {len(agent_responses)}...")
								logger.info("Calling the tts model to process the agent message...")
								try:
									tts_response: Response = post(
										url=f"{BACK_END_URL}/{TTS_ENDPOINT}",
										headers={
											"Content-Type": "application/json",
											"Authorization": f"Bearer {self.page.session.get('session_token')}"
										},
										json={"text": agent_response}
									)

								except ConnectTimeout:
									logger.error("Connection timeout while getting favorite places. Replacing last agent message with error message...")
									lv_chat_controls[-1].controls[0].content = Message(
										is_bot=True,
										message=(
											"No se pudo obtener información sobre los sitios turísticos. "
											"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
										)
									)
									self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
									self.lv_chat.controls = self.page.session.get("lv_chat_controls")
									try:
										self.page.update()
									except Exception as e:
										logger.error(f"Error: {e}")
										self.page.update()
										#! COMMENT
										post(
											url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
											headers={"Content-Type": "application/json"},
											json={
												"user_id": self.page.session.get("id"),
												"file": encode_logfile()
											}
										)
									finally:
										return

								if tts_response.status_code == 201:
									logger.info("Getting audio data from tts response...")
									audio_data: dict = tts_response.json()["audio_data"]

									logger.info("Decoding audio data...")
									audio_binary: bytes = b64decode(audio_data["audio"])

									logger.info("Saving as temporary audio file...")
									last_agent_audio_id: int = get_audio_id(type="agent")
									self.page.session.set(
										key="last_agent_audio_filename",
										value=f"{join(TEMP_ABSPATH, TEMP_AGENT_AUDIO_FILENAME)}_{last_agent_audio_id}.wav"
									)
									with wave.open(self.page.session.get("last_agent_audio_filename"), "wb") as file:
										file.setnchannels(audio_data["nchannels"])
										file.setsampwidth(audio_data["sampwidth"])
										file.setframerate(audio_data["framerate"])
										file.setnframes(audio_data["nframes"])
										# file.setcomptype(audio_data["comp_type"])
										# file.setcompname(audio_data["comp_name"])
										file.writeframes(audio_binary)

									logger.info("Creating new AudioPlayer component and waiting for audio to be loaded...")
									audio_players = self.page.session.get("audio_players")
									audio_players.append(
										AudioPlayer(
											page=self.page,
											src=self.page.session.get("last_agent_audio_filename"),
											components_width=self.page.width
										)
									)

									logger.info("Replacing last agent message...")
									if isinstance(lv_chat_controls[-1].controls[0].content.content, ft.Markdown):
										lv_chat_controls[-1].controls[0].content = audio_players[-1]
									else:
										lv_chat_controls.append(audio_players[-1])

									self.page.session.set(key="audio_players", value=audio_players)
									self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
									self.lv_chat.controls = self.page.session.get("lv_chat_controls")

								else:
									logger.info(f"TTS endpoint response received {tts_response.status_code}: {tts_response.json()}")
									logger.info("Replacing last agent message with error text...")
									if lv_chat_controls[-1].controls[0].bgcolor == ft.colors.WHITE:
										lv_chat_controls[-1].controls[0].content = Message(
											is_bot=True,
											message="AGENT_ERROR",
										)
									self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
									self.lv_chat.controls = self.page.session.get("lv_chat_controls")
								sleep(2)

					else:
						logger.info(f"Agent endpoint response received {response.status_code}: {response.json()}")
						logger.info("Agent response is NOT ok. Replacing last agent message with error message...")
						lv_chat_controls[-1].controls[0].content = Message(
							is_bot=True,
							message="AGENT_ERROR",
						)
						self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
						self.lv_chat.controls = self.page.session.get("lv_chat_controls")

		logger.info("Updating live view components...")
		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

	def cca_send_clicked(self, event: ft.ControlEvent) -> None:
		if self.txt_message.value == "" or self.txt_message.value.isspace():
			logger.info("Empty message, not sending...")

		else:
			lv_chat_controls: list = self.page.session.get("lv_chat_controls")
			logger.info("Send button clicked")

			logger.info("Changing components to initial state...")
			aux_message: str = self.txt_message.value
			self.txt_message.value = ""
			self.cont_icon.content = self.cca_mic
			self.cont_icon.on_click = self.cca_mic_clicked
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			self.add_message(is_bot=False, message=aux_message)
			self.add_message(is_bot=True, message="Buscando información...")

			logger.info("Checking if the agent needs user's location...")
			for phrase in LOCATION_PHRASES:
				if phrase in aux_message.lower():
					logger.info("Agent is asking for user location. Checking location permissions...")
					permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
					logger.info(f"Location permissions status: {permission}")
					if permission == ft.PermissionStatus.GRANTED:
						logger.info("Location permissions granted. Getting current coordinates...")
						try:
							current_position: ft.GeolocatorPosition = self.gl.get_current_position()
							self.page.session.set(key="current_latitude", value=current_position.latitude)
							self.page.session.set(key="current_longitude", value=current_position.longitude)
							logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

							logger.info("Verifying if user's location is inside CDMX coordinates...")
							if is_inside_cdmx((self.page.session.get("current_latitude"), self.page.session.get("current_longitude"))):
								logger.info("User's location is inside CDMX coordinates. Saving user's location inside DB...")

								response: Response = post(
									url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
									headers={
										"Content-Type": "application/json",
										"Authorization": f"Bearer {self.page.session.get('session_token')}"
									},
									json={
										"latitude": self.page.session.get("current_latitude"),
										"longitude": self.page.session.get("current_longitude")
									}
								)

								if response.status_code == 201:
									logger.info("User's coordinates saved successfully")
									sleep(2)
									break

								else:
									logger.warning(f"Error saving user's coordinates: {response.json()}")
									logger.info("Replacing last agent message with error message...")
									lv_chat_controls[-1].controls[0].content = Message(
										is_bot=True,
										message=(
											"Ocurrió un error al solicitar información de lugares cercanos a tu ubicación actual. "
											"Favor de intentarlo de nuevo más tarde."
										)
									)
									self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
									self.lv_chat.controls = self.page.session.get("lv_chat_controls")
									try:
										self.page.update()
									except Exception as e:
										logger.error(f"Error: {e}")
										self.page.update()
										#! COMMENT
										post(
											url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
											headers={"Content-Type": "application/json"},
											json={
												"user_id": self.page.session.get("id"),
												"file": encode_logfile()
											}
										)
									finally:
										return

							else:
								logger.warning("User's location is outside CDMX coordinates. Replacing last agent message with error message...")
								lv_chat_controls[-1].controls[0].content = Message(
									is_bot=True,
									message=(
										"Tu ubicación actual se encuentra fuera de los límites de la Ciudad de México, "
										"por lo que no se puede realizar la búsqueda de información de lugares cercanos a tu ubicación actual."
									)
								)
								self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
								self.lv_chat.controls = self.page.session.get("lv_chat_controls")
								try:
									self.page.update()
								except Exception as e:
									logger.error(f"Error: {e}")
									self.page.update()
									#! COMMENT
									post(
										url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
										headers={"Content-Type": "application/json"},
										json={
											"user_id": self.page.session.get("id"),
											"file": encode_logfile()
										}
									)
								finally:
									return

						except Exception as e:
							logger.warning(f"Error getting current coordinates: {e}")
							logger.info("Replacing last agent message with error message...")
							lv_chat_controls[-1].controls[0].content = Message(
								is_bot=True,
								message=(
									"No se han otorgado los permisos de ubicación, "
									"por lo que no se puede realizar la búsqueda de información "
									"de lugares cercanos a tu ubicación actual.\n"
									"Por favor intenta de nuevo con una pregunta diferente."
								)
							)
							self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
							self.lv_chat.controls = self.page.session.get("lv_chat_controls")
							try:
								self.page.update()
							except Exception as e:
								logger.error(f"Error: {e}")
								self.page.update()
								#! COMMENT
								post(
									url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
									headers={"Content-Type": "application/json"},
									json={
										"user_id": self.page.session.get("id"),
										"file": encode_logfile()
									}
								)
							finally:
								return

					else:
						logger.warning("Location permissions are not granted. Replacing last agent message with error message...")
						lv_chat_controls[-1].controls[0].content = Message(
							is_bot=True,
							message=(
								"No se han otorgado los permisos de ubicación, "
								"por lo que no se puede realizar la búsqueda de información "
								"de lugares cercanos a tu ubicación actual.\n"
								"Por favor intenta de nuevo con una pregunta diferente."
							)
						)
						self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
						self.lv_chat.controls = self.page.session.get("lv_chat_controls")
						try:
							self.page.update()
						except Exception as e:
							logger.error(f"Error: {e}")
							self.page.update()
							#! COMMENT
							post(
								url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
								headers={"Content-Type": "application/json"},
								json={
									"user_id": self.page.session.get("id"),
									"file": encode_logfile()
								}
							)
						finally:
							return

			self.add_message(
				is_bot=True,
				message=lv_chat_controls[-2].controls[1].content.content.value,
				must_anwser=True
			)

	def cca_mic_clicked(self, event: ft.ControlEvent) -> None:
		if not self.record_flag:
			logger.info("Recording audio process started...")

			logger.info("Asking for audio permissions if not granted...")
			if not self.audio_recorder.has_permission(wait_timeout=60.0):
				logger.warning("Audio permissions are not granted. Opening audio permissions dialog...")
				try:
					self.page.open(self.dlg_request_audio_permission)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_request_audio_permission)
				finally:
					return

			logger.info("Changing UI components to recording state...")
			self.txt_message.value = "Grabando audio..."
			self.cca_mic.bgcolor = ft.Colors.RED
			self.cca_mic.content = ft.Icon(
				name=ft.Icons.SEND,
				color=ft.Colors.WHITE,
				size=25
			)
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Starting audio recording...")
			self.record_flag = True
			last_user_audio_id: int = get_audio_id(type="user")
			self.page.session.set(
				key="last_user_audio_filename",
				value=f"{join(TEMP_ABSPATH, TEMP_USER_AUDIO_FILENAME)}_{last_user_audio_id}.wav"
			)
			self.audio_recorder.start_recording(
				output_path=self.page.session.get("last_user_audio_filename")
			)

		else:
			lv_chat_controls: list = self.page.session.get("lv_chat_controls")
			logger.info("Changing UI components to initial state...")
			self.txt_message.value = ""
			self.cca_mic.bgcolor = MAIN_COLOR
			self.cca_mic.content = ft.Icon(
				name=ft.Icons.MIC,
				color=ft.Colors.WHITE,
				size=25
			)
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			self.add_message(is_bot=False, message="Convirtiendo audio en texto...")

			logger.info("Stopping audio recording...")
			self.record_flag = False
			self.audio_recorder.stop_recording()

			logger.info("Encoding audio file...")
			with open(self.page.session.get("last_user_audio_filename"), "rb") as audio_file:
				encoded_audio_data: str = b64encode(audio_file.read()).decode("utf-8")

			logger.info("Speech recognition process started...")
			try:
				response: Response = post(
					url=f"{BACK_END_URL}/{ASR_ENDPOINT}",
					headers={
						"Content-Type": "application/json",
						"Authorization": f"Bearer {self.page.session.get('session_token')}"
					},
					json={
						"audio": encoded_audio_data
					}
				)

			except ConnectTimeout:
				logger.error("Connection timeout while authenticating user")
				self.dlg_error.title = ft.Text(value="Error de conexión a internet")
				self.dlg_error.content = ft.Text(
					value=(
						"Ocurrió un error de conexión a internet al intentar convertir el mensaje de voz en texto. "
						"Favor de revisar su conexión a internet e intentarlo de nuevo más tarde."
					)
				)
				try:
					self.page.open(self.dlg_error)
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.open(self.dlg_error)
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)
				finally:
					return

			logger.info(f"Speech recognition (ASR) endpoint response received {response.status_code}: {response.json()}")
			if response.status_code == 201:
				user_message: str = response.json()["text"]
				logger.info(f"Speech captured: {user_message}. Replacing last user temp message with audio message...")
				lv_chat_controls[-1].controls[1].content = Message(
					is_bot=False,
					message=user_message.capitalize(),
				)
				self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
				self.lv_chat.controls = self.page.session.get("lv_chat_controls")
				self.add_message(is_bot=True, message="Buscando información...")
				try:
					self.page.update()
				except Exception as e:
					logger.error(f"Error: {e}")
					self.page.update()
					#! COMMENT
					post(
						url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
						headers={"Content-Type": "application/json"},
						json={
							"user_id": self.page.session.get("id"),
							"file": encode_logfile()
						}
					)

				logger.info("Checking if the agent needs user's location...")
				user_message = lv_chat_controls[-2].controls[1].content.content.value
				for phrase in LOCATION_PHRASES:
					if phrase in user_message.lower():
						logger.info("Agent is asking for user location. Checking location permissions...")
						permission: ft.PermissionStatus = self.ph.request_permission(event.control.data, wait_timeout=60)
						logger.info(f"Location permissions status: {permission}")
						if permission == ft.PermissionStatus.GRANTED:
							logger.info("Location permissions granted. Getting current coordinates...")
							try:
								current_position: ft.GeolocatorPosition = self.gl.get_current_position()
								self.page.session.set(key="current_latitude", value=current_position.latitude)
								self.page.session.set(key="current_longitude", value=current_position.longitude)
								logger.info(f"Got current coordinates: ({current_position.latitude}, {current_position.longitude})")

								logger.info("Verifying if user's location is inside CDMX coordinates...")
								if is_inside_cdmx((self.page.session.get("current_latitude"), self.page.session.get("current_longitude"))):
									logger.info("User's location is inside CDMX coordinates. Saving user's location inside DB...")

									response: Response = post(
										url=f"{BACK_END_URL}/{USERS_ENDPOINT}/{self.page.session.get('id')}",
										headers={
											"Content-Type": "application/json",
											"Authorization": f"Bearer {self.page.session.get('session_token')}"
										},
										json={
											"latitude": self.page.session.get("current_latitude"),
											"longitude": self.page.session.get("current_longitude")
										}
									)

									if response.status_code == 201:
										logger.info("User's coordinates saved successfully")
										sleep(2)
										break

									else:
										logger.warning(f"Error saving user's coordinates: {response.json()}")
										logger.info("Replacing last agent message with error message...")
										lv_chat_controls[-1].controls[0].content = Message(
											is_bot=True,
											message=(
												"Ocurrió un error al solicitar información de lugares cercanos a tu ubicación actual. "
												"Favor de intentarlo de nuevo más tarde."
											)
										)
										self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
										self.lv_chat.controls = self.page.session.get("lv_chat_controls")

										try:
											self.page.update()
										except Exception as e:
											logger.error(f"Error: {e}")
											self.page.update()
											#! COMMENT
											post(
												url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
												headers={"Content-Type": "application/json"},
												json={
													"user_id": self.page.session.get("id"),
													"file": encode_logfile()
												}
											)
										finally:
											return

								else:
									logger.warning("User's location is outside CDMX coordinates. Replacing last agent message with error message...")
									lv_chat_controls[-1].controls[0].content = Message(
										is_bot=True,
										message=(
											"Tu ubicación actual se encuentra fuera de los límites de la Ciudad de México, "
											"por lo que no se puede realizar la búsqueda de información de lugares cercanos a tu ubicación actual."
										)
									)
									self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
									self.lv_chat.controls = self.page.session.get("lv_chat_controls")
									try:
										self.page.update()
									except Exception as e:
										logger.error(f"Error: {e}")
										self.page.update()
										#! COMMENT
										post(
											url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
											headers={"Content-Type": "application/json"},
											json={
												"user_id": self.page.session.get("id"),
												"file": encode_logfile()
											}
										)
									finally:
										return

							except Exception as e:
								logger.warning(f"Error getting current coordinates: {e}")
								logger.info("Replacing last agent message with error message...")
								lv_chat_controls[-1].controls[0].content = Message(
									is_bot=True,
									message=(
										"No se han otorgado los permisos de ubicación, "
										"por lo que no se puede realizar la búsqueda de información "
										"de lugares cercanos a tu ubicación actual.\n"
										"Por favor intenta de nuevo con una pregunta diferente."
									)
								)
								self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
								self.lv_chat.controls = self.page.session.get("lv_chat_controls")
								try:
									self.page.update()
								except Exception as e:
									logger.error(f"Error: {e}")
									self.page.update()
									#! COMMENT
									post(
										url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
										headers={"Content-Type": "application/json"},
										json={
											"user_id": self.page.session.get("id"),
											"file": encode_logfile()
										}
									)
								finally:
									return

						else:
							logger.warning("Location permissions are not granted. Replacing last agent message with error message...")
							lv_chat_controls[-1].controls[0].content = Message(
								is_bot=True,
								message=(
									"No se han otorgado los permisos de ubicación, "
									"por lo que no se puede realizar la búsqueda de información "
									"de lugares cercanos a tu ubicación actual.\n"
									"Por favor intenta de nuevo con una pregunta diferente."
								)
							)
							self.page.session.set(key="lv_chat_controls", value=lv_chat_controls)
							self.lv_chat.controls = self.page.session.get("lv_chat_controls")
							try:
								self.page.update()
							except Exception as e:
								logger.error(f"Error: {e}")
								self.page.update()
								#! COMMENT
								post(
									url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
									headers={"Content-Type": "application/json"},
									json={
										"user_id": self.page.session.get("id"),
										"file": encode_logfile()
									}
								)
							finally:
								return

				self.add_message(
					is_bot=True,
					message=lv_chat_controls[-2].controls[1].content.content.value,
					must_anwser=True
				)

			else:
				self.add_message(is_bot=False, message="SPEECH_RECOGNITION_ERROR")

	def request_audio_permission(self, _: ft.ControlEvent) -> None:
		try:
			self.page.close(self.dlg_request_audio_permission)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_request_audio_permission)
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

		logger.info("Requesting audio permissions...")

		logger.info("Asking for audio permissions...")
		if self.audio_recorder.has_permission(wait_timeout=60.0):
			logger.info("Audio permissions granted. Changing UI components to recording state...")
			self.txt_message.value = "Grabando audio..."
			self.cca_mic.bgcolor = ft.Colors.RED
			self.cca_mic.content = ft.Icon(
				name=ft.Icons.STOP,
				color=ft.Colors.WHITE,
				size=25
			)
			try:
				self.page.update()
			except Exception as e:
				logger.error(f"Error: {e}")
				self.page.update()
				#! COMMENT
				post(
					url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
					headers={"Content-Type": "application/json"},
					json={
						"user_id": self.page.session.get("id"),
						"file": encode_logfile()
					}
				)

			logger.info("Starting audio recording...")
			self.audio_recorder.start_recording(join(TEMP_ABSPATH, TEMP_USER_AUDIO_FILENAME))
			self.record_flag = True

		else:
			logger.warning("Audio permissions denied. Replacing last agent message with error message...")
			self.add_message(
				is_bot=True,
				message=(
					"No se han otorgado los permisos de micrófono, por lo que no se "
					"pueden enviar mensajes de voz al agente conversacional."
				)
			)

	def request_audio_permission_denied(self, _: ft.ControlEvent) -> None:
		try:
			self.page.close(self.dlg_request_audio_permission)
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.close(self.dlg_request_audio_permission)
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)

		logger.warning("Audio permissions denied. Replacing last agent message with error message...")
		self.add_message(
			is_bot=True,
			message=(
				"No se han otorgado los permisos de micrófono, por lo que no se "
				"pueden enviar mensajes de voz al agente conversacional."
			)
		)

	def swt_audio_changed(self, _: ft.ControlEvent) -> None:
		if self.swt_audio.value:
			logger.info("Switch audio for agent changed to Audio")
			self.swt_audio.value = True
			self.page.session.set(key="swt_audio_value", value=True)
		else:
			logger.info("Switch audio for agent changed to Text")
			self.swt_audio.value = False
			self.page.session.set(key="swt_audio_value", value=False)

		try:
			self.page.update()
		except Exception as e:
			logger.error(f"Error: {e}")
			self.page.update()
			#! COMMENT
			post(
				url=f"{BACK_END_URL}/{LOGS_ENDPOINT}",
				headers={"Content-Type": "application/json"},
				json={
					"user_id": self.page.session.get("id"),
					"file": encode_logfile()
				}
			)
