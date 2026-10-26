"""Render a 60s explanatory video from saved real CLI stdout, not a screen recording.

Requires Pillow and imageio-ffmpeg. Input demo/cli_transcript.json is captured
separately from actual local CLI executions. No LLM or GUI outputs are invented.
"""
import argparse
import json
from pathlib import Path
import subprocess
import textwrap


def main():
    from PIL import Image, ImageDraw, ImageFont
    import imageio_ffmpeg
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--frames", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = json.loads((args.root/"demo/cli_transcript.json").read_text(encoding="utf-8"))
    args.frames.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    font_path = "C:/Windows/Fonts/consola.ttf"
    title_font = ImageFont.truetype(font_path, 32)
    small = ImageFont.truetype(font_path, 18)
    slides = [(r["title"], "$ "+r["display_command"]+"\n\n"+
               json.dumps(json.loads(r["stdout"]),ensure_ascii=False,indent=2)+
               f"\n\nÇıkış kodu: {r['exit_code']}") for r in records]
    audit = json.loads((args.root/"tests/reports/final60_audit.json").read_text(encoding="utf-8"))
    slides.append(("Kanıt ve kapsam", "G*Power değildir; eğitim amaçlı bağımsız uygulama.\n\n"
        f"Sude'nin sözleşmeyle uyumlu kayıtları: {audit['source_protocol_passed']}/58\n"
        f"A-priori N tam eşleşmesi: {audit['a_priori_n_exact']}/38\n"
        "Bu set geliştirmede kullanıldı; gizli sınav sonucu değildir.\n\n"
        "CLI-MCP eşdeğerliği: 25 açık + 8 hata girdisi.\n"
        "Canlı LLM sağlayıcı koşumu: yapılmadı.\n"
        "REA adresleri ve dosya hash'i rapor paketinde.\n\n"
        "Bu video gerçek CLI çıktılarının görsel anlatımıdır.\n"
        "Terminal veya G*Power ekran kaydı değildir."))
    if len(slides) != 6:
        raise ValueError("Demo requires exactly five recorded command stages")
    paths = []
    for index, (title, body) in enumerate(slides,1):
        canvas = Image.new("RGB", (1280,720), "#101a29")
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((34,28,1246,692), radius=16, fill="#162235", outline="#38506e", width=2)
        draw.text((62,49),f"GPOWER CLONE   {index}/6",font=small,fill="#74dbc5")
        draw.text((62,85),title,font=title_font,fill="#f5f7fb")
        for size in range(24,15,-1):
            font = ImageFont.truetype(font_path,size)
            width = int(1140 / draw.textlength("M",font=font))
            lines = []
            for line in body.splitlines():
                lines.extend(textwrap.wrap(line,width=width,replace_whitespace=False,drop_whitespace=False) or [""])
            if len(lines)*(size+5) <= 476:
                break
        else:
            raise ValueError("Demo text exceeds visible layout")
        y = 143
        for line in lines:
            draw.text((64,y),line,font=font,fill="#edf2fb")
            y += size+5
        draw.text((64,650),"Gerçek çıktıların görsel anlatımı  |  Ekran kaydı değil  |  Yerel inceleme",font=small,fill="#a7b8ce")
        path = (args.frames/f"frame-{index}.png").resolve()
        canvas.save(path)
        paths.append(path)
    listing = args.frames/"concat.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\nduration 10\n" for p in paths)+f"file '{paths[-1].as_posix()}'\n",encoding="utf-8")
    command = [imageio_ffmpeg.get_ffmpeg_exe(),"-y","-f","concat","-safe","0","-i",str(listing),
        "-vf","fps=24,format=yuv420p","-t","60","-c:v","libx264","-preset","veryfast","-crf","20",
        "-movflags","+faststart",str(args.output)]
    result = subprocess.run(command,capture_output=True,text=True,check=True)
    (args.frames/"ffmpeg.log").write_text(result.stderr,encoding="utf-8")
    print(json.dumps({"output":str(args.output),"seconds":60,"frames":len(paths),"screen_recording":False}))


if __name__ == "__main__":
    main()
