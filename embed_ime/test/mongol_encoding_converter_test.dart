// Tests for the Mongolian encoding converter (the Dart port of the
// verified desktop converter, mongol-convert).
//
// Expected values come from the desktop converter itself: the Z52 ->
// MenkLetter expectations are the trimmed-lexicon MenkLetter column (the
// port validates with 0 diffs over all 135,631 words — see
// tools/mongol_convert_mirror.py --validate), and the MenkShape values
// are the desktop binary's `z52 -> menk_shape` output for the same words.
//
// Run with: flutter test (from embed_ime/)
import 'package:embed_ime/embed_ime.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const converter = MongolEncodingConverter();

  group('z52ToMenkLetter', () {
    test('mongol', () {
      expect(converter.z52ToMenkLetter('ᢌᡭᡪᢊᡱᡱᡭᢐ'), 'ᠮᠣᠩᠭᠣᠯ');
    });
    test('budugsen (feminine medial G)', () {
      expect(converter.z52ToMenkLetter('ᡴᡭᡬᢙᡭᢊᢔᡪᡧ'), 'ᠪᠦᠳ᠋ᠦᠭᠰᠡᠨ');
    });
    test('tang (final NG)', () {
      expect(converter.z52ToMenkLetter('ᢘᡪᡪᡬᡨ'), 'ᠲᠠᠩ');
    });
    test('sara (FVS4 final A, kept via MVS)', () {
      expect(converter.z52ToMenkLetter('ᢔᡪᢝᡨ'), 'ᠰᠠᠷ\u180eᠠ');
    });
    test('yabona (FVS4 final A, kept via MVS)', () {
      expect(converter.z52ToMenkLetter('ᢜᡪᡴᡭᡰᡨ'), 'ᠶᠠᠪᠣᠨ\u180eᠠ');
    });
    test('bodogsan (masculine medial G)', () {
      expect(converter.z52ToMenkLetter('ᡴᡭᢙᡭᡪᡪᢔᡪᡧ'), 'ᠪᠣᠳ᠋ᠣᠠᠠᠰᠠᠨ');
    });
    test('multi-word text keeps word order and spaces', () {
      expect(converter.z52ToMenkLetter('ᢌᡭᡪᢊᡱᡱᡭᢐ ᢔᡪᢝᡨ'),
          'ᠮᠣᠩᠭᠣᠯ ᠰᠠᠷ\u180eᠠ');
    });
    test('blank and non-Mongolian input pass through unchanged', () {
      expect(converter.z52ToMenkLetter(''), '');
      expect(converter.z52ToMenkLetter('   '), '   ');
      expect(converter.z52ToMenkLetter('abc'), 'abc');
    });
  });

  group('menkLetterToZ52', () {
    test('round-trips the battery words', () {
      expect(converter.menkLetterToZ52('ᠮᠣᠩᠭᠣᠯ'), 'ᢌᡭᡪᢊᡱᡱᡭᢐ');
      expect(converter.menkLetterToZ52('ᠪᠦᠳ᠋ᠦᠭᠰᠡᠨ'), 'ᡴᡭᡬᢙᡭᢊᢔᡪᡧ');
      expect(converter.menkLetterToZ52('ᠲᠠᠩ'), 'ᢘᡪᡪᡬᡨ');
      expect(converter.menkLetterToZ52('ᠰᠠᠷ\u180eᠠ'), 'ᢔᡪᢝᡨ');
      expect(converter.menkLetterToZ52('ᠶᠠᠪᠣᠨ\u180eᠠ'), 'ᢜᡪᡴᡭᡰᡨ');
      expect(converter.menkLetterToZ52('ᠮᠤ\u180b'), 'ᢌᡳ');
    });
  });

  group('menkShapeToZ52', () {
    test('mongol (Menksoft PUA in, Z52 out)', () {
      expect(
          converter.menkShapeToZ52(
              '\u{e2f1}\u{e291}\u{e2bd}\u{e2d9}\u{e291}\u{e2f9}'),
          'ᢌᡭᡪᢊᡱᡱᡭᢐ');
    });
    test('tang', () {
      expect(converter.menkShapeToZ52('\u{e308}\u{e26c}\u{e2bb}'),
          'ᢘᡪᡪᡬᡨ');
    });
  });

  group('menkShapeToMenkLetter', () {
    test('mongol (Menksoft PUA in, MenkLetter out)', () {
      expect(
          converter.menkShapeToMenkLetter(
              '\u{e2f1}\u{e291}\u{e2bd}\u{e2d9}\u{e291}\u{e2f9}'),
          'ᠮᠣᠩᠭᠣᠯ');
    });
    test('sara', () {
      expect(
          converter.menkShapeToMenkLetter(
              '\u{e2fd}\u{e26c}\u{e325}\u{e26a}'),
          'ᠰᠠᠷ\u180eᠠ');
    });
  });
}
