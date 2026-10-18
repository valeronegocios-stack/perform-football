/** Configurador LOCAL de la clave de OpenAI para Perform Football.
 * La clave no se envía a ningún servicio ni aparece en pantalla.
 * Se escribe solo en .env (archivo privado, nunca en el HTML).
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';

const directory = path.dirname(fileURLToPath(import.meta.url));
const target = path.join(directory, '.env');
const template = path.join(directory, '.env.example');

function hiddenInput(label) {
  return new Promise((resolve, reject) => {
    if (!process.stdin.isTTY || !process.stdin.setRawMode) {
      reject(new Error('Por seguridad, ejecuta este archivo desde una terminal interactiva en tu ordenador.'));
      return;
    }
    process.stdout.write(label);
    const input = process.stdin;
    let value = '';
    const cleanup = () => {
      input.removeListener('data', onData);
      input.setRawMode(false);
      input.pause();
    };
    const onData = (chunk) => {
      for (const char of String(chunk)) {
        if (char === '\r' || char === '\n') {
          cleanup();
          process.stdout.write('\n');
          resolve(value);
          return;
        }
        if (char === '\u0003') {
          cleanup();
          process.stdout.write('\n');
          reject(new Error('Configuración cancelada.'));
          return;
        }
        if (char === '\u007f' || char === '\b') {
          value = value.slice(0, -1);
          continue;
        }
        if (char >= ' ' && char !== '\u007f') value += char;
      }
    };
    input.setRawMode(true);
    input.resume();
    input.setEncoding('utf8');
    input.on('data', onData);
  });
}

try {
  console.log('\nPERFORM FOOTBALL · CONFIGURACIÓN PRIVADA DE OPENAI');
  console.log('Tu clave se ocultará mientras la escribes o pegas y no saldrá de tu ordenador.');
  console.log('No publiques el archivo .env ni compartas tu clave con nadie.\n');
  let current = '';
  try { current = await fs.readFile(target, 'utf8'); } catch (err) { if (err.code !== 'ENOENT') throw err; }
  if (/^OPENAI_API_KEY=\S+/m.test(current)) {
    console.log('Ya hay una clave configurada en .env. Para evitar sobrescribirla, no se ha hecho ningún cambio.');
    console.log('Si necesitas sustituirla, edita el archivo .env solo en tu equipo.');
    process.exit(0);
  }
  const key = (await hiddenInput('Pega tu API Key y pulsa Enter (no se mostrará): ')).trim();
  if (!/^sk-[^\s"'`]+$/.test(key)) throw new Error('No parece una clave de OpenAI válida. No se ha guardado nada.');
  const base = current || await fs.readFile(template,'utf8');
  const next = /^OPENAI_API_KEY=/m.test(base)
    ? base.replace(/^OPENAI_API_KEY=.*$/m, () => `OPENAI_API_KEY=${key}`)
    : `OPENAI_API_KEY=${key}\n${base}`;
  await fs.writeFile(target, next, {encoding:'utf8',mode:0o600,flag:'w'});
  if(process.platform !== 'win32') await fs.chmod(target,0o600);
  console.log('\nClave guardada de manera privada en el archivo .env de este equipo.');
  console.log('Para iniciar la web, ejecuta: node --env-file=.env server.mjs');
  console.log('Abre después http://127.0.0.1:4173 en tu navegador.');
  console.log('La clave no se ha comprobado con OpenAI todavía. Al usar la IA puede haber costes por consumo.');
} catch (err) {
  console.error(`\nNo se ha podido configurar: ${err.message}`);
  process.exitCode=1;
}
