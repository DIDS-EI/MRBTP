// Generated from D:/Workspace/CXL/Code/MABTPG/mabtpg/behavior_tree/btml/grammar/BTMLLexer.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class BTMLLexer extends BTMLLexerBase {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		INDENT=1, DEDENT=2, NEWLINE=3, OPEN_PAREN=4, CLOSE_PAREN=5, COMMA=6, OPEN_BRACE=7, 
		CLOSE_BRACE=8, LINE_COMMENT=9, WS=10, SEQUENCE=11, SELECTOR=12, PARALLEL=13, 
		ACT=14, COND=15, NOT=16, String=17, COLON=18, DEF=19, AND=20;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"NEWLINE", "OPEN_PAREN", "CLOSE_PAREN", "COMMA", "OPEN_BRACE", "CLOSE_BRACE", 
			"LINE_COMMENT", "WS", "SEQUENCE", "SELECTOR", "PARALLEL", "ACT", "COND", 
			"NOT", "String", "COLON", "DEF", "AND", "SPACES"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, "'('", "')'", "','", "'{'", "'}'", null, null, 
			null, null, "'parallel'", null, null, "'Not'", null, "':'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "INDENT", "DEDENT", "NEWLINE", "OPEN_PAREN", "CLOSE_PAREN", "COMMA", 
			"OPEN_BRACE", "CLOSE_BRACE", "LINE_COMMENT", "WS", "SEQUENCE", "SELECTOR", 
			"PARALLEL", "ACT", "COND", "NOT", "String", "COLON", "DEF", "AND"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public BTMLLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "BTMLLexer.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	@Override
	public void action(RuleContext _localctx, int ruleIndex, int actionIndex) {
		switch (ruleIndex) {
		case 0:
			NEWLINE_action((RuleContext)_localctx, actionIndex);
			break;
		}
	}
	private void NEWLINE_action(RuleContext _localctx, int actionIndex) {
		switch (actionIndex) {
		case 0:
			self.onNewLine();
			break;
		}
	}
	@Override
	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 0:
			return NEWLINE_sempred((RuleContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean NEWLINE_sempred(RuleContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return self.atStartOfInput();
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0000\u0014\u00be\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002"+
		"\u0001\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002"+
		"\u0004\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002"+
		"\u0007\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002"+
		"\u000b\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e"+
		"\u0002\u000f\u0007\u000f\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011"+
		"\u0002\u0012\u0007\u0012\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000"+
		"+\b\u0000\u0001\u0000\u0001\u0000\u0003\u0000/\b\u0000\u0001\u0000\u0003"+
		"\u00002\b\u0000\u0003\u00004\b\u0000\u0001\u0000\u0001\u0000\u0001\u0001"+
		"\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0004"+
		"\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0006\u0005\u0006F\b\u0006\n\u0006\f\u0006I\t\u0006\u0001\u0006"+
		"\u0003\u0006L\b\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0007\u0004\u0007S\b\u0007\u000b\u0007\f\u0007T\u0001\u0007\u0001"+
		"\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b"+
		"\u0001\b\u0001\b\u0001\b\u0003\bd\b\b\u0001\t\u0001\t\u0001\t\u0001\t"+
		"\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0003\t|\b\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001"+
		"\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0003\u000b\u0090"+
		"\b\u000b\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0003\f\u009f\b\f\u0001\r\u0001"+
		"\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e\u0005\u000e\u00a7\b\u000e\n"+
		"\u000e\f\u000e\u00aa\t\u000e\u0001\u000f\u0001\u000f\u0001\u0010\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0011\u0001"+
		"\u0011\u0001\u0011\u0001\u0011\u0003\u0011\u00b8\b\u0011\u0001\u0012\u0004"+
		"\u0012\u00bb\b\u0012\u000b\u0012\f\u0012\u00bc\u0001G\u0000\u0013\u0001"+
		"\u0003\u0003\u0004\u0005\u0005\u0007\u0006\t\u0007\u000b\b\r\t\u000f\n"+
		"\u0011\u000b\u0013\f\u0015\r\u0017\u000e\u0019\u000f\u001b\u0010\u001d"+
		"\u0011\u001f\u0012!\u0013#\u0014%\u0000\u0001\u0000\u0003\u0002\u0000"+
		"\t\t  \u0004\u0000--AZ__az\u0005\u0000--09AZ__az\u00cc\u0000\u0001\u0001"+
		"\u0000\u0000\u0000\u0000\u0003\u0001\u0000\u0000\u0000\u0000\u0005\u0001"+
		"\u0000\u0000\u0000\u0000\u0007\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000"+
		"\u0000\u0000\u0000\u000b\u0001\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000"+
		"\u0000\u0000\u000f\u0001\u0000\u0000\u0000\u0000\u0011\u0001\u0000\u0000"+
		"\u0000\u0000\u0013\u0001\u0000\u0000\u0000\u0000\u0015\u0001\u0000\u0000"+
		"\u0000\u0000\u0017\u0001\u0000\u0000\u0000\u0000\u0019\u0001\u0000\u0000"+
		"\u0000\u0000\u001b\u0001\u0000\u0000\u0000\u0000\u001d\u0001\u0000\u0000"+
		"\u0000\u0000\u001f\u0001\u0000\u0000\u0000\u0000!\u0001\u0000\u0000\u0000"+
		"\u0000#\u0001\u0000\u0000\u0000\u00013\u0001\u0000\u0000\u0000\u00037"+
		"\u0001\u0000\u0000\u0000\u00059\u0001\u0000\u0000\u0000\u0007;\u0001\u0000"+
		"\u0000\u0000\t=\u0001\u0000\u0000\u0000\u000b?\u0001\u0000\u0000\u0000"+
		"\rA\u0001\u0000\u0000\u0000\u000fR\u0001\u0000\u0000\u0000\u0011c\u0001"+
		"\u0000\u0000\u0000\u0013{\u0001\u0000\u0000\u0000\u0015}\u0001\u0000\u0000"+
		"\u0000\u0017\u008f\u0001\u0000\u0000\u0000\u0019\u009e\u0001\u0000\u0000"+
		"\u0000\u001b\u00a0\u0001\u0000\u0000\u0000\u001d\u00a4\u0001\u0000\u0000"+
		"\u0000\u001f\u00ab\u0001\u0000\u0000\u0000!\u00ad\u0001\u0000\u0000\u0000"+
		"#\u00b7\u0001\u0000\u0000\u0000%\u00ba\u0001\u0000\u0000\u0000\'(\u0004"+
		"\u0000\u0000\u0000(4\u0003%\u0012\u0000)+\u0005\r\u0000\u0000*)\u0001"+
		"\u0000\u0000\u0000*+\u0001\u0000\u0000\u0000+,\u0001\u0000\u0000\u0000"+
		",/\u0005\n\u0000\u0000-/\u0002\f\r\u0000.*\u0001\u0000\u0000\u0000.-\u0001"+
		"\u0000\u0000\u0000/1\u0001\u0000\u0000\u000002\u0003%\u0012\u000010\u0001"+
		"\u0000\u0000\u000012\u0001\u0000\u0000\u000024\u0001\u0000\u0000\u0000"+
		"3\'\u0001\u0000\u0000\u00003.\u0001\u0000\u0000\u000045\u0001\u0000\u0000"+
		"\u000056\u0006\u0000\u0000\u00006\u0002\u0001\u0000\u0000\u000078\u0005"+
		"(\u0000\u00008\u0004\u0001\u0000\u0000\u00009:\u0005)\u0000\u0000:\u0006"+
		"\u0001\u0000\u0000\u0000;<\u0005,\u0000\u0000<\b\u0001\u0000\u0000\u0000"+
		"=>\u0005{\u0000\u0000>\n\u0001\u0000\u0000\u0000?@\u0005}\u0000\u0000"+
		"@\f\u0001\u0000\u0000\u0000AB\u0005/\u0000\u0000BC\u0005/\u0000\u0000"+
		"CG\u0001\u0000\u0000\u0000DF\t\u0000\u0000\u0000ED\u0001\u0000\u0000\u0000"+
		"FI\u0001\u0000\u0000\u0000GH\u0001\u0000\u0000\u0000GE\u0001\u0000\u0000"+
		"\u0000HK\u0001\u0000\u0000\u0000IG\u0001\u0000\u0000\u0000JL\u0005\r\u0000"+
		"\u0000KJ\u0001\u0000\u0000\u0000KL\u0001\u0000\u0000\u0000LM\u0001\u0000"+
		"\u0000\u0000MN\u0005\n\u0000\u0000NO\u0001\u0000\u0000\u0000OP\u0006\u0006"+
		"\u0001\u0000P\u000e\u0001\u0000\u0000\u0000QS\u0007\u0000\u0000\u0000"+
		"RQ\u0001\u0000\u0000\u0000ST\u0001\u0000\u0000\u0000TR\u0001\u0000\u0000"+
		"\u0000TU\u0001\u0000\u0000\u0000UV\u0001\u0000\u0000\u0000VW\u0006\u0007"+
		"\u0001\u0000W\u0010\u0001\u0000\u0000\u0000XY\u0005s\u0000\u0000YZ\u0005"+
		"e\u0000\u0000Z[\u0005q\u0000\u0000[\\\u0005u\u0000\u0000\\]\u0005e\u0000"+
		"\u0000]^\u0005n\u0000\u0000^_\u0005c\u0000\u0000_d\u0005e\u0000\u0000"+
		"`a\u0005s\u0000\u0000ab\u0005e\u0000\u0000bd\u0005q\u0000\u0000cX\u0001"+
		"\u0000\u0000\u0000c`\u0001\u0000\u0000\u0000d\u0012\u0001\u0000\u0000"+
		"\u0000ef\u0005f\u0000\u0000fg\u0005a\u0000\u0000gh\u0005l\u0000\u0000"+
		"hi\u0005l\u0000\u0000ij\u0005b\u0000\u0000jk\u0005a\u0000\u0000kl\u0005"+
		"c\u0000\u0000l|\u0005k\u0000\u0000mn\u0005s\u0000\u0000no\u0005e\u0000"+
		"\u0000op\u0005l\u0000\u0000pq\u0005e\u0000\u0000qr\u0005c\u0000\u0000"+
		"rs\u0005t\u0000\u0000st\u0005o\u0000\u0000t|\u0005r\u0000\u0000uv\u0005"+
		"f\u0000\u0000vw\u0005a\u0000\u0000w|\u0005l\u0000\u0000xy\u0005s\u0000"+
		"\u0000yz\u0005e\u0000\u0000z|\u0005l\u0000\u0000{e\u0001\u0000\u0000\u0000"+
		"{m\u0001\u0000\u0000\u0000{u\u0001\u0000\u0000\u0000{x\u0001\u0000\u0000"+
		"\u0000|\u0014\u0001\u0000\u0000\u0000}~\u0005p\u0000\u0000~\u007f\u0005"+
		"a\u0000\u0000\u007f\u0080\u0005r\u0000\u0000\u0080\u0081\u0005a\u0000"+
		"\u0000\u0081\u0082\u0005l\u0000\u0000\u0082\u0083\u0005l\u0000\u0000\u0083"+
		"\u0084\u0005e\u0000\u0000\u0084\u0085\u0005l\u0000\u0000\u0085\u0016\u0001"+
		"\u0000\u0000\u0000\u0086\u0087\u0005a\u0000\u0000\u0087\u0088\u0005c\u0000"+
		"\u0000\u0088\u0089\u0005t\u0000\u0000\u0089\u008a\u0005i\u0000\u0000\u008a"+
		"\u008b\u0005o\u0000\u0000\u008b\u0090\u0005n\u0000\u0000\u008c\u008d\u0005"+
		"a\u0000\u0000\u008d\u008e\u0005c\u0000\u0000\u008e\u0090\u0005t\u0000"+
		"\u0000\u008f\u0086\u0001\u0000\u0000\u0000\u008f\u008c\u0001\u0000\u0000"+
		"\u0000\u0090\u0018\u0001\u0000\u0000\u0000\u0091\u0092\u0005c\u0000\u0000"+
		"\u0092\u0093\u0005o\u0000\u0000\u0093\u0094\u0005n\u0000\u0000\u0094\u0095"+
		"\u0005d\u0000\u0000\u0095\u0096\u0005i\u0000\u0000\u0096\u0097\u0005t"+
		"\u0000\u0000\u0097\u0098\u0005i\u0000\u0000\u0098\u0099\u0005o\u0000\u0000"+
		"\u0099\u009f\u0005n\u0000\u0000\u009a\u009b\u0005c\u0000\u0000\u009b\u009c"+
		"\u0005o\u0000\u0000\u009c\u009d\u0005n\u0000\u0000\u009d\u009f\u0005d"+
		"\u0000\u0000\u009e\u0091\u0001\u0000\u0000\u0000\u009e\u009a\u0001\u0000"+
		"\u0000\u0000\u009f\u001a\u0001\u0000\u0000\u0000\u00a0\u00a1\u0005N\u0000"+
		"\u0000\u00a1\u00a2\u0005o\u0000\u0000\u00a2\u00a3\u0005t\u0000\u0000\u00a3"+
		"\u001c\u0001\u0000\u0000\u0000\u00a4\u00a8\u0007\u0001\u0000\u0000\u00a5"+
		"\u00a7\u0007\u0002\u0000\u0000\u00a6\u00a5\u0001\u0000\u0000\u0000\u00a7"+
		"\u00aa\u0001\u0000\u0000\u0000\u00a8\u00a6\u0001\u0000\u0000\u0000\u00a8"+
		"\u00a9\u0001\u0000\u0000\u0000\u00a9\u001e\u0001\u0000\u0000\u0000\u00aa"+
		"\u00a8\u0001\u0000\u0000\u0000\u00ab\u00ac\u0005:\u0000\u0000\u00ac \u0001"+
		"\u0000\u0000\u0000\u00ad\u00ae\u0005d\u0000\u0000\u00ae\u00af\u0005e\u0000"+
		"\u0000\u00af\u00b0\u0005f\u0000\u0000\u00b0\u00b1\u0001\u0000\u0000\u0000"+
		"\u00b1\u00b2\u0003%\u0012\u0000\u00b2\"\u0001\u0000\u0000\u0000\u00b3"+
		"\u00b8\u0005&\u0000\u0000\u00b4\u00b5\u0005a\u0000\u0000\u00b5\u00b6\u0005"+
		"n\u0000\u0000\u00b6\u00b8\u0005d\u0000\u0000\u00b7\u00b3\u0001\u0000\u0000"+
		"\u0000\u00b7\u00b4\u0001\u0000\u0000\u0000\u00b8$\u0001\u0000\u0000\u0000"+
		"\u00b9\u00bb\u0007\u0000\u0000\u0000\u00ba\u00b9\u0001\u0000\u0000\u0000"+
		"\u00bb\u00bc\u0001\u0000\u0000\u0000\u00bc\u00ba\u0001\u0000\u0000\u0000"+
		"\u00bc\u00bd\u0001\u0000\u0000\u0000\u00bd&\u0001\u0000\u0000\u0000\u000f"+
		"\u0000*.13GKTc{\u008f\u009e\u00a8\u00b7\u00bc\u0002\u0001\u0000\u0000"+
		"\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}