import 'package:flutter/material.dart';
import 'package:mongol/mongol.dart';
import 'package:zcode_embed_ime_db/zcode_embed_ime_db.dart';

class ZcodeImeDemo extends StatefulWidget {
  const ZcodeImeDemo({super.key});

  @override
  State<ZcodeImeDemo> createState() => _ZcodeImeDemoState();
}

class _ZcodeImeDemoState extends State<ZcodeImeDemo> {
  /// Output encoding for the suggestions. Z52 is the native encoding;
  /// MenkLetter converts each suggestion at the boundary. Note the left
  /// (vertical) field renders with the Z52 font, so MenkLetter output is
  /// best checked in the right-hand horizontal field, which uses the
  /// system font. Switching encoding rebuilds the converter and clears
  /// the in-progress word.
  MongolEncoding _outputEncoding = MongolEncoding.z52;

  @override
  Widget build(BuildContext context) {
    final Brightness brightnessValue =
        MediaQuery.of(context).platformBrightness;
    bool isDark = brightnessValue == Brightness.dark;
    final brightness = isDark ? Brightness.dark : Brightness.light;
    final theme = ThemeData(fontFamily: 'ZcodeQagan', brightness: brightness);
    return Theme(
      data: theme,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("Zcode Ime Demo"),
          actions: [
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: DropdownButton<MongolEncoding>(
                value: _outputEncoding,
                items: const [
                  DropdownMenuItem(
                      value: MongolEncoding.z52, child: Text('Z52')),
                  DropdownMenuItem(
                      value: MongolEncoding.menkLetter,
                      child: Text('MenkLetter')),
                ],
                onChanged: (value) {
                  if (value != null) {
                    setState(() => _outputEncoding = value);
                  }
                },
              ),
            ),
          ],
        ),
        body: Column(
          children: [
            const Expanded(
              child: Row(
                children: [
                  Expanded(
                    child: Padding(
                      padding: EdgeInsets.all(8.0),
                      child: MongolTextField(
                        expands: true,
                        minLines: null,
                        maxLines: null,
                        textAlignHorizontal: TextAlignHorizontal.left,
                        decoration:
                            InputDecoration(border: OutlineInputBorder()),
                      ),
                    ),
                  ),
                  Expanded(
                    child: Padding(
                      padding: EdgeInsets.all(8.0),
                      child: TextField(
                        minLines: null,
                        maxLines: null,
                        textAlignVertical: TextAlignVertical.top,
                        expands: true,
                        decoration:
                            InputDecoration(border: OutlineInputBorder()),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            EmbedKeyboard(
              layoutBuilders: [
                (i) => ZcodeLayout(i,
                    converter: DBZcodeLayoutConverter(
                        outputEncoding: _outputEncoding)),
                EnglishLayout.create
              ],
            ),
          ],
        ),
      ),
    );
  }
}
