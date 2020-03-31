# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#!/bin/bash
data=$1
table_data=$2
output=$3
echo "Start download NLTK data"
python3 download_nltk.py
echo "Start process the origin Spider dataset"
python3 data_process.py --data_path ${data} --table_path ${table_data} --output "process_data.json"
echo "Start generate SemQL from SQL"
python3 sql2SemQL.py --data_path process_data.json --table_path ${table_data} --output ${data}

#rm process_data.json
