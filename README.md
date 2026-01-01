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
