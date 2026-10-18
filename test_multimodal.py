"""Pruebas locales sin una clave real de OpenAI (servidor falso solo en 127.0.0.1)."""
import json
import os
import subprocess
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent
class FakeOpenAI(BaseHTTPRequestHandler):
    calls=[]
    def log_message(self,*args): pass
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0')); payload=self.rfile.read(n)
        FakeOpenAI.calls.append((self.path,self.headers.get('Content-Type'),len(payload)))
        if self.path.endswith('/audio/transcriptions'):
            assert b'nota-perform' in payload and b'gpt-4o-mini-transcribe' in payload
            response={'text':'Hoy he hecho 75 minutos de fútbol, RPE 7, 45 minutos de gimnasio y he dormido 8 horas.'}
        else:
            body=json.loads(payload.decode())
            assert body.get('store') is False
            if 'extractor preciso' in body.get('instructions',''):
                response={'output':[{'content':[{'type':'output_text','text':json.dumps({'records':[
                    {'kind':'session','data':{'date':'2026-10-17','type':'team','duration':75,'rpe':7,'title':'Equipo'},'missing':[]},
                    {'kind':'session','data':{'date':'2026-10-17','type':'gym','duration':45,'rpe':None,'title':'Gimnasio'},'missing':['RPE del gimnasio']},
                    {'kind':'checkin','data':{'date':'2026-10-17','sleepHours':8},'missing':['Energía y molestias']}
                ]},ensure_ascii=False)}]}]}
            else:
                response={'output':[{'content':[{'type':'output_text','text':'Tu carga semanal medida es la que muestran los registros, siempre que estén completos.'}]}]}
        body=json.dumps(response).encode()
        self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)

def inline_html(js_mock):
    html=(ROOT/'index.html').read_text()
    html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+ (ROOT/'styles.css').read_text().replace("@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');",'') +'</style>')
    html=html.replace('<link rel="manifest" href="./manifest.webmanifest">','').replace('<link rel="icon" type="image/svg+xml" href="./icon.svg">','')
    html=html.replace('<script src="./app.js" defer></script>','<script>('+js_mock+')();</script><script>'+(ROOT/'app.js').read_text()+'</script>')
    return html

fake=HTTPServer(('127.0.0.1',4166),FakeOpenAI)
th=threading.Thread(target=fake.serve_forever,daemon=True);th.start()
env={**os.environ,'OPENAI_API_KEY':'test-dummy-no-network','OPENAI_API_BASE_URL':'http://127.0.0.1:4166','PORT':'4173','HOST':'127.0.0.1'}
server=subprocess.Popen(['node','server.mjs'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
try:
    for i in range(80):
        try:
            r=requests.get('http://127.0.0.1:4173/api/health',timeout=.3)
            if r.ok:break
        except Exception: time.sleep(.1)
    else:raise AssertionError('Server did not start')
    assert r.json()['transcriptionEnabled'] is True
    invalid=requests.post('http://127.0.0.1:4173/api/transcribe',data=b'abc',headers={'Content-Type':'text/plain'})
    assert invalid.status_code==415, (invalid.status_code,invalid.text)
    audio=requests.post('http://127.0.0.1:4173/api/transcribe',data=b'fake audio body',headers={'Content-Type':'audio/webm'})
    assert audio.ok and '75 minutos' in audio.json()['text'], audio.text
    interpretation=requests.post('http://127.0.0.1:4173/api/interpret',json={'message':'Hoy he hecho 75 min de fútbol y 45 min de gimnasio; dormí 8h','localDate':'2026-10-17'})
    assert interpretation.ok and len(interpretation.json()['records'])==3, interpretation.text
    answer=requests.post('http://127.0.0.1:4173/api/chat',json={'message':'¿Cómo llevo la carga?','context':{'summaries':{'load7':525}}})
    assert answer.ok and 'carga' in answer.json()['answer'], answer.text
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
        ctx=browser.new_context(viewport={'width':1365,'height':945},accept_downloads=True)
        page=ctx.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(inline_html(r"""() => {
          const map = {};
          Object.defineProperty(window, 'localStorage', { configurable:true, value:{
            getItem:k=>map[k]??null, setItem:(k,v)=>{map[k]=v}, removeItem:k=>{delete map[k]}
          }});
          window.fetch = async (url,opts={}) => {
            const u=String(url);
            if(u.endsWith('/api/health'))return {ok:true,json:async()=>({aiEnabled:true,transcriptionEnabled:true})};
            if(u.endsWith('/api/transcribe'))return {ok:true,json:async()=>({text:'Hoy he hecho 75 minutos de fútbol, RPE 7, 45 minutos de gimnasio y he dormido 8 horas.'})};
            if(u.endsWith('/api/interpret')){if(JSON.parse(opts.body||'{}').message.startsWith('¿'))return {ok:true,json:async()=>({records:[]})};return {ok:true,json:async()=>({records:[
                {kind:'session',data:{date:'2026-10-17',type:'team',duration:75,rpe:7,title:'Equipo'},missing:[]},
                {kind:'session',data:{date:'2026-10-17',type:'gym',duration:45,title:'Gimnasio'},missing:['RPE del gimnasio']},
                {kind:'checkin',data:{date:'2026-10-17',sleepHours:8},missing:['Energía']}
            ]})}};
            if(u.endsWith('/api/chat'))return {ok:true,json:async()=>({answer:'Los cálculos proceden de tus registros confirmados.'})};
            throw Error('Unknown mock URL '+u);
          };
          window.MediaRecorder = class {
            static isTypeSupported(){return true}
            constructor(stream,options){this.state='inactive';this.mimeType=options?.mimeType||'audio/webm'}
            start(){this.state='recording'}
            stop(){this.state='inactive';this.ondataavailable?.({data:new Blob(['demo'],{type:'audio/webm'})});this.onstop?.()}
          };
          Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:async()=>({getTracks:()=>[{stop(){}}]})}});
        }"""),wait_until='domcontentloaded',timeout=10000)
        page.get_by_role('button',name='Asistente IA').first.click()
        page.wait_for_function('document.querySelector(".btn-voice") && !document.querySelector(".btn-voice").disabled', timeout=5000)
        assert page.get_by_text('Adjuntar audio').count() == 1
        page.locator('#chat-audio-file').set_input_files({'name':'nota.webm','mimeType':'audio/webm','buffer':b'fake audio body'})
        page.wait_for_function("document.querySelector('#chat-input').value.includes('75 minutos')",timeout=15000)
        assert page.locator('#chat-messages .bubble').count()==1, 'Transcription must not save/send automatically'
        # Simulate voice recording and verify that stopping also puts text in the composer.
        page.locator('#chat-input').fill('')
        page.locator('[data-action=voice-start]').click()
        assert 'Grabando' in page.locator('#voice-status').inner_text()
        page.locator('[data-action=voice-stop]').click()
        page.wait_for_function("document.querySelector('#chat-input').value.includes('75 minutos')",timeout=5000)
        page.locator('#chat-input').press('Enter')
        page.wait_for_function("document.querySelectorAll('[data-action=review-draft]').length === 3",timeout=15000)
        print('MULTI DRAFTS',page.locator('[data-action=review-draft]').count())
        page.locator('[data-action=review-draft]').nth(0).click()
        assert page.locator('#session-form').count()==1
        assert page.locator('#duration').input_value()=='75'
        assert page.locator('#rpe').input_value()=='7'
        page.locator('#session-form button[type=submit]').click()
        page.wait_for_timeout(300)
        assert page.locator('[data-action=review-draft]').count()==2, 'The confirmed draft should disappear'
        page.get_by_role('button',name='Mi panel').first.click()
        assert '525' in page.locator('.stat-number').first.inner_text(), '75×7=525 UA'
        page.get_by_role('button',name='Asistente IA').first.click()
        page.locator('#chat-input').fill('¿Qué carga llevo esta semana?')
        page.locator('#chat-input').press('Enter')
        page.wait_for_timeout(600)
        print('LAST REPLY',page.locator('.bubble').last.inner_text()[:150])
        assert not errors, errors
        page.screenshot(path='/mnt/data/PerformFootball_v02_IA.png',full_page=True)
        print('START MOBILE', flush=True)
        mob=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
        mob.on('pageerror',lambda e:errors.append(str(e)))
        print('MOBILE CONTENT', flush=True)
        mob.set_content(inline_html("""() => {const map={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>map[k]??null,setItem:(k,v)=>map[k]=v}});window.fetch=async()=>({ok:true,json:async()=>({aiEnabled:true})});}"""),wait_until='domcontentloaded',timeout=10000)
        print('MOBILE CLICK',flush=True)
        mob.locator('.mobile-tab[data-page=assistant]').click()
        mob.wait_for_function('document.querySelector(".btn-voice") && !document.querySelector(".btn-voice").disabled',timeout=5000)
        assert not mob.evaluate('document.documentElement.scrollWidth > innerWidth'), 'Mobile page has horizontal overflow'
        print('MOBILE SCREEN',flush=True)
        mob.screenshot(path='/mnt/data/PerformFootball_v02_movil.png',full_page=True)
        assert not errors, errors
        print('TESTS PASSED',FakeOpenAI.calls)
        print('CLOSING',flush=True)
        browser.close()
finally:
    server.terminate(); server.wait(timeout=5);fake.shutdown()
