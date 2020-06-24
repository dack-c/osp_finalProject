#!/bin/bash
cd ../elasticsearch-7.6.2
./bin/elasticsearch -d
cd ../osp_finalProject
python ./initFlask.py #리눅스 환경에서만 작동
#PY initFlask.py    #윈도우 환경에서만 작동 (둘 중 하나만 사용하시오)



