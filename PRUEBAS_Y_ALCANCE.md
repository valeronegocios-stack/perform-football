# Verificaciones y alcance · Perform Football v0.2

## Comprobado en pruebas automatizadas y simuladas

- Servidor local activo, estado de conexión y comprobación de credenciales configuradas sin exponerlas al navegador.
- Validación de tipo de audio no admitido (respuesta HTTP 415).
- Envío de audio binario mediante formulario al endpoint compatible de transcripción, con respuesta de servicio **simulado** (sin API externa ni transcripción de voz real).
- Extracción estructurada de tres borradores separados desde un mensaje con fútbol, gimnasio y sueño, con confirmación manual individual.
- Confirmación de sesión de fútbol de 75 min y RPE 7, con total correcto de **525 UA** y actualización del panel.
- Análisis conversacional mediante ruta `/api/chat`, respuesta sintética simulada.
- Introducción de archivo de audio en la interfaz, transcripción previa al envío y grabación controlada con simulación de micrófono/MediaRecorder.
- Maquetación para 1365 px y móvil de 390 px, sin desbordamiento horizontal de la pantalla de asistente; sin errores JavaScript en rutas verificadas.

## Pendiente para uso personal real y publicación

- Prueba de calidad con grabaciones reales en distintos móviles/navegadores, conexión HTTPS y permiso del micrófono.
- Prueba de OpenAI con clave propia y extractos reales de Footbar Meteor.
- Autenticación, almacenamiento en una base de datos privada, sincronización entre móvil y ordenador, backups automáticos y restricciones de consumo.
- Integración con el Meteor, si el fabricante tiene exportación o API compatibles.
- Auditoría de fórmulas y personalización basada en series temporales suficientes.

Los registros numéricos simulados en las pruebas NO son datos reales de ningún deportista.
