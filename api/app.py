import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# 将项目根目录添加到系统路径
sys.path.append(os.path.join(current_dir, '..'))

from factory import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
