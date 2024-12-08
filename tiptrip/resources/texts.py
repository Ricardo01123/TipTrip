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

PRIVACY_POLITICS: str = """
Fecha de Vigencia: 7 de diciembre de 2024

1. Datos que Recopilamos
Recopilamos los siguientes datos personales proporcionados por usted al registrarse o interactuar con la aplicación:

Nombre
Correo electrónico
Ubicación geográfica actual (mediante servicios de geolocalización)
Datos de interacción con la app para mejorar nuestros servicios.

2. Finalidad del Tratamiento de Datos Personales
Sus datos personales son tratados con las siguientes finalidades:

Crear y gestionar su cuenta en la aplicación.
Proporcionarle un servicio personalizado, adaptado a sus preferencias e intereses.
Ofrecerle información sobre sitios turísticos basados en su ubicación.
Mejorar y optimizar la funcionalidad de la aplicación.
Responder a sus consultas o solicitudes de soporte técnico.
3. Legitimación para el Tratamiento de Datos
El tratamiento de sus datos se realiza con base a:

Su consentimiento explícito al aceptar esta política de privacidad.
La necesidad de tratar sus datos para ejecutar el servicio contratado a través de la aplicación.
4. Cesión de Datos a Terceros
No compartimos sus datos personales con terceros, salvo que sea necesario para:

Cumplir con obligaciones legales.
Proveer funcionalidades de la app mediante servicios externos, como proveedores de mapas o servicios de localización. En estos casos, garantizamos el cumplimiento de la normativa aplicable por parte de dichos terceros.

5.  Plazo de Conservación de Datos
Sus datos personales se conservarán únicamente durante el tiempo necesario para cumplir con las finalidades para las que se recopilaron o según lo exija la ley. Una vez cumplido este plazo, los datos serán eliminados de manera segura.

6. Derechos de los Usuarios
Como usuario, tiene los siguientes derechos en relación con sus datos personales:

Acceso: Solicitar una copia de sus datos personales.
Rectificación: Corregir datos inexactos o incompletos.
Supresión: Solicitar la eliminación de sus datos personales, salvo en casos requeridos por ley.
Limitación: Restringir el uso de sus datos en ciertas circunstancias.
Portabilidad: Recibir sus datos en un formato estructurado.
Oposición: Negarse al tratamiento de sus datos en situaciones específicas.

7.  Actualizaciones de la Política de Privacidad
Nos reservamos el derecho de modificar esta política de privacidad en cualquier momento. Notificaremos sobre cualquier cambio importante mediante la aplicación o al correo electrónico proporcionado. Le recomendamos revisar regularmente esta política para estar informado sobre cómo protegemos sus datos.

8. Permisos Solicitados por la App
Para funcionar correctamente, la app TipTrip solicita acceso a:

Micrófono: Para procesar comandos de voz y mejorar la experiencia del agente conversacional.
Ubicación: Para proporcionarle información turística basada en su posición geográfica.
9. Tratamiento de Datos de Menores
La app no está diseñada ni dirigida a menores de 13 años. Si descubrimos que hemos recopilado información de un menor sin el consentimiento de su tutor legal, eliminaremos dicha información inmediatamente.
"""

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
