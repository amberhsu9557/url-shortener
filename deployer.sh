#!/bin/bash
# ========================================
# Modify with deserved values
export COMPOSE_PROFILES=${COMPOSE_PROFILES:-develop} # develop, production
# ========================================
# lib
app_init () {
    docker-compose up -d transferapp
    docker-compose exec transferdb /bin/bash -c 'until psql -h localhost -U postgres -c "\q" ; do sleep 1; done'

    echo -e "Migrate ...\n"
    docker-compose exec transferapp flask db init
    docker-compose exec transferapp flask db migrate
    docker-compose exec -T transferapp flask db upgrade
}


subcommand="${1:-up}"
option="${2:-}"
shift

case $subcommand in
  gen ) # generate env files
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
