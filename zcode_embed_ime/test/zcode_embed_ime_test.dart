// Tests for the ZCode splicer (zcode_logic.dart) and the outputEncoding
// boundary (zcode_layout_converter.dart).
//
// The splicer expectations are the dictionary / desktop-oracle first forms
// (see tools/zcode_mirror.py): "mongol" is the ANG fix, "yabona" the FVS4
// final-A order, "bodogsan"/"budugsen" the medial-G harmony, "tang" the
// final-NG form. The desktop C++ port (splice_test) agrees on all of them.
//
// Run with: flutter test (from zcode_embed_ime/)
import 'package:flutter_test/flutter_test.dart';
import 'package:zcode_embed_ime/zcode_embed_ime.dart';

void main() {
  group('ZCode splicer', () {
    final zcode = ZCode();

    test('mongol keeps the ANG form (U+188A) of the ng digraph', () {
      // Before the fix this was 'ᢌᡭᡪᡱᡱᡭᢐ' (ANG dropped by the
      // "g before a or o" rule). The correct ANG shape is
      // U+188A U+1871 U+1871 (desktop Fix 1, G.gMiddleAngGa).
      expect(zcode.excuteEx('mongol').first, 'ᢌᡭᡪᢊᡱᡱᡭᢐ');
    });
    test('yabona puts the FVS4 final-A form first', () {
      expect(zcode.excuteEx('yabona').first, 'ᢜᡪᡴᡭᡰᡨ');
    });
    test('bodogsan puts the masculine medial G first', () {
      expect(zcode.excuteEx('bodogsan').first, 'ᡴᡭᢙᡭᡪᡪᢔᡪᡧ');
    });
    test('budugsen puts the feminine medial G first', () {
      expect(zcode.excuteEx('budugsen').first, 'ᡴᡭᡬᢙᡭᢊᢔᡪᡧ');
    });
    test('tang ends in the final-NG form U+186C U+1868', () {
      expect(zcode.excuteEx('tang').first, 'ᢘᡪᡪᡬᡨ');
    });
    test('sara and nara put the FVS4 final-A form first', () {
      expect(zcode.excuteEx('sara').first, 'ᢔᡪᢝᡨ');
      expect(zcode.excuteEx('nara').first, 'ᡯᡪᢝᡨ');
    });
  });

  group('ZcodeLayoutTextConverter outputEncoding', () {
    test('defaults to Z52', () {
      final converter = ZcodeLayoutTextConverter();
      converter.appendLayoutText('mongol');
      expect(converter.suggestionWords.first, 'ᢌᡭᡪᢊᡱᡱᡭᢐ');
    });
    test('menkLetter converts suggestions at the boundary', () {
      final converter = ZcodeLayoutTextConverter(
          outputEncoding: MongolEncoding.menkLetter);
      converter.appendLayoutText('mongol');
      expect(converter.suggestionWords.first, 'ᠮᠣᠩᠭᠣᠯ');
    });
    test('menkShape is rejected (no Z52 -> MenkShape port)', () {
      expect(
          () => ZcodeLayoutTextConverter(
              outputEncoding: MongolEncoding.menkShape),
          throwsArgumentError);
    });
  });
}
