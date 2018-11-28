# -*- coding: utf-8 -*-
"""The 'fwp_save' module saves data, dealing with overwriting.

It could be divided into 2 sections:
    (1) making new directories and free files to avoid overwriting 
    ('new_dir', 'free_file')
    (2) saving data into files with the option of not overwriting 
    ('saveplot', 'savetext', 'savewav')

new_dir : function
    Makes and returns a new related directory to avoid overwriting.
free_file : function
    Returns a name for a new file to avoid overwriting.
new_name : function
    Returns a unique name with input name as template.
saveplot : function
    Saves a matplotlib.pyplot plot on an image file (i.e: 'png').
savetxt : function
    Saves some np.array like data on a '.txt' file.
savewav : function
    Saves a PyAudio encoded audio on a '.wav' file.
saveanimation : function
    Saves a matplotlib.animation object as '.gif' or '.mp4'.

@author: Vall
@date: 09-17-2018
"""

import fwp_string as fst
import matplotlib.pyplot as plt
import numpy as np
import os
#import pyaudio
#import wave

#%%

def new_dir(my_dir, newformat='{}_{}'):
    
    """Makes and returns a new directory to avoid overwriting.
    
    Takes a directory name 'my_dir' and checks whether it already 
    exists. If it doesn't, it returns 'dirname'. If it does, it 
    returns a related unoccupied directory name. In both cases, 
    the returned directory is initialized.
    
    Parameters
    ----------
    my_dir : str
        Desired directory (should also contain full path).
    
    Returns
    -------
    new_dir : str
        New directory (contains full path)
    
    Yields
    ------
    new_dir : directory
    
    """
    
    sepformat = newformat.split('{}')
    base = os.path.split(my_dir)[0]
    
    new_dir = my_dir
    while os.path.isdir(new_dir):
        new_dir = os.path.basename(new_dir)
        new_dir = new_dir.split(sepformat[-2])[-1]
        try:
            new_dir = new_dir.split(sepformat[-1])[0]
        except ValueError:
            new_dir = new_dir
        try:
            new_dir = newformat.format(my_dir, str(int(new_dir)+1))
        except ValueError:
            new_dir = newformat.format(my_dir, 2)
        new_dir = os.path.join(base, new_dir)
    os.makedirs(new_dir)
        
    return new_dir

#%%

def free_file(my_file, newformat='{}_{}'):
    
    """Returns a name for a new file to avoid overwriting.
        
    Takes a file name 'my_file'. It returns a related unnocupied 
    file name 'free_file'. If necessary, it makes a new 
    directory to agree with 'my_file' path.
        
    Parameters
    ----------
    my_file : str
        Tentative file name (must contain full path and extension).
    newformat='{}_{}' : str
        Format string that indicates how to make new names.
    
    Returns
    -------
    new_fname : str
        Unoccupied file name (also contains full path and extension).
    
    """
    
    base = os.path.split(my_file)[0]
    extension = os.path.splitext(my_file)[-1]
    
    if not os.path.isdir(base):
        os.makedirs(base)
        free_file = my_file
    
    else:
        sepformat = newformat.split('{}')[-2]
        free_file = my_file
        while os.path.isfile(free_file):
            free_file = os.path.splitext(free_file)[0]
            free_file = free_file.split(sepformat)
            number = free_file[-1]
            free_file = free_file[0]
            try:
                free_file = newformat.format(
                        free_file,
                        str(int(number)+1),
                        )
            except ValueError:
                free_file = newformat.format(
                        os.path.splitext(my_file)[0], 
                        2)
            free_file = os.path.join(base, free_file+extension)
    
    return free_file

#%%
    
def new_name(name, newseparator='_'):
    '''Returns a name of a unique file or directory so as to not overwrite.
    
    If proposed name existed, will return name + newseparator + number.
     
    Parameters:
    -----------
        name : str (path)
            proposed file or directory name influding file extension
        nweseparator : str
            separator between original name and index that gives unique name
            
    Returns:
    --------
        name : str
            unique namefile using input 'name' as template
    '''
    
    #if file is a directory, extension will be empty
    base, extension = os.path.splitext(name)
    i = 2
    while os.path.exists(name):
        name = base + newseparator + str(i) + extension
        i += 1
        
    return name

#%%

def saveplot(file, overwrite=False):
    
    """Saves a plot on an image file.
    
    This function saves the current matplotlib.pyplot plot on a file. 
    If 'overwrite=False', it checks whether 'file' exists or not; if it 
    already exists, it defines a new file in order to not allow 
    overwritting. If overwrite=True, it saves the plot on 'file' even if 
    it already exists.
    
    Variables
    ---------
    file : string
        The name you wish (must include full path and extension)
    overwrite=False : bool
        Indicates whether to overwrite or not.
    
    Returns
    -------
    nothing
    
    Yields
    ------
    an image file
    
    See Also
    --------
    free_file()
    
    """
    
    if not os.path.isdir(os.path.split(file)[0]):
        os.makedirs(os.path.split(file)[0])
    
    if not overwrite:
        file = free_file(file)

    plt.savefig(file, bbox_inches='tight')
    
    print('Archivo guardado en {}'.format(file))
    

#%%

def savetxt(file, datanumpylike, overwrite=False, header='', footer=''):
    
    """Takes some array-like data and saves it on a '.txt' file.
    
    This function takes some data and saves it on a '.txt' file.
    If 'overwrite=False', it checks whether 'file' exists or not; if it 
    already exists, it defines a new file in order to not allow 
    overwritting. If overwrite=True, it saves the plot on 'file' even if 
    it already exists.
    
    Variables
    ---------
    file : string
        The name you wish (must include full path and extension)
    datanumpylike : array, list
        The data to be saved.
    overwrite=False : bool, optional
        Indicates whether to overwrite or not.
    header='' : list, str, optional
        Data's descriptor. Its elements should be str, one per column.
        But header could also be a single string.
    footer='' : dict, str, optional
        Data's specifications. Its elements and keys should be str. 
        But footer could also be a single string. Otherwise, an element 
        could be a tuple containing value and units; i.e.: (100, 'Hz').
    
    Return
    ------
    nothing
    
    Yield
    -----
    '.txt' file
    
    See Also
    --------
    free_file()
    
    """
    
    base = os.path.split(file)[0]
    if not os.path.isdir(base):
        os.makedirs(base)
    
    if header != '':
        if not isinstance(header, str):
            try:
                header = '\t'.join(header)
            except:
                TypeError('Header should be a list or a string')

    if footer != '':
        if not isinstance(footer, str):
            try:
                aux = []
                for key, value in footer.items():
                    if isinstance(value, tuple) and len(value) == 2:
                        condition = isinstance(value[0], str)
                        if not condition and isinstance(value[1], str):
                            value = '"{} {}"'.format(*value)
                    elif isinstance(value, str):
                        value = '"{}"'.format(value)
                    aux.append('{}={}'.format(key, value) + ', ')
                footer = ''.join(aux)
            except:
                TypeError('Header should be a dict or a string')

    file = os.path.join(
            base,
            (os.path.splitext(os.path.basename(file))[0] + '.txt'),
            )
    
    if not overwrite:
        file = free_file(file)
        
    np.savetxt(file, np.array(datanumpylike), 
               delimiter='\t', newline='\n', header=header, footer=footer)
    
    print('Archivo guardado en {}'.format(file))
    
    return

#%%
#
#def savewav(file,
#            datapyaudio,
#            data_nchannels=1,
#            data_format=pyaudio.paFloat32,
#            data_samplerate=44100,
#            overwrite=False):
#    
#    """Takes a PyAudio byte stream and saves it on a '.wav' file.
#    
#    Takes a PyAudio byte stream and saves it on a '.wav' file. It 
#    specifies some parameters: 'datanchannels' (number of audio 
#    channels), 'dataformat' (format of the audio data), and 'samplerate' 
#    (sampling rate of the data). If 'overwrite=False', it checks whether 
#    'file' exists or not; if it already exists, it defines a new file in 
#    order to not allow overwritting. If overwrite=True, it saves the 
#    plot on 'file' even if it already exists.
#    
#    Variables
#    ---------
#    file : str
#        Desired file (must include full path and extension)
#    datapyaudio : str
#        PyAudio byte stream.
#    data_nchannels=1 : int
#        Data's number of audio channels.
#    data_format : int
#        Data's PyAudio format.
#    overwrite=False : bool
#        Indicates wheter to overwrite or not.
#        
#    Returns
#    -------
#    nothing
#    
#    Yields
#    ------
#    '.wav' file
#    
#    See Also
#    --------
#    free_file()
#    
#    """
#    
#    base = os.path.split(file)[0]
#    if not os.path.isdir(base):
#        os.makedirs(base)
#
#    file = os.path.join(
#            base,
#            (os.path.splitext(os.path.basename(file))[0] + '.wav'),
#            )
#    
#    if not overwrite:
#        file = free_file(file)
#    
#    datalist = []
#    datalist.append(datapyaudio)
#    
#    p = pyaudio.PyAudio()
#    wf = wave.open(file, 'wb')
#    
#    wf.setnchannels(data_nchannels)
#    wf.setsampwidth(p.get_sample_size(data_format))
#    wf.setframerate(data_samplerate)
#    wf.writeframes(b''.join(datalist))
#    
#    wf.close()
#    
#    print('Archivo guardado en {}'.format(file))
#    
#    return

#%%

def saveanimation(file,
                  animation,
                  frames_per_second=30,
                  overwrite=False):
    
    """Saves a matplotlib.animation object as '.gif' or '.mp4'.
    
    Variables
    ---------
    file : str
        Desired file (must include full path and extension).
    animation : matplotlib.animation object
        Animation to save.
    frames_per_second=30 : int
        Animation's frames per second.
    overwrite=False : bool
        Indicates wheter to overwrite or not.
        
    Returns
    -------
    nothing
    
    Yields
    ------
    video file
    
    Warnings
    --------
    To save '.gif' you must have ImageMagick installed.
    To save '.mp4' you must have FFPG installed.
    
    See Also
    --------
    free_file()
    fwp_plot.animation_2D()
    
    """
    
    if not os.path.isdir(os.path.split(file)[0]):
        os.makedirs(os.path.split(file)[0])
    
    if not overwrite:
        file = free_file(file)
    
    extension = os.path.splitext(file)[-1]
    
    if extension == '.mp4':
        animation.save(file,
                       extra_args=['-vcodec', 'libx264'])
    elif extension == '.gif':
        animation.save(file,
                       dpi=50,
                       writer='imagemagick')    
    
    print('Archivo guardado en {}'.format(file))
    
    return

#%%

def savefile_helper(folder, 
                    filename_template, 
                    parent_folder='Measurements', 
                    parent_folder_in_cwd=True):
    
    """Defines a function that creates filenames from a template.
    
    Parameters
    ----------
    folder :  str
        Directory of the folder where you'll create files.
    filename_template : str
        Function that makes only filenames (file's name with 
        termination) from a series of arguments.
    parent_folder='Measurements', optional
        Directory of a folder that will contain 'folder'.
    parent_folder_in_cwd=True : bool, optional
        Indicates whether 'parent_folder' is in the current working 
        directory or not. If it isn't, then 'parent_folder' should be a 
        full global directory.
    
    Returns
    -------
    filename_maker : function
        Function that returns a filename (including full path and 
        termination). Its arguments are *args.
    """
    
    
    if parent_folder_in_cwd:
        parent_folder = os.path.join(os.getcwd(), parent_folder)
        
    save_dir = os.path.join(parent_folder, folder)
    
    def filename_maker(*args, **kwargs):
        
        return os.path.join(save_dir, filename_template.format(*args, **kwargs))

    return filename_maker

#%%

def retrieve_footer(file, comment_marker='#'):
    """Retrieves the footer of a .txt file saved with np.savetxt.
    
    Parameters
    ----------
    file : str
        File's root (must include directory and termination).
    comment_marker='#' : str, optional
        Sign that indicates a line is a comment on np.savetxt.
    
    Returns
    -------
    last_line : str, dict
        File's footer
    
    Raises
    ------
    ValueError : "Footer not found. Sorry!"
        When the last line doesn't begin with 'comment_marker'.
        
    See Also
    --------
    fwp_save.savetxt
    
    """
    
    
    with open(file, 'r') as f:
        for line in f:
            last_line = line
    
    if last_line[0] == comment_marker:
        try:
            last_line = last_line.split(comment_marker + ' ')[-1]
            last_line = last_line.split('\n')[0]
            footer = eval('dict({})'.format(last_line))
            for key, value in footer.items():
                try:
                    number = fst.find_numbers(value)
                    if len(number) == 1:
                        number = number[0]
                        if len(value.split(' ')) == 2:
                            footer[key] = (
                                number, 
                                value.split(' ')[-1]
                                )
                        else:
                            footer[key] = number
                except TypeError:
                    value = value
        except:
            footer = last_line
        return footer
        
    else:
        raise ValueError("No footer found. Sorry!")

#%%

def retrieve_header(file, comment_marker='#'):
    """Retrieves the header of a .txt file saved with np.savetxt.
    
    Parameters
    ----------
    file : str
        File's root (must include directory and termination).
    comment_marker='#' : str, optional
        Sign that indicates a line is a comment on np.savetxt.
    
    Returns
    -------
    last_line : str, list
        File's header
    
    Raises
    ------
    ValueError : "Header not found. Sorry!"
        When the first line doesn't begin with 'comment_marker'.
    
    See Also
    --------
    fwp_save.savetxt
    
    """
    
    
    with open(file, 'r') as f:
        for line in f:
            first_line = line
            break
    
    if first_line[0] == comment_marker:
        header = first_line.split(comment_marker + ' ')[-1]
        header = header.split('\n')[0]
        header = header.split('\t')
        if len(header) > 1:
            return header
        else:
            return header[0]
        
    else:
        raise ValueError("No header found. Sorry!")