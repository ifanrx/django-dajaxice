import os
import tempfile

from django.contrib.staticfiles import finders
from django.core.exceptions import SuspiciousOperation
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template


class VirtualStorage(FileSystemStorage):
    """Mock a FileSystemStorage to build tmp files on demand."""

    def __init__(self, *args, **kwargs):
        self._files_cache = {}
        super(VirtualStorage, self).__init__(*args, **kwargs)

    def get_or_create_file(self, path):
        if path not in self.files:
            return ''

        data = getattr(self, self.files[path])()

        cached_path = self._files_cache.get(path)
        if cached_path and os.path.exists(cached_path):
            try:
                with open(cached_path, 'r', encoding='utf-8') as current_file:
                    current_data = current_file.read()
                if current_data == data:
                    return cached_path
                os.remove(cached_path)
            except Exception:
                pass

        handle, tmp_path = tempfile.mkstemp()
        with os.fdopen(handle, 'w', encoding='utf-8') as tmp_file:
            tmp_file.write(data)
        self._files_cache[path] = tmp_path

        return self._files_cache[path]

    def exists(self, name):
        return name in self.files

    def listdir(self, path):
        path = path.strip('/')
        prefix = (path + '/') if path else ''
        folders, files = set(), set()
        for f in self.files:
            f_norm = f.replace('\\', '/')
            if prefix and not f_norm.startswith(prefix):
                continue
            relative = f_norm[len(prefix):]
            if '/' in relative:
                folders.add(relative.split('/', 1)[0])
            elif relative:
                files.add(relative)
        return sorted(list(folders)), sorted(list(files))

    def path(self, name):
        try:
            path = self.get_or_create_file(name)
        except ValueError:
            raise SuspiciousOperation("Attempted access to '%s' denied." % name)
        return os.path.normpath(path)


class DajaxiceStorage(VirtualStorage):

    files = {
        'dajaxice/dajaxice.core.js': 'dajaxice_core_js',
        os.path.join('dajaxice', 'dajaxice.core.js'): 'dajaxice_core_js',
    }

    def dajaxice_core_js(self):
        from dajaxice.core import dajaxice_autodiscover, dajaxice_config

        dajaxice_autodiscover()

        return get_template('dajaxice/dajaxice.core.js').render(
            {'dajaxice_config': dajaxice_config}
        )


class DajaxiceFinder(finders.BaseStorageFinder):
    storage = DajaxiceStorage()
