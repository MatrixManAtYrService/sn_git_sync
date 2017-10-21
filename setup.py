from setuptools import setup

setup(name='sn_git_sync',
      version='0.1.0.dev1',
      description='syncs github with simplenote',
      url='https://github.com/MatrixManAtYrService/gitSnSync',
      author='M@ Rixman',
      author_email ='gitSnSync@matt.rixman.org',
      license='MPL-2.0',
      keywords='git simplenote sync',
      packages=['sn_git'],
      python_requires = '>=3',
      entry_points={'console_scripts':['sngit = sn_git.main:main']}
      )

