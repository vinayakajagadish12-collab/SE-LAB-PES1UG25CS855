from hypothesis import given, example, strategies as st
from bowling_alley_parser import format_player_name, parse_frame, parse_scoreboard

inputs = st.one_of(st.text(), st.none(), st.integers(), st.floats(),
                   st.binary(), st.lists(st.integers()),
                   st.dictionaries(st.text(), st.integers()))

@given(inputs)
@example(None)
@example('  asha  ')
def test_format_player_name_no_crash(s):
    try:
        result = format_player_name(s)
    except Exception as exc:
        assert False, f'format_player_name crashed: {exc!r}'
    assert isinstance(result, str) and len(result) <= 10
    if isinstance(s, str):
        assert result == s.strip().title()[:10]
    else:
        assert result == ''

@given(inputs)
@example('')
@example('X')
@example('7/')
@example('45')
@example('99')
@example('123')
def test_parse_frame_no_crash(s):
    try:
        result = parse_frame(s)
    except Exception as exc:
        assert False, f'parse_frame crashed: {exc!r}'
    assert result is None or (isinstance(result, tuple) and len(result) == 2
        and all(type(n) is int and 0 <= n <= 10 for n in result)
        and sum(result) <= 10)
    if s == 'X': assert result == (10, 0)
    if s == '7/': assert result == (7, 3)
    if s == '45': assert result == (4, 5)
    if s in ('99', '123', ''): assert result is None

@given(inputs)
@example('')
@example('Asha:150,Ravi:132')
@example('Asha:301')
@example('A:1,bad')
def test_parse_scoreboard_no_crash(s):
    try:
        result = parse_scoreboard(s)
    except Exception as exc:
        assert False, f'parse_scoreboard crashed: {exc!r}'
    assert isinstance(result, dict)
    assert all(isinstance(k, str) and k.strip() and type(v) is int
               and 0 <= v <= 300 for k, v in result.items())
    if s == 'Asha:150,Ravi:132': assert result == {'Asha':150, 'Ravi':132}
    if s in ('', 'Asha:301', 'A:1,bad'): assert result == {}
