# ImageRetrieval-engine

### image retrieval 검색엔진 모듈


### usage
```

# DB 및 환경변수 설정
- docker-compose-env/db.env의 MYSQL_DATABASE 와 docker-compose-env/main.env의 engine_general_db 가 같아야함
- docker-compose-env/main.env 에서 MANAGER_DB_HOST는 site의 manager db
- docker-compos.yml 포트 확인

docker-compose up
```

##Todo
- 사용되는 gpu 메모리 확인
- 추가 검색 알고리즘 적용
