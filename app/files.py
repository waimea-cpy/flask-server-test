import os
import click
from flask import current_app
from werkzeug.utils import secure_filename


#-------------------------------------------
# Save an uploaded file to the uploads folder
def save_file(the_file):
    filename = secure_filename(the_file.filename)
    the_file.save(os.path.join(current_app.config['UPLOADS'], filename))
    return filename


#-------------------------------------------
# Delete a given file from the uploads folder
def delete_file(filename):
    uploads = current_app.config['UPLOADS']
    file_path = os.path.join(uploads, filename)
    os.remove(file_path)


#-------------------------------------------
# Register 'flask init-files' command and
def init_app(app):
    app.cli.add_command(init_files_command)


#-------------------------------------------
# Respond to the 'flask init-files' command
@click.command('init-files')
def init_files_command():
    '''Empty the uploads folder'''
    uploads = current_app.config['UPLOADS']
    for filename in os.listdir(uploads):
        file_path = os.path.join(uploads, filename)
        os.remove(file_path)
    click.echo('Uploads cleared')


