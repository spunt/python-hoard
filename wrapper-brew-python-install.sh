                #!/bin/bash

# Preliminaries
# -----------------------------------------------------------------
sudo -v # Ask for the administrator password upfront
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &  # Keep-alive: update existing `sudo` time stamp until `.osx` has finished
sudo chown -R $(whoami) $(brew --prefix)
brew update

# Install Python3
# -----------------------------------------------------------------
brew install python3
brew linkapps python3

# upgrade pip3
# -----------------------------------------------------------------
pip3 install --upgrade setuptools
pip3 install --upgrade pip
pip3 install pip-review

# virtualenv: http://www.virtualenv.org/
# -----------------------------------------------------------------
pip3 install virtualenv

# Dependencies
# -----------------------------------------------------------------
pip3 install nose
pip3 install pyparsing
pip3 install python-dateutil
pip3 install zeromq # Necessary for pyzmq
pip3 install pyzmq
pip3 install pygments
pip3 install jinja2
pip3 install tornado
pip3 install PyQt5
pip3 install pymdown-extensions
pip3 install jedi # autocomplete/static analysis: http://jedi.readthedocs.io
pip3 install pep8
pip3 install autopep8 # auto reformat code in PEP 8 style.
# ex. >>> autopep8 --in-place optparse.py
# $ autopep8 --in-place optparse.py

# =================================================================

# Core Scientific Python
# -----------------------------------------------------------------
pip3 install numpy
pip3 install numpydoc
pip3 install scipy
pip3 install pandas
pip3 install sympy
pip3 install statsmodels
pip3 install scikit-learn


# Visualization
# -----------------------------------------------------------------
s


# Natural Language Processing (NLP)
# -----------------------------------------------------------------
pip3 install nltk
pip3 install gensim
pip3 install textblob

# Data Mining
# -----------------------------------------------------------------
pip3 install scrapy


# Machine Learning
# -----------------------------------------------------------------


# Stimulus Presentation (PsychoPy)
# -----------------------------------------------------------------
# Note: You will need to manually install pyo: http://ajaxsoundstudio.com/software/pyo/
pip3 install -U wxPython
pip3 install pyopengl pyglet pillow moviepy lxml openpyxl configobj psychopy
pip3 install iolabs pyyaml gevent greenlet msgpack-python psutil tables xlrd

# Deep Learning
# -----------------------------------------------------------------
# pip3 install theano
# pip3 install tensorflow
# pip3 install keras

# Functional Neuroimaging
# -----------------------------------------------------------------
# pip3 install Nibabel
# pip3 install nipy # https://github.com/nipy/nipy
# pip3 install mriqc # http://mriqc.readthedocs.io/en/stable/install.html
# pip3 install -U --user nilearn # https://github.com/nilearn/nilearn

# Web Development
# # -----------------------------------------------------------------
# pip3 install boto3 # Python SDK for Amazon Web Services (AWS)
# pip3 install mkdocs # static site generator geared to documentation
# pip3 install mkdocs-material # mkdocs theme
# pip3 install django

# IDEs
# -----------------------------------------------------------------
pip3 install ipython[zmq,qtconsole,notebook,test]
pip3 install ipywidgets ipykernel
python3 -m ipykernel install --user
pip3 install jupyter jupyterlab jupyterthemes
jupyter serverextension enable --py jupyterlab --sys-prefix

# Miscellaneous
# -----------------------------------------------------------------
# pip3 install dataset # https://github.com/pudo/dataset
# pip3 install tablib # https://github.com/kennethreitz/tablib

