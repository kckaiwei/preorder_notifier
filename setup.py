from setuptools import setup, find_packages

setup(name='GameDealBot',
      version='1.0.0',
      description='reddit bot for scraping Game Deals',
	  author = 'Kevin C.',
	  author_email = 'kckaiwei@gmail.com',
      keywords='reddit bot',
      url='https://github.com/HewlettPackard/python-ilorest-library',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          'praw'
      ])
