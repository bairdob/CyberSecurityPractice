from pygost.gost3411_12 import GOST341112

m = GOST341112(digest_size=256)
m.update(b"foo")
m.update(b"bar")
print(m.hexdigest())
m = GOST341112(digest_size=256)
m.update(b"a")
print(m.hexdigest())
m = GOST341112(digest_size=256)
m.update(b"a")
print(m.hexdigest())
