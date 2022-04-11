#!/bin/bash
# ========================================
# Modify with deserved values
export COMPOSE_PROFILES=${COMPOSE_PROFILES:-develop} # develop, production
# ========================================
# lib
app_init () {
    docker-compose up -d transferapp
    docker-compose exec transferdb /bin/bash -c 'until psql -h localhost -U postgres -c "\q" ; do sleep 1; done'

    # echo -e "Create database\n"

    # echo -e "Reset schema ...\n"
    # docker-compose exec -T backend /bin/bash -c 'django-admin reset_schema --noinput'

    # echo -e "Keep original transferdb data ...\n"
    # [ -d "./data/transferdb" ] && [ ! -f "./data/transferdb/backup/transferdb_`date +'%Y_%m_%d'`.tar" ] && cd ./data/transferdb && mkdir -p backup && sudo tar cvf "transferdb_`date +'%Y_%m_%d'`.tar" data 1>/dev/null && mv "transferdb_`date +'%Y_%m_%d'`.tar" backup/ && cd - > /dev/null

    echo -e "Migrate ...\n"
    docker-compose exec transferapp flask db init
    docker-compose exec transferapp flask db migrate
    docker-compose exec -T transferapp flask db upgrade
    # docker-compose exec -T transferapp flask db downgrade

    # echo -e "Collectstatic ...\n"
    # docker-compose exec -T backend /bin/bash -c 'django-admin collectstatic --noinput'

    # echo -e "Load fixtures ...\n"
    # substitute_fixture_template
    # docker-compose exec -T backend /bin/bash -c 'django-admin loaddata /app/fixtures/default-*.json'
    # docker-compose exec -T backend /bin/bash -c 'rm -f /app/fixtures/default-*.{json,yml}'
}


subcommand="${1:-up}"
option="${2:-}"
shift

case $subcommand in
  gen ) # generate env files
    cp ./apps/transferservice/src/config/.env.sample ./apps/transferservice/src/config/.env
    cp ./dockeryml/docker-compose.yml docker-compose.yml
    rm -f .env
    echo "COMPOSE_PROFILES='${COMPOSE_PROFILES}'" >> .env
    export $(cat .env | xargs)
    ;;
  reset|init ) # reset database and start with fixtures
    bash ./deployer.sh gen
    bash ./deployer.sh down
    
    app_init

    bash ./deployer.sh up
    ;;
  build ) # build image without cache
    bash ./deployer.sh gen
    docker-compose build --no-cache $option
    ;;
  up )
    bash ./deployer.sh gen
    docker-compose up -d --force-recreate $option
    ;;
  restart )
    docker-compose restart $option
    ;;
  exec )
    docker-compose exec $option /bin/bash
    ;;
  logs )
    docker-compose logs -f $option
    ;;
  down )
    docker-compose down --remove-orphans
    ;;
  ps )
    docker-compose ps
    ;;
  *)
    echo "Unknown command"
    ;;
esac
