import copy
import hashlib
import itertools
import os

import pytest

import keri.core.coring as coring
from keri.kering import Version, Versionage


def init():
    os.makedirs("example_payloads/keripy_tests/", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/CBOR", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/JSON", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v1/MGPK", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/CBOR", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/JSON", exist_ok=True)
    os.makedirs("example_payloads/keripy_tests/v2/MGPK", exist_ok=True)

def monkey_patch_sizeify():
    old_sizeify = coring.sizeify # the function not the result of the call
    old_directory = os.getcwd()

    v1_tuple = Versionage(major=1, minor=0)
    v2_tuple = Versionage(major=2, minor=0)

    # If this signature changes this will probably break in weird ways
    def new_sizeify(ked, kind=None, version=Version):
        # old_ked = copy.deepcopy(ked)
        # old_kind = copy.deepcopy(kind)
        # old_version = copy.deepcopy(version)

        # _cesr_message, proto, kind, ked, vrsn = old_sizeify(ked=ked, kind=k, version=v)
        # print(proto, kind, vrsn)
        for v, k in itertools.product((v1_tuple, v2_tuple), 
                                      ('JSON', 'MGPK', 'CBOR')):
            cesr_message, _proto, _kind, _ked, _vrsn = old_sizeify(ked=ked, kind=kind, version=version)
            hashed_filename = hashlib.md5(cesr_message).hexdigest()
            with open(old_directory + f"/example_payloads/keripy_tests/v{v.major}/{k}/{hashed_filename}", "wb") as fyle:
                fyle.write(cesr_message)

        # We run whatever was passed in originally
        return old_sizeify(ked=ked, kind=kind, version=version)

    # Monkeypatch
    coring.sizeify = new_sizeify

def cd_to_keripy_repo_run_pytest():
    keri_repo = os.getenv("KERI_REPO")
    if not keri_repo:
        raise Exception("Environment variable not set: KERI_REPO")
    os.chdir(keri_repo)
    pytest.main([])

if __name__ == '__main__':
    init()
    monkey_patch_sizeify()
    cd_to_keripy_repo_run_pytest()
