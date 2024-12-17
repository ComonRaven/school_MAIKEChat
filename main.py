import eel
import sys
from pathlib import Path
# pythonディレクトリをモジュールパスに追加
sys.path.append(str(Path(__file__).parent / "python"))
import testAI

eel.init("web")
eel.start("AI.html", mode="default")