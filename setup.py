from setuptools import setup

lcns = 'License :: OSI Approved :: GNU General Public License v3 or later'\
          '(GPLv3+)'
setup(name='sudoku',
      author='Maksim Grinman',
      author_email='maxchgr@gmail.com',
      description='Solves sudoku puzzles',
      keywords=['sudoku'],
      version='1.0',
      py_modules=['sudoku_solver'],
      license='GPLv3+',
      classifiers = [lcns])
