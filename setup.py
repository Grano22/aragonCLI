from distutils.core import setup
setup(
  name = 'aragon',
  packages = ['aragon'],
  version = '0.1', 
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Aragon is api for CLI applications', 
  author = 'Grano22', 
  author_email = 'grano22@outlook.com', 
  url = 'https://github.com/Grano22/aragonCLI',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['Aragon', 'CLI', 'application', 'command', 'api'],
  install_requires=[
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)