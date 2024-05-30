import configparser
import os
import pytest

from keri.core.coring import Matter, MtrDex

os.makedirs("test_vectors/primitives/", exist_ok=True)

old_init = Matter.__init__
old_directory = os.getcwd()

def new_init(self, raw=None, code=MtrDex.Ed25519N, soft='', rize=None,
                 qb64b=None, qb64=None, qb2=None, strip=False):
    old_init(self, raw=raw, code=code, soft=soft, rize=rize,
                 qb64b=qb64b, qb64=qb64, qb2=qb2, strip=strip)
    """
    raw:    49-a4-da-94-1f-1b-94-8d-d0-b4-c6-08-b1-78-1e-67-a8-bb-ae-27-bc-60-4b-f1-21-c1-7e-48-d1-0e-de-c7-77-76-40-2c-43-54-5b-76-b3-2d-c3-be-37-d1-80-1b-9f-85-22-bf-0e-75-3f-05-6c-9a-e3-95-af-24-66-0c
    code:   A
    qb2:    00-10-49-a4-da-94-1f-1b-94-8d-d0-b4-c6-08-b1-78-1e-67-a8-bb-ae-27-bc-60-4b-f1-21-c1-7e-48-d1-0e-de-c7-77-76-40-2c-43-54-5b-76-b3-2d-c3-be-37-d1-80-1b-9f-85-22-bf-0e-75-3f-05-6c-9a-e3-95-af-24-66-0c
    qb64:   ABBJpNqUHxuUjdC0xgixeB5nqLuuJ7xgS_EhwX5I0Q7ex3d2QCxDVFt2sy3DvjfRgBufhSK_DnU_BWya45WvJGYM
    """
    config_writer = configparser.ConfigParser()
    config_writer['PRIMITIVE'] = {"code": self.code,
                                 "raw": self.raw.hex("-"),
                                 "qb2": self.qb2.hex("-"),
                                 "qb64": self.qb64}
    with open(old_directory + f"/test_vectors/primitives/{self.qb64[:64]}", "w") as fyle:
        config_writer.write(fyle)
    
    # [PRIMITIVE]
    # code = A
    # raw = 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
    # qb2 = 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00
    # qb64 = AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Matter.__init__ = new_init

keri_repo = os.getenv("KERI_REPO")
if not keri_repo:
    raise Exception("Environment variable not set: KERI_REPO")
os.chdir(keri_repo)
pytest.main()