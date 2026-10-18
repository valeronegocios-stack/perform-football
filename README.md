# Perform Football — vista previa protegida para alojamiento en Render

Lee primero `DESPLIEGUE_RENDER.md`. Esta variante añade protección provisional de usuario/contraseña, comprobación de origen y límites básicos para la IA. **No incluye base de datos remota ni sincronización entre dispositivos.**

Desarrollo local: `node server.mjs` (sin contraseña cuando `NODE_ENV` no es `production`). Prueba del modo online: configura `NODE_ENV=production`, `PERFORM_USER` y `PERFORM_PASSWORD` (contraseña de 16+ caracteres) como variables de entorno y arranca `node server.mjs`.

Nunca publiques ni compartas el archivo `.env` ni tu API key.
