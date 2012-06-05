#!/usr/bin/env python
"""
BaseStation - A Python-based control panel for QuadHLFC
Copyright (c) 2012 Greg Haynes

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.command.install_scripts import install_scripts
from distutils.core import setup


class InstallScripts(install_scripts):
    '''create the bat for windows so the launcher script
    works out of the box'''
    def run(self):
        import os
        '''if os.name == 'nt':
            import sys
            parts = os.path.split(sys.executable)
            py_path = os.path.join(*(parts[:-1]))
            script_path = os.path.join(py_path, 'Scripts')
            f = open(os.path.join(script_path, 'pymazon.bat'), 'w')
            pymazon = os.path.join(script_path, 'pymazon')
            bat = '@' + ('"%s" "%s"' % (sys.executable, pymazon)) + ' %*'
            f.write(bat)
            f.close()'''
        install_scripts.run(self)


setup(name='BaseStation',
      version='1.12.0526',
      description='A Python-based control panel for QuadHLFC',
      author='Greg Haynes',
      author_email='psu-avt@googlegroups.com',
      url='https://github.com/PSU-AVT/BaseStation',
      package_dir = {'basestation': './basestation'},
      packages=['basestation', 'basestation.core','basestation.resource'],
      package_data={'basestation.resource': ['icons/*.png']},
      scripts=['./bin/basestation'],
      license='GPLv3',
      long_description=\
'''This is the GUI for controlling the QuadCopter over the server with PubSub. 
All commands to the helicopter are issued from your computer to the server, 
which itself sends the commands to the helicopter and feedback is returned to 
you using PubSub subscription. Therefore, the helicopter has two important 
characteristics for control: it is available over a large network of potential 
controllers, but also the network requires low latency; secondly, command 
control is run in order of the issuing time of the commands, meaning that 
contradictory commands will be executed in the order they are issued.''',
      cmdclass={'install_scripts': InstallScripts},
     )
