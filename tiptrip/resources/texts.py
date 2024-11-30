ADVICES: list[str] = [
	# Consejos de usabilidad
	"Puedes usar comandos de voz para realizar búsquedas.",
	"Encuentra tu lugar ideal, cerca de ti.",
	"En el mapa interactivo, ¡haz click en un marcador de un sitio turístico para ver su información!",
	"Sólo necesitas otorgar 2 permisos: ubicación y micrófono. ¡Y listo!",
	"¡Puedes preguntarme lo que quieras! Estoy aquí para ayudarte.",
	"¡Guarda tus sitios favoritos para visitarlos más tarde!",
	"¡Puedes cambiar tu contraseña en cualquier momento!",
	"¡Puedes leer nuestra política de privacidad y términos y condiciones en la app!",
	"¡Puedes actualizar tu perfil en cualquier momento!",
	"¡Puedes ver tus sitios favoritos en una lista!",
	"¡Habla conmigo! Envíame audios de voz para hacer tus preguntas de forma rápida y sencilla.",
	"Recuerda activar tu ubicación para obtener las mejores recomendaciones personalizadas.",
	"Filtra las recomendaciones según tu interés: museos, centros culturales, etc.",
	# Consejos de viaje
	"Siempre lleva contigo un botiquín de primeros auxilios.",
	"Una sonrisa y un saludo pueden abrir muchas puertas durante tu viaje.",
	"Camina y explora, pero no olvides llevar calzado cómodo para largas jornadas.",
	"Planifica tu viaje con antelación para evitar contratiempos de última hora.",
	"Lleva siempre algo de efectivo, pero ten cuidado con grandes sumas de dinero.",
	"Respeta las normas locales y cuida los espacios que visites.",
	# Consejos de seguridad
	"Evita usar auriculares en lugares muy concurridos para estar siempre alerta.",
	"Guarda tus pertenencias personales en lugares seguros y evita llevar objetos de valor.",
	"Evita usar auriculares en lugares muy concurridos para estar siempre alerta.",
	"Si viajas solo, informa a alguien de confianza sobre tu itinerario.",
	"Mantén tu dispositivo móvil cargado y lleva un power bank en tus viajes.",
	# Consejos sostenibles
	"Lleva tu propia botella de agua reutilizable y bolsas para evitar desechables.",
	"Opta por transporte público o rutas a pie para reducir tu huella de carbono.",
	"No olvides apoyar a los negocios locales y consume productos regionales durante tu viaje.",
	"Evita comprar souvenirs hechos con materiales que dañen el medio ambiente."
]

SPEECH_RECOGNITION_ERROR_MESSAGE: str = (
	"ERROR.\n"
	"Ocurrió un error al transcribir voz a texto. "
	"Favor de intentarlo de nuevo más tarde."
)

AGENT_ERROR_MESSAGE: str = (
	"ERROR.\n"
	"Ocurrió un error al obtener información del agente. "
	"Favor de intentarlo de nuevo más tarde."
)

AGENT_WELCOME_MESSAGE: str = (
	"¡Hola! Soy el agente conversacional de TIP TRIP.\n"
	"Estoy aquí para ayudarte con tus dudas y guiarte sobre los sitios turísticos cerca de tu ubicación actual.\n"
	"¿En qué puedo ayudarte?"
)

PRIVACY_POLITICS: str = "Esta es nuestra política de privacidad: ..."

TERMS_CONDITIONS: str = """
Cómo controlas tus datos personales.

Usted como usuario, tiene el control de sus datos personales, por lo que puede cambiarlos a su preferencia en cualquier momento.


Cómo recopilamos u utilizamos sus datos personales.

Recopilamos sus datos personales al momento de que usted como usuario nos proporcione dicha información para obtener una cuenta en nuestra aplicación móvil. Algunos de los datos personales que recopilamos son su nombre y correo electrónico.

Utilizamos sus datos personales con el fin de comprender mejor sus interés y preferencias como consumidor y persona. Estos fines incluyen presentarle un servicio y gestionar los clientes para la administración de cuentas.


Cómo protegemos tus datos.

Su privacidad es importante, por lo que tomamos medidas para proteger sus datos contra perdida, mal uso o alteraciones. Para ello, incluimos técnicas de cifrado de contraseñas únicas y complejas, así como capacitar al personal sobre las obligaciones de procesamiento de datos, identificar incidentes y riesgos.


Bases legales.
Generalmente, conservamos sus datos personales solo durante el tiempo que sea necesario para completar el propósito del procesamiento para el cual fueron recopilados o según lo exija la ley. Es posible que necesitemos conservar sus datos personales durante más tiempo que nuestros períodos de retención especificados para cumplir con sus solicitudes, incluso para continuar manteniendo su exclusión voluntaria de correos electrónicos de marketing o para cumplir con obligaciones legales o de otro tipo.
"""
