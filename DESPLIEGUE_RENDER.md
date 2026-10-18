# Perform Football — despliegue de vista privada en Render

**Esta es una versión de VISTA PREVIA, no la aplicación personal definitiva.**

## Qué incluye

- La web y el servidor Node con rutas de texto, imagen y audio preparadas para OpenAI.
- Protección HTTP Basic de un único usuario, obligatoria cuando `NODE_ENV=production`. Es un acceso **provisional**, no sustituye un login con sesiones, roles y permisos de acceso por registro.
- Limitación básica de peticiones de IA y comprobación de origen.
- Arranque compatible con el puerto y host proporcionados por Render, `/healthz` para health checks.
- **Los registros siguen guardándose únicamente en localStorage de cada navegador. No hay sincronización entre dispositivos ni base de datos remota.** Exporta copias desde Ajustes.
- El asistente de voz/fotos necesita `OPENAI_API_KEY` en **Variables de entorno**, nunca en archivos públicos.

## Paso a paso

1. Conecta Render en ChatGPT o inicia sesión en Render.
2. Sube esta carpeta a un repositorio Git privado. No incluyas ningún archivo `.env`.
3. Crea un Web Service Node en Render usando el repositorio o aplica el Blueprint de `render.yaml`.
4. Configura secretos: `PERFORM_USER` (usuario), `PERFORM_PASSWORD` (contraseña fuerte de 16+ caracteres), y de forma opcional `OPENAI_API_KEY`. **Nunca envíes esas claves por ChatGPT.**
5. Comprueba que la URL pública pide autenticación. Sin credenciales, la web y `/api/*` deben dar 401. `/healthz` responde 200 sin datos privados.
6. No utilices esta vista previa para almacenar registros sensibles a largo plazo; primero añade base de datos y acceso con sesiones.

## Limitaciones y seguridad

HTTP Basic es provisional: el navegador recuerda las credenciales y no hay cierre de sesión fiable. Render proporciona HTTPS para sus dominios. No uses dispositivos compartidos. El almacenamiento local es distinto en cada dispositivo y se puede borrar al limpiar el navegador.

Render Free puede entrar en reposo tras inactividad; las bases gratuitas de PostgreSQL expiran después de 30 días, así que no son adecuadas para datos definitivos. El uso de OpenAI API puede tener costes separados.

## Próxima etapa para uso real

- Login con sesiones.
- PostgreSQL persistente con backups y autorización por usuario.
- API para guardar y consultar entrenamientos, bienestar, alimentación y chat; migración voluntaria de datos locales.
- Pruebas con audios e imágenes reales al configurar la API key del servidor.
