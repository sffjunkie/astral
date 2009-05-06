try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='celestial',
    version='0.01',
    description='Celestial calculations for dawn, sunrise, solar noon, sunset and dusk.',
    author='Simon Kennedy',
    author_email='celestial@sffjunkie.co.uk',
    url="http://www.sffjunkie.co.uk/python-celestial.html",
    license='MIT',
    py_modules=['celestial'],
    install_requires=['pytz']
)

