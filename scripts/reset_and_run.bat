@echo off
echo ============================================================
echo SHOPX - RESET & RUN SYSTEM
echo ============================================================

echo [1/3] Dong du an va xoa volume loi...
docker compose down
docker volume rm shopx_mysql_data shopx_neo4j_data

echo [2/3] Khoi chay he thong moi voi .env...
docker compose up -d

echo [3/3] Doi he thong san sang (Neo4j & MySQL Start)...
echo Vui long cho khoang 1 phut de cac service xanh het.
echo Ban co the theo doi bang lenh: docker ps
pause
