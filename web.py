#!/usr/bin/env python3
"""Web UI for Subtitles Translator with real-time progress"""
import os
import json
import time
from pathlib import Path
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, Response, stream_with_context
from werkzeug.utils import secure_filename
import sys

sys.path.insert(0, os.path.dirname(__file__))

from subtitle_parser import parse_subtitle_file
from translator import get_translator, LLM_PROVIDERS

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

UPLOAD_FOLDER = '/tmp/subtitles_uploads'
OUTPUT_FOLDER = '/tmp/subtitles_output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'srt', 'ass'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    if 'files' not in request.files:
        flash('没有选择文件 / No file selected')
        return redirect(url_for('index'))

    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        flash('没有选择文件 / No file selected')
        return redirect(url_for('index'))

    file_list = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(input_path)
            file_list.append({'name': filename, 'path': input_path})

    if not file_list:
        flash('没有有效的字幕文件 / No valid subtitle files')
        return redirect(url_for('index'))

    translator_type = request.form.get('translator', 'google')
    api_key = request.form.get('api_key', '')
    source_lang = request.form.get('source_lang', 'auto')
    target_lang = request.form.get('target_lang', 'zh-cn')
    bilingual = request.form.get('bilingual', 'on') == 'on'
    model = request.form.get('model', '')

    return render_template('progress.html',
                          files=file_list,
                          translator=translator_type,
                          api_key=api_key,
                          source_lang=source_lang,
                          target_lang=target_lang,
                          bilingual=bilingual,
                          model=model)


@app.route('/stream_translate')
def stream_translate():
    files_json = request.args.get('files', '[]')
    translator_type = request.args.get('translator', 'google')
    api_key = request.args.get('api_key', '')
    source_lang = request.args.get('source_lang', 'auto')
    target_lang = request.args.get('target_lang', 'zh-cn')
    bilingual = request.args.get('bilingual', 'true') == 'true'
    model = request.args.get('model', '')

    files = json.loads(files_json)

    try:
        translator = get_translator(translator_type, api_key or None, source_lang, target_lang, model=model or None)
    except Exception as e:
        def error_stream():
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        return Response(stream_with_context(error_stream()), mimetype='text/event-stream')

    def generate():
        results = []
        errors = []
        total_files = len(files)
        start_time = time.time()

        for file_idx, file_info in enumerate(files, 1):
            filename = file_info['name']
            input_path = file_info['path']

            yield f"data: {json.dumps({'type': 'file_start', 'file': filename, 'file_num': file_idx, 'total_files': total_files})}\n\n"

            try:
                subtitles = parse_subtitle_file(input_path)
                total_subs = len(subtitles)

                yield f"data: {json.dumps({'type': 'file_info', 'file': filename, 'subtitle_count': total_subs})}\n\n"

                translated_subtitles = []
                for i, sub in enumerate(subtitles, 1):
                    original_text = sub.original
                    translated_text = translator.translate_text(original_text)
                    sub.translated = translated_text
                    translated_subtitles.append(sub)

                    progress = int(i / total_subs * 100)
                    yield f"data: {json.dumps({'type': 'progress', 'file': filename, 'current': i, 'total': total_subs, 'progress': progress, 'original': original_text[:50], 'translated': translated_text[:50]})}\n\n"

                    if i < total_subs:
                        time.sleep(0.05)

                stem = Path(filename).stem
                suffix = Path(filename).suffix
                output_filename = f"{stem}_bilingual_{target_lang}{suffix}"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                from main import save_translated_subtitles
                save_translated_subtitles(input_path, translated_subtitles, output_path, bilingual)

                result = {
                    'original': filename,
                    'output': output_filename,
                    'subtitle_count': total_subs,
                    'status': 'success'
                }
                results.append(result)

                yield f"data: {json.dumps({'type': 'file_complete', 'file': filename, 'output': output_filename, 'download_url': f'/download/{output_filename}'})}\n\n"

                os.remove(input_path)

            except Exception as e:
                errors.append({'file': filename, 'error': str(e)})
                yield f"data: {json.dumps({'type': 'file_error', 'file': filename, 'error': str(e)})}\n\n"

        elapsed = time.time() - start_time
        yield f"data: {json.dumps({'type': 'complete', 'results': results, 'errors': errors, 'elapsed': round(elapsed, 1), 'total_files': total_files, 'success_count': len(results), 'error_count': len(errors)})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    flash('文件不存在 / File not found')
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)