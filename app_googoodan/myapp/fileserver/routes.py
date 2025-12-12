from flask import render_template, request, send_file, flash, redirect, url_for
from . import fileserver_bp
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

@fileserver_bp.route('/fileserver', methods=['GET', 'POST'])
def fileserver():
    if request.method == 'POST':
        file = request.files['file']
        file.save(f"{ABS_PATH}/upload/{file.filename}")
        flash("파일 업로드 성공")
    file_names = os.listdir(f"{ABS_PATH}/upload")
    files = []
    for file_name in file_names:
        file_path = os.path.join(f"{ABS_PATH}/upload", file_name)
        file_size_bytes = os.path.getsize(file_path)
        def convert_bytes_to_human_readable(size_bytes):
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.2f} PB"
        file_size = convert_bytes_to_human_readable(file_size_bytes)

        import datetime
        file_created_at_timestamp = os.path.getctime(file_path)
        file_updated_at_timestamp = os.path.getmtime(file_path)
        file_created_at = datetime.datetime.fromtimestamp(file_created_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        file_updated_at = datetime.datetime.fromtimestamp(file_updated_at_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        files.append({
            'name': file_name,
            'size': file_size,
            'created_at': file_created_at,
            'updated_at': file_updated_at
        })
    return render_template('fileserver/fileserver.html', files=files)

@fileserver_bp.route('/download/<filename>', methods=['GET'])
def download(filename):
    flash("파일 다운로드 성공")
    return send_file(f"{ABS_PATH}/upload/{filename}", as_attachment=True)

@fileserver_bp.route('/delete/<filename>', methods=['GET'])
def delete(filename):
    os.remove(f"{ABS_PATH}/upload/{filename}")
    flash("파일 삭제 성공")
    return redirect(url_for('fileserver.fileserver'))