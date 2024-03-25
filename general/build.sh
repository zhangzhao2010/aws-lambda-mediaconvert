#!/bin/bash
rm -rf ./output

mkdir output
cp ./* ./output/

cd output
mkdir package

pip install -r ../requirements.txt --target ./package

cd package

find . -type d -name "tests" -exec rm -rfv {} +
find . -type d -name "__pycache__" -exec rm -rfv {} +

zip -r ../deployment_package.zip .

cd ..
zip deployment_package.zip *.py
zip deployment_package.zip *.json