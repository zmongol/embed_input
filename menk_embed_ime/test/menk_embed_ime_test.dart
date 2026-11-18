// Tests for the Menk layout converter and the outputEncoding boundary
// (menk_layout_converter.dart).
//
// The MenkShape (Menksoft PUA) expectations are the desktop converter's
// `z52 -> menk_shape` output for the same words — the Dart menk splicer
// must agree with that spelling, and the boundary converter must map it
// back to the same Z52 / MenkLetter. If the PUA expectation fails, the
// Dart menk splicer and the desktop converter disagree about a word's
// MenkShape spelling; if only a converted expectation fails, the
// boundary converter is at fault.
//
// Run with: flutter test (from menk_embed_ime/)
import 'package:flutter_test/flutter_test.dart';
import 'package:menk_embed_ime/menk_embed_ime.dart';

void main() {
  group('MenkLayoutConverter outputEncoding', () {
    test('defaults to MenkShape (Menksoft PUA)', () {
      final converter = MenkLayoutConverter();
      converter.appendLayoutText('mongol');
      expect(converter.suggestionWords.first,
          '\u{e2f1}\u{e291}\u{e2bd}\u{e2d9}\u{e291}\u{e2f9}');
    });
    test('z52 converts suggestions at the boundary', () {
      final converter =
          MenkLayoutConverter(outputEncoding: MongolEncoding.z52);
      converter.appendLayoutText('mongol');
      expect(converter.suggestionWords.first, 'ᢌᡭᡪᢊᡱᡱᡭᢐ');
    });
    test('menkLetter converts suggestions at the boundary', () {
      final converter =
          MenkLayoutConverter(outputEncoding: MongolEncoding.menkLetter);
      converter.appendLayoutText('mongol');
      expect(converter.suggestionWords.first, 'ᠮᠣᠩᠭᠣᠯ');
    });
    test('tang converts the same in both encodings', () {
      final z52 =
          MenkLayoutConverter(outputEncoding: MongolEncoding.z52);
      z52.appendLayoutText('tang');
      expect(z52.suggestionWords.first, 'ᢘᡪᡪᡬᡨ');
      final menkLetter =
          MenkLayoutConverter(outputEncoding: MongolEncoding.menkLetter);
      menkLetter.appendLayoutText('tang');
      expect(menkLetter.suggestionWords.first, 'ᠲᠠᠩ');
    });
  });
}
