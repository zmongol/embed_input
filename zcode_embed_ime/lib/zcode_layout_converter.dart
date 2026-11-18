/*
 * Copyright 2014 The Flutter Authors.
 * Copyright 2023 Satsrag.
 * All rights reserved.
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */
import 'package:embed_ime/embed_ime.dart';
import 'zcode_logic.dart';

/// This class is used to convert Latin to the Zcode Mongol Words.
/// [layoutText] is the Latin text that is inputted by hard/soft layout.
/// [suggestionWords] is the converted Zcode Mongol Words.
///
/// [outputEncoding] selects the encoding of the emitted suggestions.
/// It defaults to [MongolEncoding.z52], the package's native encoding, so
/// existing callers are unaffected. Pass [MongolEncoding.menkLetter] to
/// emit Unicode MenkLetter instead: each suggestion is converted at the
/// boundary by [MongolEncodingConverter.z52ToMenkLetter] (a port of the
/// verified desktop converter; 0 diffs over the 135,631-word trimmed
/// lexicon). [MongolEncoding.menkShape] is not supported here — there is
/// no ported Z52 -> MenkShape conversion — and throws [ArgumentError].
class ZcodeLayoutTextConverter with LayoutConverter {
  ZcodeLayoutTextConverter({this.outputEncoding = MongolEncoding.z52}) {
    if (outputEncoding == MongolEncoding.menkShape) {
      throw ArgumentError(
          'ZcodeLayoutTextConverter cannot emit menkShape: no Z52 -> '
          'MenkShape conversion is ported. Use z52 (default) or menkLetter.');
    }
  }

  final MongolEncoding outputEncoding;

  final zcode = ZCode();

  static const _converter = MongolEncodingConverter();

  /// Converts [words] from the package's native Z52 encoding to
  /// [outputEncoding]. A no-op when the output encoding is Z52.
  List<String> convertOutput(List<String> words) {
    if (outputEncoding == MongolEncoding.menkLetter) {
      return words.map(_converter.z52ToMenkLetter).toList();
    }
    return words;
  }

  @override
  void appendLayoutText(String text) {
    super.appendLayoutText(text);
    suggestionWords.clear();
    if (layoutText.isEmpty) return;
    suggestionWords.addAll(convertOutput(zcode.excuteEx(layoutText)));
  }

  @override
  void backspaceLayoutText(bool clear) {
    super.backspaceLayoutText(clear);
    suggestionWords.clear();
    if (layoutText.isEmpty) return;
    suggestionWords.addAll(convertOutput(zcode.excuteEx(layoutText)));
  }
}
