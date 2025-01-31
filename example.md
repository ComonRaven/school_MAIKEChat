<h1>Siv3D <a href="https://github.com/Siv3D/OpenSiv3D/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-4aaa4a"></a> <a href="https://discord.gg/mzevvsY"><img src="https://img.shields.io/badge/social-Discord-404eed"></a> <a href="https://twitter.com/search?q=Siv3D%20OR%20OpenSiv3D&src=typed_query&f=live"><img src="https://img.shields.io/badge/social-Twitter-1DA1F2"></a> <a href="https://github.com/sponsors/Reputeless"><img src="https://img.shields.io/badge/funding-GitHub_Sponsors-ea4aaa"></a></h1>

<p align="center"><a href="https://siv3d.github.io/"><img src="https://raw.githubusercontent.com/Siv3D/File/master/v6/logo.png" width="480" alt="Siv3D logo"></a></p>

**Siv3D** (OpenSiv3D) is a C++20 framework for **creative coding** (2D/3D games, media art, visualizers, and simulators). Siv3D applications run on **Windows, macOS, Linux, and the Web**.


## Features

- **Graphics**
  - Advanced 2D graphics
  - Basic 3D graphics (Wavefront OBJ, primitive shapes)
  - Custom vertex / pixel shaders (HLSL, GLSL)
  - Text rendering (Bitmap, SDF, MSDF)
  - PNG, JPEG, BMP, SVG, GIF, Animated GIF, TGA, PPM, WebP, TIFF
  - Unicode 14.0 emojis and 7,000+ icons
  - Image processing
  - Video rendering
- **Audio** 
  - WAVE, MP3, AAC, OggVorbis, Opus, MIDI, WMA*, FLAC*, AIFF*
  - Adjustable volume, pan, play speed and pitch
  - File streaming (WAVE, MP3, OggVorbis)
  - Fade in and fade out
  - Looping
  - Mixing busses
  - Filters (LPF, HPF, echo, reverb)
  - FFT
  - SoundFont rendering
  - Text to speech*
- **Input**
  - Mouse
  - Keyboard
  - Gamepad
  - Webcam
  - Microphone
  - Joy-Con / Pro Controller
  - XInput*
  - Digital drawing tablet*
  - Leap Motion*
- **Window**
  - Fullscreen mode
  - High DPI support
  - Window styles (sizable, borderless)
  - File dialog
  - Drag & drop
  - Message box
  - Toast notification*
- **Network and communication**
  - HTTP client
  - Multiplayer (with Photon SDK)
  - TCP communication
  - Serial communication
  - Interprocess communication (pipe)
- **Math**
  - Vector and matrix classes (`Point`, `Float2`, `Vec2`, `Float3`, `Vec3`, `Float4`, `Vec4`, `Mat3x2`, `Mat3x3`, `Mat4x4`, `SIMD_Float4`, `Quaternion`)
  - 2D shape classes (`Line`, `Circle`, `Ellipse`, `Rect`, `RectF`, `Triangle`, `Quad`, `RoundRect`, `Polygon`, `MultiPolygon`, `LineString`, `Spline2D`, `Bezier2`, `Bezier3`)
  - 3D shape classes (`Plane`, `InfinitePlane`, `Sphere`, `Box`, `OrientedBox`, `Ray`, `Line3D`, `Triangle3D`, `ViewFrustum`, `Disc`, `Cylinder`, `Cone`)
  - Color classes (`Color`, `ColorF`, `HSV`)
  - Polar / cylindrical / spherical coordinates system
  - 2D / 3D shape intersection
  - 2D / 3D geometry processing
  - Rectangle packing
  - Planar subdivisions
  - Linear and gamma color space
  - Pseudo random number generators
  - Interpolation, easing, and smoothing
  - Perlin noise
  - Math parser
  - Navigation mesh
  - Extended arithmetic types (`HalfFloat`, `int128`, `uint128`, `BigInt`, `BigFloat`)
- **String and Text Processing**
  - Advanced String class (`String`, `StringView`)
  - Unicode conversion
  - Regular expression
  - `{fmt}` style text formatting
  - Text reader / writer classes
  - CSV / INI / JSON / XML / TOML reader classes
  - CSV / INI / JSON writer classes
- **Misc**
  - Basic GUI (button, slider, radio buttons, checkbox, text box, color picker, list box, menu bar)
  - Integrated 2D physics engine (Box2D)
  - Advanced array / 2D array classes (`Array`, `Grid`)
  - Kd-tree
  - Disjoint set
  - Asynchronous asset file streaming
  - Data compression (zlib, Zstandard)
  - Transitions between scenes
  - File system
  - Directory watcher
  - QR code reader / writer
  - GeoJSON
  - Date and time
  - Stopwatch and timer
  - Logging
  - Serialization
  - UUID
  - Child process
  - Clipboard
  - Power status
  - Scripting (AngelScript)

<small>* Some features are limited to specific platforms</small>

## How to Install Siv3D + Tutorial

- **(English) Getting Started with Siv3D:** https://siv3d.github.io/
- **(日本語) Siv3D をはじめよう:** https://siv3d.github.io/ja-jp/

**v0.6.6** | *released 22 November 2022* | [Release Notes](https://siv3d.github.io/ja-jp/releases/)

| Platform           | SDK  | Requirements                  |
|:------------------:|:----------:|:------------------------------|
| Windows            | [**Download SDK**](https://siv3d.github.io/download/windows/) /<br>[**SDK をダウンロード**](https://siv3d.github.io/ja-jp/download/windows/) | - Windows 10 / 11 (64-bit)<br>- Microsoft Visual C++ 2022 17.4<br>- Windows 10 SDK<br>- Intel / AMD CPU |
| macOS              | [**Download SDK**](https://siv3d.github.io/download/macos/) /<br>[**SDK をダウンロード**](https://siv3d.github.io/ja-jp/download/macos/) | - macOS Mojave / Catalina / Big Sur / Monterey<br>- Xcode 11.3 or newer (Big Sur requires Xcode 12.5 or newer)<br>- Intel CPU / Apple Silicon (Rosetta mode)*<br>- OpenGL 4.1 compatible hardware |
| Linux              | [**Compiling for Linux**](https://siv3d.github.io/download/ubuntu/) /<br>[**Linux 版のビルド**](https://siv3d.github.io/ja-jp/download/ubuntu/) | - GCC 9.3.0 (with Boost 1.71.0) / GCC 11.2 (with Boost 1.74.0)<br>- Intel / AMD CPU<br>- OpenGL 4.1 compatible hardware |
| Web (experimental**) | [**Compiling for Web**](https://siv3d.kamenokosoft.com/download) /<br>[**Web 版のビルド**](https://siv3d.kamenokosoft.com/ja/download) | Web browser with WebAssembly and WebGL2 support |

<small>* Native Apple Silicon support will be added in the future release. You can build and run Siv3D in Rosetta mode</small><br><small>** Some functionality may be missing or limited</small>


## Community

- [Siv3D Discord Server](https://discord.gg/mzevvsY)


## Miscellaneous

- [Open Source Software used in Siv3D](ThirdParty.md)
- [Architecture](ARCHITECTURE.md)
- [Roadmap](https://zenn.dev/reputeless/articles/opensiv3d-roadmap)


## Supporting the Project

If you would like to support the project financially, visit my GitHub Sponsors page. Your support will accelerate the development of this exciting framework.

💗 https://github.com/sponsors/Reputeless

# Super Snake (スーパースネーク)

![Game Screen](assets/GameScreen.png)

最大4人対戦のスネークゲームです

ルール：   
- 各プレイヤーは盤面の四隅からスタートします
- ステップごとに、今向いている方向から直進/右斜め前/左斜め前に進むことができます
- ゲームオーバーの条件
  - 盤面外に進む
  - 自分自身や他のプレイヤーの胴体に衝突
  - 同じステップでプレイヤー同士が同じマスに進む
- 最後まで生き残ったプレイヤーが勝ちとなります

## 設定画面

![Settings Window](assets/SettingsWindow.png)

- Preset (プリセット設定)   
  ゲーム設定を保存することができます   
  上部のボタンを左クリック：設定の呼び出し   
  上部のボタンを右クリック：設定の削除   
  `Save Preset`ボタン：設定をプリセットに名前をつけて保存

- Config (ゲーム設定)
  - Field   
    盤面の大きさ
  - Snake   
    ヘビ(プレイヤー)の数
  - Controllers   
    - Solver: コンピューター
    - Gamepad: プロコン/Joy-Conなどのコントローラーで操作 (右のConfigでボタンの割り当てができます)
    - Keyboard: キーボード操作
  - Options
    - Hide Confirmed Action   
      確定したプレイヤーの入力を非表示にします

設定をしたら、`Start!`ボタンでゲームを開始します

## ゲーム画面

![Player Input](assets/PlayerInput.png)

- 上部アイコン   
  操作中のコントローラーが表示されます。操作を確定するとアイコンが非表示になります。

- 矢印アイコン   
  次のステップで移動する向きが表示されます。今向いている向きに応じて、次の選択肢が候補に表示されます。

### 操作方法

**キーボード**

`W`/`E`/`D`/`C`/`X`/`Z`/`A`/`Q` キー：移動方向の選択

`←`/`→` キー：(操作対象が複数ある場合) 操作対象の選択

`Enter` キー：操作の確定

**コントローラー**

スティック：移動方向の選択

`L`/`R` ボタン：(操作対象が複数ある場合) 操作対象の選択

`Select` ボタン：操作の確定