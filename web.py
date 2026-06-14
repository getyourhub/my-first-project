#!/usr/bin/env python3
"""Web UI for Subtitles Translator"""
import os
import tempfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import sys

sys.path.insert(0, os.path.dirname(__file__))

from subtitle_parser import parse_subtitle_file
from translator import get_translator

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

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
        flash('没有选择文件')
        return redirect(url_for('index'))

    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        flash('没有选择文件')
        return redirect(url_for('index'))

    translator_type = request.form.get('translator', 'google')
    api_key = request.form.get('api_key', '')
    source_lang = request.form.get('source_lang', 'auto')
    target_lang = request.form.get('target_lang', 'zh-cn')
    bilingual = request.form.get('bilingual', 'on') == 'on'
    model = request.form.get('model', '')

    try:
        translator = get_translator(translator_type, api_key or None, source_lang, target_lang, model=model or None)
    except Exception as e:
        flash(f'翻译器初始化失败: {e}')
        return redirect(url_for('index'))

    results = []
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(input_path)

                subtitles = parse_subtitle_file(input_path)
                translated_subtitles = translator.translate_subtitles(subtitles)

                Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
                stem = Path(filename).stem
                suffix = Path(filename).suffix
                output_filename = f"{stem}_bilingual_{target_lang}{suffix}"
                output_path = os.path.join(OUTPUT_FOLDER, output_filename)

                from main import save_translated_subtitles
                save_translated_subtitles(input_path, translated_subtitles, output_path, bilingual)

                results.append({
                    'original': filename,
                    'output': output_filename,
                    'path': output_path
                })

                os.remove(input_path)

            except Exception as e:
                errors.append(f"{file.filename}: {e}")
        else:
            if file.filename:
                errors.append(f"{file.filename}: 不支持的文件格式")

    return render_template('results.html', results=results, errors=errors)


@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    flash('文件不存在')
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)