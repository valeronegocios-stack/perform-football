# Activar la base de datos online de Perform Football

## Paso 1 — GitHub

Descarga `PerformFootball_v0.3_PostrgreSQL.zip`, descomprímelo y abre la carpeta. En tu repositorio `https://github.com/valeronegocios-stack/perform-football`, selecciona `Add file` → `Upload files`. Sube `server.mjs`, `app.js`, `index.html`, `package.json` y `schema.sql` de la raíz de la carpeta. Confirma que GitHub ofrece reemplazar los 4 archivos existentes (y añadir schema.sql). Pulsa `Commit changes`.

## Paso 2 — Render (solo cuando GitHub haya desplegado)

- Sitio: `https://dashboard.render.com/web/srv-dbaem5e1egvs73ae2s7g`
- Base de datos nueva (gratuita de desarrollo): `https://dashboard.render.com/d/dpg-dbaet18m7kps738j32r0-a`
- Abre la base → `Connect` → **Internal Database URL** → copiar.
- Abre el sitio → `Environment` → `Add Environment Variable`.
- **Key:** `DATABASE_URL`.
- **Value:** pega la URL interna de PostgreSQL que copiaste.
- Guarda los cambios y espera a que Render complete el nuevo despliegue. No edites las otras variables de usuario/contraseña.

No pegues el enlace interno en chats, capturas ni GitHub: incluye usuario y contraseña de la base de datos.

## Paso 3 — Prueba de sincronización

1. Entra en `https://perform-football.onrender.com`.
2. Abre **Ajustes** y confirma que indique `Datos sincronizados en la nube` o `Nube conectada`.
3. Añade una sesión ficticia: 60 minutos y RPE 5 (300 UA).
4. En una ventana de incógnito, inicia sesión con el mismo usuario/contraseña y comprueba que ves la sesión.
5. Vuelve al primer navegador: después de unos segundos debería mantenerse el mismo registro.
6. Exporta un archivo JSON en **Ajustes** como respaldo.

**No uses datos reales todavía.** El plan gratis de PostgreSQL caduca el 17/11/2026 y no ofrece backups. Primero acordaremos la opción definitiva con almacenamiento duradero y seguridad personal.
