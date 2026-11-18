/*
 * Copyright 2014 The Flutter Authors.
 * Copyright 2023 Satsrag.
 * All rights reserved.
 * Use of this source code is governed by a BSD-style license that can be
 * found in the LICENSE file.
 */

import 'package:embed_ime/embed_ime.dart';

import 'char_convertor.dart';

/// Converts Latin to Menksoft (MenkShape) Mongol words; see
/// [MenkLayoutConverter] in the original library for the input logic.
///
/// [outputEncoding] selects the encoding of the emitted suggestions.
/// It defaults to [MongolEncoding.menkShape], the package's native
/// encoding (Menksoft private-use shapes), so existing callers are
/// unaffected. The other values convert each suggestion at the boundary
/// with [MongolEncodingConverter] (a port of the verified desktop
/// converter):
///
/// * [MongolEncoding.z52] — via `menkShapeToZ52` (matches the desktop
///   converter exactly; the desktop converter itself differs from the
///   lexicon on 49 of 135,631 words in this direction).
/// * [MongolEncoding.menkLetter] — via `menkShapeToMenkLetter` (0 diffs
///   over the 135,631-word trimmed lexicon).
class MenkLayoutConverter with LayoutConverter {
  MenkLayoutConverter({this.outputEncoding = MongolEncoding.menkShape});

  final MongolEncoding outputEncoding;

  static const _converter = MongolEncodingConverter();

  /// Converts [words] from the package's native MenkShape encoding to
  /// [outputEncoding]. A no-op when the output encoding is MenkShape.
  List<String> convertOutput(List<String> words) {
    switch (outputEncoding) {
      case MongolEncoding.menkShape:
        return words;
      case MongolEncoding.z52:
        return words.map(_converter.menkShapeToZ52).toList();
      case MongolEncoding.menkLetter:
        return words.map(_converter.menkShapeToMenkLetter).toList();
    }
  }

  @override
  void appendLayoutText(String text) {
    super.appendLayoutText(text);
    suggestionWords.clear();
    final (latin, suggestions) = suggestion(layoutText);
    layoutText = latin;
    suggestionWords.addAll(convertOutput(suggestions));
  }

  @override
  void backspaceLayoutText(bool clear) {
    super.backspaceLayoutText(clear);
    suggestionWords.clear();
    final (latin, suggestions) = suggestion(layoutText);
    layoutText = latin;
    suggestionWords.addAll(convertOutput(suggestions));
  }

  @override
  void confirmWord(String word) {
    final nextWords = nextSuggestion(layoutText, word);
    super.confirmWord(word);
    suggestionWords.addAll(convertOutput(nextWords));
  }
}
