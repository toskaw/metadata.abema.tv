# metadata.abema.tv
# ABEMA 情報プロバイダ

ABEMAのビデオ情報を取得するスクラッパーです。
yt-dlpで保存したファイル名を想定しています。

## 準備
kodi の TV番組情報はファイル名に Season と Episode の番号が必要です。以下の記述を advancedsettings.xmlに追加してください
```xml:advancedsettings.xml
<tvshowmatching action="prepend">
  <regexp>s([0-9]+)_*p([0-9]+)</regexp>
</tvshowmatching>
```
## Tips
ABEMAのIDがシーズン番号と一致しないことがあります。例）鬼滅の刃 ハイキュー!!
うまく情報が取得できない場合は直接シーズンIDを指定することで取得できる場合があります。

  1. フォルダを選択してコンテキストメニューを表示
  2. スキャンしてライブラリに追加
  3. タイトル候補を選ばずにMANUALを選択
  4. abema:シーズンIDで検索

シーズンIDはブラウザのURLから取得してください。

  例: 鬼滅の刃 無限列車編
  https://abema.tv/video/title/26-75?s=26-75_s2&eg=26-75_eg0

  シーズンIDは `26-75_s2` になります。
  無限列車編のファイルIDは`26-149_s1_p1`なのでシーズン1となってしまいますが、補正して取得します
  