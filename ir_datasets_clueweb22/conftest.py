
from itertools import islice
from re import Pattern

from pytest_subtests import SubTests
from ir_datasets import log, load, Dataset
from tqdm.auto import tqdm


_logger = log.easy()


def _assert_namedtuple(a, b):
    assert type(a).__name__ == type(b).__name__
    if hasattr(type(a), '_fields') or hasattr(type(b), '_fields'):
        assert type(a)._fields == type(b)._fields
    for v_a, v_b in zip(a, b):
        # support compiled regex for matching (e.g., for long documents)
        if isinstance(v_b, Pattern):
            assert v_b.match(v_a) is not None
        elif isinstance(v_a, Pattern):
            assert v_a.match(v_b) is not None
        elif isinstance(v_a, tuple) and isinstance(v_b, tuple):
            _assert_namedtuple(v_a, v_b)
        elif isinstance(v_a, list) and isinstance(v_b, list):
            _assert_namedtuple(v_a, v_b)
        else:
            assert v_a == v_b


def _test_docs(subtests: SubTests, dataset_name, count=None, items=None, test_docstore=True, test_iter_split=True) -> None:
    orig_items = dict(items)
    with subtests.test('docs', dataset=dataset_name):
        if isinstance(dataset_name, str):
            dataset = load(dataset_name)
        else:
            dataset = dataset_name
        expected_count = count
        items = items or {}
        count = 0
        for i, doc in enumerate(_logger.pbar(dataset.docs_iter(), f'{dataset_name} docs', unit='doc')):
            count += 1
            if i in items:
                _assert_namedtuple(doc, items[i])
                del items[i]
                if expected_count is None and len(items) == 0:
                    break  # no point in going further

        if expected_count is not None:
            assert expected_count == count

        assert {} == items

    if test_iter_split:
        with subtests.test('docs_iter split', dataset=dataset_name):
            it = dataset.docs_iter()
            with _logger.duration('doc lookups by index'):
                for idx, doc in orig_items.items():
                    _assert_namedtuple(next(it[idx:idx+1]), doc)
                    _assert_namedtuple(it[idx], doc)

    if test_docstore:
        with subtests.test('docs_store', dataset=dataset_name):
            doc_store = dataset.docs_store()
            with _logger.duration('doc lookups by doc_id'):
                for doc in orig_items.values():
                    ret_doc = doc_store.get(doc.doc_id)
                    _assert_namedtuple(doc, ret_doc)


def _test_docs_slice(
        dataset: Dataset,
        indices: slice,
        num_expected: int,
        name: str,
        skip_islice: bool = False,
) -> None:
    with _logger.duration(f"{name} (slice)"):
        docs_slice = list(tqdm(dataset.docs_iter()[indices]))
    docs_slice = sorted(docs_slice)
    assert len(docs_slice) == num_expected
    if skip_islice:
        return

    with _logger.duration(f"{name} (islice)"):
        docs_islice = list(islice(
            tqdm(dataset.docs_iter()),
            indices.start, indices.stop, indices.step
        ))
    docs_islice = sorted(docs_islice)
    assert len(docs_islice) == num_expected

    assert docs_slice == docs_islice
