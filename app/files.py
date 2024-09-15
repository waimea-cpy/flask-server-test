'''
FILE SYSTEM RELATED FUNCTIONS
- Uploading files
- Deleting uploaded files
- Retrieving uploaded files
- Initialising uploads folder
'''

import os
import click
from flask import current_app
from flask import send_from_directory
from werkzeug.utils import secure_filename


#-------------------------------------------------------
def uploads_path():
    '''
    Build the path to the defined uploads folder
    '''
    return os.path.join(
        current_app.root_path,
        current_app.config['UPLOADS_DIR']
    )


#-------------------------------------------------------
def init_files():
    '''
    Clear out all files in the uploads folder
    '''
    uploads = uploads_path()
    # Iterate through the folder
    for filename in os.listdir(uploads):
        # Deleting the files
        os.remove(os.path.join(uploads, filename))


#-------------------------------------------------------
def save_file(the_file):
    '''
    Save an uploaded file to the uploads folder
    '''
    # Deal with any dodgy files names
    filename = secure_filename(the_file.filename)
    # Save the file into the uploads folder
    the_file.save(os.path.join(uploads_path(), filename))
    # Pass back the cleaned-up filename
    return filename


#-------------------------------------------------------
def delete_file(filename):
    '''
    Delete a given file from the uploads folder
    '''
    os.remove(os.path.join(uploads_path(), filename))


#-------------------------------------------------------
def get_file(filename):
    '''
    Return a given file from the uploads folder
    '''
    return send_from_directory(uploads_path(), filename)

#-------------------------------------------------------
def init_app(app):
    '''
    Register 'flask init-files' command
    '''
    app.cli.add_command(init_files_command)


#-------------------------------------------------------
@click.command('init-files')

def init_files_command():
    '''
    Delete all files in the uploads folder.
    '''
    init_files()
    click.echo('Uploads cleared')


