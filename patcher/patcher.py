"""Hash-checked, offline Korean patch installer. Original ISO is read-only."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading

VERSION = '1.1'

def sha256(path, progress=lambda *_: None, start=0, span=0):
    total=path.stat().st_size; done=0; digest=hashlib.sha256()
    with path.open('rb') as stream:
        while data:=stream.read(8*1024*1024):
            digest.update(data);done+=len(data)
            progress(None,start+span*done/max(1,total))
    return digest.hexdigest()

def install(source, output, package, progress=lambda *_: None, decoder=None):
    source=Path(source).resolve(strict=True);output=Path(output).resolve();package=Path(package).resolve()
    manifest=json.loads((package/'patch-manifest.json').read_text(encoding='utf-8-sig'))
    if manifest['version']!=VERSION:raise ValueError('패치 버전이 적용 도구와 다릅니다.')
    if source==output:raise ValueError('원본 ISO와 출력 파일은 다른 경로여야 합니다.')
    if output.exists():raise FileExistsError('출력 파일이 이미 있습니다. 새 파일 이름을 지정하세요.')
    if not output.parent.is_dir():raise FileNotFoundError('출력 폴더가 없습니다.')
    if shutil.disk_usage(output.parent).free<manifest['output']['bytes']+64*1024*1024:
        raise OSError('출력 드라이브에 약 3GB의 빈 공간을 확보해 주세요.')
    patch_name=manifest['patch']['file']
    if Path(patch_name).name!=patch_name:raise ValueError('올바르지 않은 패치 파일 이름입니다.')
    patch=package/patch_name
    progress('일본판 원본 ISO를 확인하고 있습니다.',0)
    if source.stat().st_size!=manifest['source']['bytes'] or sha256(source,progress,0,20)!=manifest['source']['sha256']:
        raise ValueError('지원하는 일본판 원본 ISO가 아닙니다. README의 크기와 SHA-256을 확인하세요.')
    progress('패치 파일의 SHA-256을 확인하고 있습니다.',20)
    if patch.stat().st_size!=manifest['patch']['bytes'] or sha256(patch,progress,20,10)!=manifest['patch']['sha256']:
        raise ValueError('패치 파일이 손상됐거나 다른 버전입니다. 릴리스 압축 파일을 다시 받으세요.')
    if decoder is None:
        decoder=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))/'runtime/xdelta3.exe'
    decoder=Path(decoder).resolve(strict=True)
    tmp=None
    try:
        handle=tempfile.NamedTemporaryFile(prefix=output.name+'.',suffix='.partial',dir=output.parent,delete=False)
        tmp=Path(handle.name);handle.close()
        progress('한글 ISO를 만들고 있습니다. 창을 닫지 마세요.',None)
        result=subprocess.run([str(decoder),'-d','-f','-D','-R','-s',str(source),str(patch),str(tmp)],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if result.returncode:
            detail=result.stderr.decode('utf-8',errors='replace').strip()[-1800:]
            raise RuntimeError(f'패치 적용에 실패했습니다.\n{detail}')
        progress('완성된 ISO의 SHA-256을 확인하고 있습니다.',80)
        actual=sha256(tmp,progress,80,20)
        if tmp.stat().st_size!=manifest['output']['bytes'] or actual!=manifest['output']['sha256']:
            raise ValueError('출력 ISO의 검증값이 다릅니다. 불완전한 파일은 확정하지 않습니다.')
        if os.name=='nt':os.rename(tmp,output)  # Windows rename rejects an existing destination.
        else:
            os.link(tmp,output)  # Also reject a destination created during decoding.
            tmp.unlink()
        tmp=None
        receipt=dict(version=VERSION,success=True,output=str(output),bytes=output.stat().st_size,
            sha256=actual,original_opened_read_only=True)
        progress('완료했습니다.',100)
        return receipt
    finally:
        if tmp is not None and tmp.exists():tmp.unlink()

def gui():
    import tkinter as tk
    from tkinter import ttk,filedialog,messagebox
    base=Path(sys.executable).resolve().parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parent
    root=tk.Tk();root.title(f'내일의 죠 한글 패치 v{VERSION}');root.geometry('700x350');root.minsize(650,350)
    style=ttk.Style(root)
    if 'vista' in style.theme_names():style.theme_use('vista')
    outer=ttk.Frame(root,padding=22);outer.pack(fill='both',expand=True)
    ttk.Label(outer,text='내일의 죠 — 하얗게 불태워라!',font=('Malgun Gothic',17,'bold')).pack(anchor='w')
    ttk.Label(outer,text=f'일본판 SLPM-65441 · 비공식 한글화 정식버전 v{VERSION}',padding=(0,6,0,12)).pack(anchor='w')
    source=tk.StringVar();output=tk.StringVar();status=tk.StringVar(value='원본 ISO를 선택하면 해시를 확인한 뒤 별도의 한글 ISO를 만듭니다.')
    form=ttk.Frame(outer);form.pack(fill='x');form.columnconfigure(1,weight=1)
    def pick_source():
        chosen=filedialog.askopenfilename(title='일본판 원본 ISO 선택',filetypes=[('ISO 이미지','*.iso'),('모든 파일','*.*')])
        if chosen:
            source.set(chosen)
            if not output.get():output.set(str(Path(chosen).parent/f'Ashita-no-Joe-Kr-v{VERSION}.iso'))
    def pick_output():
        chosen=filedialog.asksaveasfilename(title='한글 ISO 저장 위치',defaultextension='.iso',initialfile=f'Ashita-no-Joe-Kr-v{VERSION}.iso',filetypes=[('ISO 이미지','*.iso')])
        if chosen:output.set(chosen)
    for i,(label,var,command) in enumerate([('원본 ISO',source,pick_source),('한글 ISO',output,pick_output)]):
        ttk.Label(form,text=label,width=10).grid(row=i,column=0,sticky='w',pady=6)
        ttk.Entry(form,textvariable=var).grid(row=i,column=1,sticky='ew',padx=(0,8),pady=6)
        ttk.Button(form,text='찾아보기',command=command).grid(row=i,column=2,pady=6)
    bar=ttk.Progressbar(outer,maximum=100);bar.pack(fill='x',pady=(18,8))
    ttk.Label(outer,textvariable=status,wraplength=630).pack(anchor='w')
    busy=False;events=queue.Queue();button=ttk.Button(outer,text='한글 패치 적용');button.pack(anchor='e',pady=(14,0))
    def worker(src,dst):
        try:events.put(('done',install(src,dst,base,lambda msg,n:events.put(('progress',(msg,n))))))
        except Exception as exc:events.put(('error',str(exc)))
    def begin():
        nonlocal busy
        if not source.get() or not output.get():messagebox.showinfo('파일 선택','원본 ISO와 한글 ISO 저장 위치를 선택하세요.');return
        busy=True;button.configure(state='disabled')
        threading.Thread(target=worker,args=(source.get(),output.get()),daemon=True).start()
    button.configure(command=begin)
    def poll():
        nonlocal busy
        try:
            while True:
                kind,value=events.get_nowait()
                if kind=='progress':
                    msg,n=value
                    if msg:status.set(msg)
                    if n is None:
                        if msg:bar.configure(mode='indeterminate');bar.start(12)
                    else:bar.stop();bar.configure(mode='determinate',value=n)
                else:
                    bar.stop();busy=False;button.configure(state='normal')
                    if kind=='done':
                        bar.configure(mode='determinate',value=100);status.set('완료: '+value['output'])
                        messagebox.showinfo('한글 패치 완료','한글 ISO를 만들고 SHA-256 검증을 마쳤습니다.\n\n'+value['output'])
                    else:status.set('실패: '+value);messagebox.showerror('패치 적용 실패',value)
        except queue.Empty:pass
        root.after(100,poll)
    def close():
        if busy:messagebox.showinfo('패치 적용 중','파일 검증과 패치가 끝날 때까지 기다려 주세요.');return
        root.destroy()
    root.protocol('WM_DELETE_WINDOW',close);root.after(100,poll);root.mainloop()

def main():
    parser=argparse.ArgumentParser(description='Ashita no Joe Korean patch installer')
    parser.add_argument('--source',type=Path);parser.add_argument('--output',type=Path)
    parser.add_argument('--package',type=Path);parser.add_argument('--decoder',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    if args.source is None and args.output is None:gui();return 0
    if args.source is None or args.output is None:parser.error('--source and --output must be used together')
    base=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).parent
    try:report=install(args.source,args.output,args.package or base,decoder=args.decoder);code=0
    except Exception as exc:report=dict(version=VERSION,success=False,error=str(exc));code=1
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if sys.stdout is not None:print(json.dumps(report,ensure_ascii=False))
    return code

if __name__=='__main__':raise SystemExit(main())
