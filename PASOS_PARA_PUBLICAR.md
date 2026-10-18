# Cómo publicar Perform Football en GitHub y Render

**Versión 0.2.2: vista previa privada, no app de producción.**

## 1. Subir el código a GitHub

1. Entra en https://github.com/new e inicia sesión.
2. **Repository name:** `perform-football` (si no está disponible, `perform-football-app`).
3. Selecciona **Private**. No es necesario marcar opciones para crear README o `.gitignore`, porque ya vienen incluidos.
4. Pulsa **Create repository**.
5. En la nueva página, selecciona **uploading an existing file** o **Add file → Upload files**.
6. Descomprime `PerformFootball_listo_para_GitHub.zip` en tu equipo y **arrastra el contenido de la carpeta extraída** (todos los archivos del proyecto) al repositorio. `package.json` y `server.mjs` deben quedar directamente en la raíz, no dentro de otra carpeta.
7. Pulsa **Commit changes**. No subas `.env` ni ninguna clave privada.
8. Copia la URL de tu repositorio, que tendrá el formato `https://github.com/TU_USUARIO/perform-football`.

## 2. Conectar a Render y publicar

1. En https://dashboard.render.com/ inicia sesión y pulsa **New → Web Service**.
2. Selecciona **Git Provider → GitHub**. Autoriza a Render a acceder al repositorio privado `perform-football` (si aparece la opción, autoriza solo ese repositorio).
3. Configura **Runtime: Node**, **Branch: main**, **Region: Frankfurt** si tu zona principal es Europa, **Plan: Free** para una vista previa.
4. **Build command:** `npm install`; **Start command:** `npm start` (equivale a `node server.mjs`).
5. En **Environment Variables**, añade:
   - `NODE_ENV=production`
   - `HOST=0.0.0.0`
   - `PERFORM_USER` = el usuario de acceso que elijas.
   - `PERFORM_PASSWORD` = contraseña aleatoria privada de al menos 16 caracteres.
   - `OPENAI_API_KEY` = clave de API de OpenAI (opcional hasta activar la IA).
   - `OPENAI_MODEL=gpt-4.1-mini` (opcional).
   - `OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe` (opcional).
   No pongas estos secretos en el repositorio y no los copies en un chat.
6. Crea el servicio y espera a que el deploy salga como **Live**.
7. Abre la URL `https://<tu-servicio>.onrender.com`. Debe pedir usuario y contraseña. `/healthz` devuelve un estado de servidor, sin información privada.

## 3. Limitaciones y advertencias

- **No hay base de datos remota:** los registros se quedan en cada navegador, no se sincronizan entre dispositivos y se pierden si se borran los datos locales.
- **Acceso HTTP Basic provisional:** no sustituye un login moderno con sesiones, contraseñas cifradas y permisos por usuario.
- El plan gratuito puede entrar en reposo y tardar en despertar.
- La API de OpenAI puede generar costes independientes de ChatGPT.
- La interpretación de audios y fotos reales solo funcionará al configurar una clave válida.
- No introduzcas datos de salud sensibles ni uses la versión como registro definitivo hasta implementar autenticación completa y almacenamiento persistente.

## Siguiente fase

Añadir cuentas de usuario y una base PostgreSQL persistente con copia de seguridad, migración controlada de los datos locales y sincronización móvil-ordenador.
