# 开启后端服务
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c cd backend & flask run"

# 开启前端服务
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c cd frontend\front & npm run serve"

Start-Process "http://localhost:8080/#/Main"