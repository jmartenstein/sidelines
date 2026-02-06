# sidelines
A simulator program for American / Gridiron football

## Testing

This project uses `pytest` for unit testing. The tests are located in the `tests/` directory.

### Running Tests

To run all tests, ensure you have the dependencies installed and execute:

```bash
python3 -m pytest
```

If you are using a virtual environment:

```bash
.venv/bin/python -m pytest
```

### Example Output

```text
================================== test session starts ==================================
platform darwin -- Python 3.x.x, pytest-9.x.x, pluggy-1.x.x
rootdir: /Users/justin/Code/sidelines
collected 16 items

tests/test_play_by_play.py ......                                                 [ 37%]
tests/test_score_over_time.py ..........                                          [100%]

================================== 16 passed in 3.69s ===================================
```
