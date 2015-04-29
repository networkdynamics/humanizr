from distutils.core import setup


setup(
    name = 'Twitter Feature Extractor',
    version = '0.0.3',
    scripts = ['bin/tfx'],
    packages = ['tfx'],
    package_dir = {'tfx': 'src/tfx'},
    package_data = {'tfx': ['resources/*']},

    author = 'Wendy Liu',
    author_email = 'wendy.liu@mail.mcgill.ca',
    description = "A tool for extracting feature vectors from Twitter users. \
                  For use in conjunction with a machine learning classifier. \
                  For usage information, run `tfx --help`."
)
