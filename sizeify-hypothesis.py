import os
import uuid

from hypothesis import assume, given, settings, Verbosity
from hypothesis.strategies import dictionaries, text, recursive, none, booleans, floats, lists

from keri.core.coring import sizeify, loads, Versionage

@settings(verbosity=Verbosity.verbose, max_examples=100)

# 1. Generate random dicts that are gonna be smaller than the max size of cesr fieldmap
# 2. Add some random version
# 2. sizeify them (we'll get back "raw" serialization and new dict with updated version) for each serialization type
# 3. loads(raw serializations) == updated ked

@given(recursive(
    none() | booleans() | floats(allow_nan=False, allow_infinity=False) | text(),
    lambda children: lists(children) | dictionaries(text(), children)))
def test_sizeify_v1(test_dict):
    for kind in ['JSON', 'MGPK', 'CBOR']:
        assume(isinstance(test_dict, dict))
        test_dict.pop("v", None)
        dict_with_version = {"v": f"KERI10{kind}000000_"}
        dict_with_version.update(test_dict)
        assert isinstance(dict_with_version, dict)
        assert dict_with_version.get("v") == f"KERI10{kind}000000_"
        cesr_message, _, _, _, _ = sizeify(dict_with_version, kind=kind, version=Versionage(major=1, minor=0))
        with open(f"example_payloads/version1/{kind.lower()}/cesr_message_{uuid.uuid1()}.{kind.lower()}","wb") as fyle:
            fyle.write(cesr_message)
        assert loads(cesr_message, kind=kind) == dict_with_version

@given(recursive(
    none() | booleans() | floats(allow_nan=False, allow_infinity=False) | text(),
    lambda children: lists(children) | dictionaries(text(), children)))
def test_sizeify_v2(test_dict):
    for kind in ['JSON', 'MGPK', 'CBOR']:
        assume(isinstance(test_dict, dict))
        test_dict.pop("v", None)
        dict_with_version = {"v": f"KERICAA{kind}AAAA."}
        dict_with_version.update(test_dict)
        # TODO Fix asserts later
        # assert isinstance(dict_with_version, dict)
        # assert dict_with_version.get("v") == f"KERIBAA{kind}AAAA."
        cesr_message, _, _, _, _ = sizeify(dict_with_version, kind=kind, version=Versionage(major=2, minor=0))
        with open(f"example_payloads/version2/{kind.lower()}/cesr_message_{uuid.uuid1()}.{kind.lower()}","wb") as fyle:
            fyle.write(cesr_message)
        # assert loads(cesr_message, kind=kind) == dict_with_version

if __name__ == "__main__":
    os.makedirs("example_payloads", exist_ok=True)
    os.makedirs("example_payloads/version1", exist_ok=True)
    os.makedirs("example_payloads/version1/mgpk", exist_ok=True)
    os.makedirs("example_payloads/version1/json", exist_ok=True)
    os.makedirs("example_payloads/version1/cbor", exist_ok=True)
    os.makedirs("example_payloads/version2", exist_ok=True)
    os.makedirs("example_payloads/version2/mgpk", exist_ok=True)
    os.makedirs("example_payloads/version2/json", exist_ok=True)
    os.makedirs("example_payloads/version2/cbor", exist_ok=True)
    test_sizeify_v1()
    test_sizeify_v2()