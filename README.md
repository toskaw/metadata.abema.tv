# metadata.abema.tv
# ABEMA 情報プロバイダ

ABEMAのビデオ情報を取得するscraperです。
yt-dlpで保存したファイル名を想定しています。

## 準備
kodi の TV番組情報はファイル名に Season と Episode の番号が必要です。以下の記述を advancedsettings.xmlに追加してください
```xml:advancedsettings.xml
<tvshowmatching action="prepend">
  <regexp>s([0-9]+)_*p([0-9]+)</regexp>
</tvshowmatching>
```

## 使い方  
  
  1. Zip形式でダウンロード<br>
  1. システム>アドオン>ZIPファイルからインストール<br>
  1. 動画を保存しているフォルダを選択してコンテキストメニューを表示<br>
  1. セットコンテンツ<br>
  1. テレビ番組,ABEMA,選択したフォルダにはテレビ番組が1件含まれています<br>

<img src="https://github.com/toskaw/metadata.abema.tv/blob/master/screenshots/download_zip.png?raw=true" alt="screenshot 1" width="400"/>
<img src="https://github.com/toskaw/metadata.abema.tv/blob/master/screenshots/install_from_zip.png?raw=true" alt="screenshot 1" width="400"/>
<img src="https://github.com/toskaw/metadata.abema.tv/blob/master/screenshots/set_contents.png?raw=true" alt="screenshot 1" width="400"/>
<img src="https://github.com/toskaw/metadata.abema.tv/blob/master/screenshots/settings.png?raw=true" alt="screenshot 1" width="400"/>
<img src="https://github.com/toskaw/metadata.abema.tv/blob/master/screenshots/list.png?raw=true" alt="screenshot 1" width="400"/>

## Tips
ABEMAのIDがシーズン番号と一致しないことがあります。

例）鬼滅の刃 ハイキュー!!

基本的にはファイルIDは以下の形式です

  シリーズID_sシーズン番号_pエピソード番号

  例) 推しの子 第１話


  https://abema.tv/video/episode/25-240_s1_p1

  シリーズID=25-240
  
  シーズン番号=1
  
  エピソード番号=1

鬼滅の刃のシーズン2 無限列車編 1話は以下のURLです。

  https://abema.tv/video/episode/26-149_s1_p1

  シリーズID=26-149
  
  シーズン番号=1
  
  エピソード番号=1

無限列車編のシーズンURLは

  https://abema.tv/video/title/26-75?s=26-75_s2&eg=26-75_eg0

  シリーズID=26-75
  
  シーズン番号=2

シリーズIDとシーズンIDが不一致なので情報取得に失敗します
  
うまく情報が取得できない場合は手動検索でシーズンIDを指定することで取得できる場合があります。

  1. フォルダを選択してコンテキストメニューを表示
  2. スキャンしてライブラリに追加
  3. タイトル候補を選ばずにMANUALを選択
  4. abema:シリーズID/シーズンIDで検索

     abema:26-75/26-75_s2
     
シリーズIDとシーズンIDはブラウザのURLから取得してください。

  例: 鬼滅の刃 無限列車編
  
  https://abema.tv/video/title/26-75?s=26-75_s2&eg=26-75_eg0

  シリーズIDは `26-75` シーズンIDは `26-75_s2` になります。
  無限列車編のファイルIDは`26-149_s1_p1`なのでシーズン1となってしまいますが、補正して取得します
  