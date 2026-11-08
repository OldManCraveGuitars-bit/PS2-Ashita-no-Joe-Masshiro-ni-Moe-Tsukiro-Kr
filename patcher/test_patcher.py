import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from patcher import install

class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.addCleanup(self.directory.cleanup)
        self.base=Path(self.directory.name);self.source=self.base/'original.iso';self.source.write_bytes(b'original bytes')
        self.patch=self.base/'sample.xdelta';self.patch.write_bytes(b'delta sample')
        self.output=self.base/'korean.iso'
        self.manifest=dict(version='0.95',source=dict(bytes=self.source.stat().st_size,sha256=hashlib.sha256(self.source.read_bytes()).hexdigest()),
            output=dict(bytes=100,sha256='0'*64),patch=dict(file=self.patch.name,bytes=self.patch.stat().st_size,sha256='0'*64))
        self.save()
    def save(self):
        (self.base/'patch-manifest.json').write_text(json.dumps(self.manifest),encoding='utf-8')
    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b'existing output')
        with self.assertRaises(FileExistsError):install(self.source,self.output,self.base)
        self.assertEqual(self.output.read_bytes(),b'existing output')
    def test_source_cannot_be_output(self):
        with self.assertRaises(ValueError):install(self.source,self.source,self.base)
        self.assertEqual(self.source.read_bytes(),b'original bytes')
    def test_wrong_source_is_rejected_before_decoding(self):
        self.manifest['source']['sha256']='0'*64;self.save()
        with self.assertRaisesRegex(ValueError,'원본 ISO'):install(self.source,self.output,self.base)
        self.assertFalse(self.output.exists())
    def test_damaged_patch_is_rejected_before_decoding(self):
        with self.assertRaisesRegex(ValueError,'패치 파일'):install(self.source,self.output,self.base)
        self.assertFalse(self.output.exists());self.assertEqual(self.source.read_bytes(),b'original bytes')

if __name__=='__main__':unittest.main()
