# bigdata_avito
## How to install: ##
1. Install Docker Desktop following the instructions (https://docs.docker.com/engine/install/)
2. Unpack the archive bigdata_avito_release.zip into an empty bigdata_avito folder for example
3. Unpack the archive `elastic.zip` into a current directory (with the new `elastic` folder)
4. In the command line in the directory with the unpacked files, run the command 'docker compose up --build'

## How to use Kibana: ##
1. Go to `http://localhost:5601/`
2. Type in the Kibana search bar `flats_dashboard`
3. Choose `Last one year` (or more) in time interval settings
4. You will see graphs
