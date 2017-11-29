'''
    This script checks and/or installs necessary dependencies to run tools
'''


import general_use
import subprocess
import os

repo_bluez = 'https://github.com/khvzak/bluez-tools.git'
link_lightblue = 'http://prdownloads.sourceforge.net/lightblue/lightblue-0.4.tar.gz?download'

def commandline_install(pack_man, i):
    general_use.update(pack_man)
    return subprocess.run(['sudo', pack_man, '-y', 'install', i]).returncode

def download_install(link):
    return subprocess.run(['curl', '-O', link]).returncode

def clone_git_repo(repo):
    return subprocess.run(["git", "clone", repo]).returncode

def install_pyserial(link):
    '''
        This function installs pyserial. This library is needed to run pyobd, specifically 2.0 because this is the version needed.
    '''

    d_rc = download_install(link) #FYI MIGHT BE ABLE TO RUN PIP INSTALL PYSERIAL. But this will install the latest version
    if d_rc != 0:
        print ('DOWNLOAD FAILED: Failed to download pyserial')
        print ('ERROR CODE:', d_rc)
        return d_rc
    else:
        print ('DOWNLOAD SUCCESSFUL: Successfully downloaded pyserial')
        print ('Building PySerial 2.0 package...')
        current_dir = os.getcwd()
        path = current_dir + '/pyserial-2.0'
        os.chdir(path)
        build_rc = subprocess.run(['python', 'setup.py', 'build']).returncode
        if build_rc != 0:
            print ('BUILD FAILED: Failed to build pyserial.')
            print ('ERROR CODE:', build_rc)
            return build_rc
        else:
            print ('BUILD SUCCESSFUL: Successfully completed pyserial build')
            print ('Installing pyserial...')
            i_rc = subprocess.run(['sudo', 'python', 'setup.py', 'install']).returncode
            if i_rc != 0:
                return i_rc
            else:
                return 0
                general_use.move_up_directory()


def install_NPM(pack_man):
    '''
        This function installs NPM. This is a dependency needed to run canbus-utils
    '''

    print ('Installing npm...')
    npm_rc = commandline_install(pack_man, 'npm')
    if npm_rc != 0:
        print ('INSTALLATION FAILED: Could not install npm. This package is necessary to run canbus-utils')
        print ('ERROR CODE:', npm_rc)
        return npm_rc
    else:
        print ('INSTALLATION SUCCESSFUL: Successfully installed npm')
        return 0

def check_symlink(source_file, symlink):
    '''
        This function checks whether there is a symbolic link between source_file and symlink. If it does not exists, it creates one
    '''

    check_rc = subprocess.run(['test', '-h', symlink]).returncode
    if check_rc!= 0:
        print ('Creating symbolic link between', source_file, 'and', symlink, '...')
        symlink_rc = subprocess.run(['sudo', 'ln', '-s', source_file, symlink]).returncode #this might not work
        if symlink_rc != 0:
            print ('SYMLINK CREATION FAILED: Failed to create a symbolic link between', source_file, 'and', symlink)
        elif symlink_rc == 0:
            print ('SYMLINK CREATION SUCCESSFUL: Successfully created a symbolic link between', source_file, 'and', symlink)
        return symlink_rc
    else:
        print ('Symbolic link already created between', source_file, 'and', symlink)
        return 0

def check_NPM(pack_man):
    '''
        This function checks if NPM is installed. If it is not, it installs it. This is a dependency needed to run canbus-utils
    '''

    try:
        print ('Checking nodejs existence...')
        print ('If nodejs exists, version number will be printed below:')
        check_node_existence_rc = subprocess.run(['/usr/bin/nodejs', '--version']).returncode
    except FileNotFoundError:
        check_node_existence_rc = -1
    try:
        print ('Checking node existence...')
        print ('If node exists, version number will be printed below:')
        check_npm_existence_rc = subprocess.run(['/usr/bin/node', '--version']).returncode
    except FileNotFoundError:
        check_npm_existence_rc = -1

    if check_node_existence_rc == 0:
        if check_npm_existence_rc == 0:
            print ('CONFIRMATION COMPLETE: Both node.js and npm are installed')
            i_rc = 0
        else:
            i_rc = install_NPM(pack_man)
    else:
        print ('Installing nodejs...')
        node_rc = commandline_install(pack_man, 'nodejs')
        if node_rc != 0:
            print ('INSTALLATION FAILED: Could not install nodejs. This package is necessary to run npm which is used for canbus-utils')
            print ('ERROR CODE:', node_rc)
            i_rc = node_rc
        else:
            print ('INSTALLATION SUCCESSFUL: Successfully installed nodejs')
            print ('Installing npm...')
            i_rc = install_NPM(pack_man)    

    if i_rc != 0:
        return i_rc
    else:
        print ('Checking for symbolic link existence between nodejs (/usr/bin/nodejs) and npm (/usr/bin/node)')
        symlink_rc = check_symlink('/usr/bin/nodejs', '/usr/bin/node')
        if symlink_rc != 0:
            return symlink_rc
        else:
            print ('Confirming complete installation of nodejs and npm...') #dk if will keep this yet, we'll see
            node_check_rc = subprocess.run(['/usr/bin/nodejs', '--version']).returncode
            npm_check_rc = subprocess.run(['/usr/bin/node', '--version']).returncode
            if node_check_rc == 0 and npm_check_rc == 0:
                print ('CONFIRMATION COMPLETE: Successfully confirmed installation of both node.js and npm')
                return 0
            else:
                if node_check_rc != 0:
                    print ('CONFIRMATION FAILED: Could not confirm installation of node.js')
                    print ('ERROR CODE:', node_check_rc)
                    return node_check_rc
                elif npm_check_rc != 0:
                    print ('CONFIRMATION FAILED: Could not confirm installation of npm')
                    print ('ERROR CODE:', npm_check_rc)
                    return npm_check_rc

def install_bluez(pack_man):
    '''
        This function installs the bluez dependency. This is also available via sudo apt-get and comes installed in most VM's so we have removed it as a tool and no longer use this function
        However, we kept this code here just incase bluez is not included in your VM and sudo apt-get bluez does not work
        To use this script, follow the instructions in the user manual on how to add a tool (in this case bluez)
        In the install.py, call this function. 
    '''
    print ('Installing Bluez...')
    print ('Cloning Bluez repository...')
    clone_rc = clone_git_repo(repo_bluez)
    if clone_rc != 0:
        print ('CLONING FAILED: Failed to clone repository at', repo_bluez)
        print ('ERROR CODE:', clone_rc)
    else:
        print ('CLONING SUCCESSFUL: Successfully cloned repository at', repo_bluez)
        current_dir = os.getcwd()
        path = current_dir + '/bluez-tools'
        os.chdir(path)
        read_rc = commandline_install(pack_man, 'libreadline-dev')
        if read_rc != 0:
            print ('INSTALLATION FAILED: Failed to install readline.h file. This is needed to complete autoconf')
            print ('ERROR CODE:', read_rc)
            return read_rc
        else:
            print ('INSTALLATION SUCCESSFUL: Successfully installed readline.h')
            print ('Installing autoconf...')
            auto_rc = commandline_install(pack_man, 'autoconf')
            if auto_rc != 0:
                print ('INSTALLATION FAILED: Failed to install autoconf. Cannot complete bluez installation')
                print ('ERROR CODE:'. auto_rc)
                return auto_rc
            else:
                print ('INSTALLATION SUCCESSFUL: Successfully installed autoconf')
                print ('Running autogen.sh...')
                autogen_rc = subprocess.run(['./autogen.sh']).returncode
                if autogen_rc != 0:
                    print ('AUTOGENERATION FAILED: Failed to run autogen.sh. Cannot complete bluez installation')
                    print ('ERROR CODE:', autogen_rc)
                    return autogen_rc
                else:
                    print ('AUTOGENERATION SUCCESSFUL: Successfully ran autogen.sh')
                    print ('Running configure...')
                    config_rc = subprocess.run(['./configure']).returncode
                    if config_rc != 0:
                        print ('CONFIGURATION FAILED: Failed to run ./configure after cloning Bluez repo')
                        print ('ERROR CODE:', config_rc)
                        return config_rc
                    else:
                        print ('CONFIGURATION SUCCESSFUL: Successfully ran ./configure after cloning Bluez repo')
                        print ('Compiling...')
                        make_rc = subprocess.run(['make']).returncode
                        if make_rc != 0:
                            print ('COMPILATION FAILED: Failed to compile bluez package')
                            print ('ERROR CODE:', make_rc)
                            return make_rc
                        else:
                            print ('COMPILATION SUCCESSFUL: Successfully compiled bluez package')
                            print ('Installing Bluez...')
                            make_install_rc = subprocess.run(['sudo', 'make', 'install']).returncode
                            if make_install_rc != 0:
                                print ('INSTALLATION FAILED: Failed to run "make install"')
                                print ('ERROR CODE:', make_install_rc)
                                return make_install_rc
                            else:
                                print ('INSTALLATION SUCCESSFUL: Successfully ran make install')
                                return 0
                                general_use.move_up_directory()

def install_lightblue(pack_man):
    '''
        This function installs the lightblue library/dependency
    '''

    print ('Installing pybluez...')
    pyb_rc = subprocess.run(['sudo', '-H', 'pip', 'install', 'pybluez']).returncode
    if pyb_rc != 0:
        print ('INSTALLATION FAILED: Failed to install pybluez. Cannot complete lightblue installation')
        print ('ERROR CODE:', pyb_rc)
        return pyb_rc
    else:
        print ('INSTALLATION SUCCESSFUL: Successfully installed pybluez')
        print ('Downloading lightblue...')
        light_rc = download_install(link_lightblue)
        if light_rc != 0:
            print ('DOWNLOAD FAILED: Failed to download lightblue. Cannot complete lightblue installation')
            print ('ERROR CODE:', light_rc)
            return light_rc
        else:
            print ('DOWNLOAD SUCCESSFUL: Successfully downloaded lightblue .tar')
            print ('Extracting files...')
            ex_rc = subprocess.run(['tar', '-xzvf', 'lightblue-0.4.tar']).returncode
            if ex_rc != 0:
                print ('EXTRACTION FAILED: Failed to decompress the tar file (lightblue-0.4.tar). Cannot complete lightblue installation')
                print ('ERROR CODE:', ex_rc)
                return ex_rc
            else:
                print ('EXTRACTION SUCCESSFUL: Successfully decompressed lightblue-0.4.tar')
                setup_rc = subprocess.run(['python', 'setup.py', 'install']).returncode
                if setup_rc != 0:
                    print ('INSTALLATION FAILED: Failed to install lightblue')
                    print ('ERROR CODE:', setup_rc)
                    return setup_rc
                else:
                    print ('INSTALLATION SUCCESSFUL: Successfully installed lightblue')
                    return 0

def can_utils_x(pack_man):
    '''
        This function installs the matplot-lib library which is needed for can-utils-x to run
    '''

    mat_rc = commandline_install(pack_man, 'python-matplotlib')
    if mat_rc != 0:
        print ('INSTALLATION FAILED: Failed to install matplotlib from python. This is needed to run do')
        print ('ERROR CODE:'. mat_rc)
    else:
        print ('INSTALLATION SUCCESSFUL: Successfully installed matplotlib from python')
        socket = github_tools(pack_man, 'can-utils', repo) #this clones and installs the can-utils repository which is also needed for can-utils to run
    return mat_rc

