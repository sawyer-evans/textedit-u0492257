"""Language definitions for syntax highlighting."""

from enum import Enum, auto


class TokenType(Enum):
    """Types of tokens for syntax highlighting."""
    KEYWORD = auto()
    TYPE = auto()
    STRING = auto()
    COMMENT = auto()
    NUMBER = auto()
    BUILTIN = auto()
    FUNCTION = auto()
    DECORATOR = auto()
    OPERATOR = auto()


# Color scheme (dark theme)
TOKEN_COLORS = {
    TokenType.KEYWORD: "#FF8000",
    TokenType.TYPE: "#00AAAA",
    TokenType.STRING: "#90EE90",
    TokenType.COMMENT: "#646464",
    TokenType.NUMBER: "#B5CEA8",
    TokenType.BUILTIN: "#DCDCAA",
    TokenType.FUNCTION: "#DCDC64",
    TokenType.DECORATOR: "#4EC9B0",
    TokenType.OPERATOR: "#FF8000",
}


class LanguageDefinition:
    """Holds regex patterns for a language, ordered by priority."""

    def __init__(self, name, patterns, multiline_patterns=None):
        """
        Args:
            name: Language name.
            patterns: List of (TokenType, regex_pattern_string) tuples.
            multiline_patterns: List of (TokenType, start_regex, end_regex) tuples.
        """
        self.name = name
        self.patterns = patterns
        self.multiline_patterns = multiline_patterns or []


def _python_definition():
    keywords = (
        r'\b(?:False|None|True|and|as|assert|async|await|break|class|continue|'
        r'def|del|elif|else|except|finally|for|from|global|if|import|in|is|'
        r'lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'
    )
    builtins = (
        r'\b(?:print|len|range|int|str|float|list|dict|set|tuple|bool|'
        r'type|isinstance|hasattr|getattr|setattr|open|super|property|'
        r'staticmethod|classmethod|enumerate|zip|map|filter|sorted|reversed|'
        r'abs|min|max|sum|any|all|input|id|repr|hex|oct|bin|chr|ord)\b'
    )
    types = r'\b(?:int|str|float|bool|list|dict|set|tuple|bytes|bytearray|complex|frozenset|object)\b'

    patterns = [
        (TokenType.COMMENT, r'#[^\n]*'),
        (TokenType.STRING, r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'),
        (TokenType.DECORATOR, r'@\w+(?:\.\w+)*'),
        (TokenType.KEYWORD, keywords),
        (TokenType.TYPE, types),
        (TokenType.BUILTIN, builtins),
        (TokenType.FUNCTION, r'\b\w+(?=\s*\()'),
        (TokenType.NUMBER, r'\b(?:0[xXoObB][\da-fA-F_]+|\d[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?)\b'),
        (TokenType.OPERATOR, r'[+\-*/%=<>!&|^~]+'),
    ]

    multiline_patterns = [
        (TokenType.STRING, r'"""', r'"""'),
        (TokenType.STRING, r"'''", r"'''"),
    ]

    return LanguageDefinition("python", patterns, multiline_patterns)


def _javascript_definition():
    keywords = (
        r'\b(?:break|case|catch|class|const|continue|debugger|default|delete|'
        r'do|else|export|extends|finally|for|function|if|import|in|instanceof|'
        r'let|new|of|return|super|switch|this|throw|try|typeof|var|void|while|'
        r'with|yield|async|await|from|static|get|set)\b'
    )
    builtins = (
        r'\b(?:console|document|window|Array|Object|String|Number|Boolean|'
        r'Math|JSON|Promise|Date|RegExp|Error|Map|Set|Symbol|parseInt|'
        r'parseFloat|isNaN|isFinite|undefined|null|NaN|Infinity)\b'
    )
    types = r'\b(?:string|number|boolean|object|symbol|bigint|undefined|null|void|never|any)\b'

    patterns = [
        (TokenType.COMMENT, r'//[^\n]*'),
        (TokenType.STRING, r'(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|`(?:[^`\\]|\\.)*`)'),
        (TokenType.KEYWORD, keywords),
        (TokenType.TYPE, types),
        (TokenType.BUILTIN, builtins),
        (TokenType.FUNCTION, r'\b\w+(?=\s*\()'),
        (TokenType.NUMBER, r'\b(?:0[xXoObB][\da-fA-F_]+|\d[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?)\b'),
        (TokenType.OPERATOR, r'[+\-*/%=<>!&|^~?:]+'),
    ]

    multiline_patterns = [
        (TokenType.COMMENT, r'/\*', r'\*/'),
    ]

    return LanguageDefinition("javascript", patterns, multiline_patterns)


def _html_definition():
    patterns = [
        (TokenType.COMMENT, r'<!--.*?-->'),
        (TokenType.STRING, r'(?:"[^"]*"|\'[^\']*\')'),
        (TokenType.DECORATOR, r'</?[\w-]+'),  # tags
        (TokenType.DECORATOR, r'/?>'),  # closing angle brackets
        (TokenType.KEYWORD, r'\b(?:class|id|href|src|style|type|name|value|alt|title|rel|lang|charset|content|http-equiv)\b'),
        (TokenType.BUILTIN, r'&\w+;'),  # HTML entities
    ]

    multiline_patterns = [
        (TokenType.COMMENT, r'<!--', r'-->'),
    ]

    return LanguageDefinition("html", patterns, multiline_patterns)


def _css_definition():
    keywords = (
        r'\b(?:important|inherit|initial|unset|none|auto|block|inline|flex|grid|'
        r'absolute|relative|fixed|sticky|solid|dashed|dotted|hidden|visible|'
        r'normal|bold|italic|center|left|right|top|bottom)\b'
    )
    builtins = (
        r'\b(?:color|background|margin|padding|border|font|display|position|'
        r'width|height|max-width|min-width|max-height|min-height|overflow|'
        r'text-align|text-decoration|line-height|opacity|z-index|transition|'
        r'transform|animation|box-shadow|cursor|content|float|clear)\b'
    )

    patterns = [
        (TokenType.COMMENT, r'/\*.*?\*/'),
        (TokenType.STRING, r'(?:"[^"]*"|\'[^\']*\')'),
        (TokenType.DECORATOR, r'[.#][\w-]+'),  # selectors
        (TokenType.KEYWORD, keywords),
        (TokenType.BUILTIN, builtins),
        (TokenType.NUMBER, r'\b\d+(?:\.\d+)?(?:px|em|rem|%|vh|vw|s|ms|deg|fr)?\b'),
        (TokenType.FUNCTION, r'\b\w+(?=\s*\()'),
        (TokenType.OPERATOR, r'[{}:;,>+~]'),
    ]

    multiline_patterns = [
        (TokenType.COMMENT, r'/\*', r'\*/'),
    ]

    return LanguageDefinition("css", patterns, multiline_patterns)


LANGUAGES = {
    "python": _python_definition(),
    "javascript": _javascript_definition(),
    "html": _html_definition(),
    "css": _css_definition(),
}
